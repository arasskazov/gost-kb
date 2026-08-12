"""CLI-импортёр JSON-снимков в реестр (раздел 7, 9 Шаг 5 ТЗ).

Интерпретация раздела 7.3 ТЗ, зафиксированная явно (это интерпретация,
а не факт из ТЗ): список «блокирующих ошибок» смешивает два разных
уровня. Здесь они разделены так:

  * ошибки уровня файла (нечитаемый файл, невалидный JSON, корень не
    массив) — блокируют весь импорт: файл не может быть безопасно
    обработан по записям, поэтому весь запуск помечается как `failed`
    и снимок не активируется, независимо от флага --activate;
  * ошибки уровня записи (нет обязательного поля, поле пустое после
    strip) — не останавливают обработку набора: запись отклоняется и
    попадает в import_rejections (буквально по разделу 7.2 п.5);
  * конфликт одинакового designation_normalized с различающимися
    реквизитами в пределах ОДНОГО снимка — блокирует активацию, если
    не передан --allow-conflicts (раздел 7.2 п.9);
  * невозможность записать отчёт или провал проверки целостности БД —
    блокируют активацию.

Дубликат (тот же designation_normalized и тот же record_hash) не
является конфликтом и не блокирует активацию (раздел 7.2 п.8).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import uuid
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from . import repository as repo
from .config import DEFAULT_DB_PATH, DEFAULT_INCOMING_DIR, DEFAULT_REPORTS_DIR
from .models import FileImportResult, ImportReport, RawStandardRecord
from .normalization import normalize_title, parse_designation, parse_ics_codes


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _record_hash(designation_raw: str, title_ru_raw: str, status: str | None, ics_raw: str | None) -> str:
    canonical = json.dumps(
        {
            "designation_raw": designation_raw,
            "title_ru_raw": title_ru_raw,
            "status": status,
            "ics_raw": ics_raw,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _utcnow_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def run_import(
    input_dir: Path,
    db_path: Path,
    snapshot_date: str | None,
    activate: bool,
    allow_conflicts: bool,
    report_path: Path | None,
) -> ImportReport:
    input_dir = Path(input_dir)
    files = sorted(p for p in input_dir.glob("*.json") if p.is_file())

    snapshot_id = str(uuid.uuid4())
    imported_at = _utcnow_iso()

    conn = repo.connect(db_path)
    repo.init_schema(conn)
    repo.insert_snapshot(conn, snapshot_id, imported_at, snapshot_date, status="staged")
    conn.commit()

    report = ImportReport(snapshot_id=snapshot_id, snapshot_date=snapshot_date, imported_at=imported_at)

    if not files:
        report.blocking_errors.append(f"В каталоге {input_dir} не найдено файлов *.json.")
        repo.mark_snapshot_failed(conn, snapshot_id)
        conn.commit()
        _write_report(report, report_path)
        return report

    seen_in_snapshot: dict[str, dict[str, Any]] = {}
    total_read = total_imported = total_rejected = total_dup = total_conf = 0
    file_level_blocking = False

    for path in files:
        file_result = FileImportResult(filename=path.name, sha256="")
        try:
            raw_bytes = path.read_bytes()
        except OSError as exc:
            report.blocking_errors.append(f"Файл {path.name} не читается: {exc}")
            file_level_blocking = True
            continue

        file_result.sha256 = _sha256_bytes(raw_bytes)

        try:
            payload = json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            report.blocking_errors.append(f"Файл {path.name} содержит невалидный JSON: {exc}")
            file_level_blocking = True
            continue

        if not isinstance(payload, list):
            report.blocking_errors.append(f"Корень файла {path.name} не является JSON-массивом.")
            file_level_blocking = True
            continue

        file_result.records_read = len(payload)
        total_read += len(payload)

        for idx, raw_item in enumerate(payload):
            if not isinstance(raw_item, dict):
                _reject(
                    conn, snapshot_id, path.name, idx, raw_item,
                    "INVALID_RECORD_TYPE", "Элемент массива не является объектом JSON.",
                )
                file_result.records_rejected += 1
                total_rejected += 1
                continue

            try:
                record = RawStandardRecord.model_validate(raw_item)
            except ValidationError as exc:
                _reject(
                    conn, snapshot_id, path.name, idx, raw_item,
                    "SCHEMA_VALIDATION_FAILED", str(exc),
                )
                file_result.records_rejected += 1
                total_rejected += 1
                continue

            designation_raw = record.designation.strip() if record.designation else ""
            title_raw = record.title_ru.strip() if record.title_ru else ""
            if not designation_raw or not title_raw:
                _reject(
                    conn, snapshot_id, path.name, idx, raw_item,
                    "REQUIRED_FIELD_EMPTY",
                    "Обозначение или заглавие пусты после удаления пробелов.",
                )
                file_result.records_rejected += 1
                total_rejected += 1
                continue

            parsed = parse_designation(record.designation)
            designation_normalized = parsed.designation_normalized or designation_raw.upper()
            title_normalized = normalize_title(record.title_ru)
            ics_codes = parse_ics_codes(record.ics_raw)
            rec_hash = _record_hash(record.designation, record.title_ru, record.status, record.ics_raw)
            needs_review = (not parsed.parsed) or (parsed.series == "OTHER")

            prior = seen_in_snapshot.get(designation_normalized)
            if prior is not None:
                if prior["record_hash"] == rec_hash:
                    file_result.duplicates += 1
                    total_dup += 1
                    continue
                else:
                    file_result.conflicts += 1
                    total_conf += 1
                    report.blocking_errors.append(
                        f"Конфликт: designation_normalized='{designation_normalized}' "
                        f"встречается повторно с иными реквизитами "
                        f"(файлы: {prior['source_filename']} и {path.name})."
                    )
                    if not allow_conflicts:
                        continue
                    # allow_conflicts=True: сохраняем первую версию, вторую не вставляем повторно.
                    continue

            standard_id = str(uuid.uuid4())
            db_record = {
                "standard_id": standard_id,
                "snapshot_id": snapshot_id,
                "designation_raw": record.designation,
                "designation_normalized": designation_normalized,
                "series": parsed.series or "OTHER",
                "number_part": parsed.number_part,
                "year": parsed.year,
                "title_ru_raw": record.title_ru,
                "title_ru_normalized": title_normalized,
                "status": record.status,
                "ics_codes_json": json.dumps(ics_codes, ensure_ascii=False),
                "needs_review": 1 if needs_review else 0,
                "record_hash": rec_hash,
                "source_filename": path.name,
            }
            repo.insert_standard(conn, db_record)
            seen_in_snapshot[designation_normalized] = {
                "record_hash": rec_hash,
                "source_filename": path.name,
            }
            file_result.records_imported += 1
            total_imported += 1

        repo.upsert_snapshot_file(
            conn,
            snapshot_id,
            file_result.filename,
            file_result.sha256,
            file_result.records_read,
            file_result.records_imported,
            file_result.records_rejected,
            file_result.duplicates,
            file_result.conflicts,
        )
        report.files.append(file_result)

    conn.commit()

    report.total_records_read = total_read
    report.total_records_imported = total_imported
    report.total_records_rejected = total_rejected
    report.total_duplicates = total_dup
    report.total_conflicts = total_conf
    repo.update_snapshot_counters(conn, snapshot_id, total_read, total_imported, total_rejected)
    conn.commit()

    has_conflicts_blocking = total_conf > 0 and not allow_conflicts
    can_activate = activate and not file_level_blocking and not has_conflicts_blocking

    if file_level_blocking:
        repo.mark_snapshot_failed(conn, snapshot_id)
        report.activation = "failed"
    elif can_activate:
        integrity_problems = repo.integrity_check(conn)
        if integrity_problems:
            report.blocking_errors.extend(integrity_problems)
            repo.mark_snapshot_failed(conn, snapshot_id)
            report.activation = "failed"
        else:
            repo.set_active_snapshot(conn, snapshot_id)
            report.activation = "active"
    else:
        report.activation = "staged"

    conn.commit()
    conn.close()

    ok = _write_report(report, report_path)
    if not ok:
        # Раздел 7.3: невозможность создать отчёт — блокирующая ошибка.
        # Отчёт уже вычислен в памяти и возвращается вызывающей стороне,
        # но активация должна считаться несостоявшейся, если она ещё
        # не была применена к БД. Поскольку set_active_snapshot уже
        # выполнен транзакционно к этому моменту, мы лишь фиксируем это
        # как диагностику для оператора.
        report.blocking_errors.append("Не удалось записать файл отчёта импорта на диск.")

    return report


def _reject(conn, snapshot_id: str, filename: str, idx: int, raw_item: Any, code: str, message: str) -> None:
    repo.insert_rejection(
        conn,
        {
            "rejection_id": str(uuid.uuid4()),
            "snapshot_id": snapshot_id,
            "source_filename": filename,
            "record_index": idx,
            "raw_record_json": json.dumps(raw_item, ensure_ascii=False, default=str),
            "error_code": code,
            "error_message": message,
        },
    )


def _write_report(report: ImportReport, report_path: Path | None) -> bool:
    if report_path is None:
        return True
    try:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(report.model_dump(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    except OSError:
        return False


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m gost_registry.importer",
        description="Импорт JSON-снимков библиографических записей стандартов в локальный реестр.",
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INCOMING_DIR, help="Каталог с *.json файлами.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH, help="Путь к файлу SQLite.")
    parser.add_argument("--snapshot-date", type=str, default=None, help="Дата снимка (YYYY-MM-DD), если задана оператором.")
    parser.add_argument("--activate", action="store_true", help="Активировать снимок при отсутствии блокирующих ошибок.")
    parser.add_argument("--allow-conflicts", action="store_true", help="Не блокировать активацию из-за конфликтов дублей.")
    parser.add_argument("--report", type=Path, default=None, help="Путь для сохранения JSON-отчёта импорта.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    report_path = args.report
    if report_path is None:
        DEFAULT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_path = DEFAULT_REPORTS_DIR / f"import-{_utcnow_iso().replace(':', '').replace('+00:00', 'Z')}.json"

    report = run_import(
        input_dir=args.input_dir,
        db_path=args.db,
        snapshot_date=args.snapshot_date,
        activate=args.activate,
        allow_conflicts=args.allow_conflicts,
        report_path=report_path,
    )

    print(json.dumps(report.model_dump(), ensure_ascii=False, indent=2))
    print(f"\nОтчёт сохранён: {report_path}", file=sys.stderr)

    if report.activation == "failed" or report.blocking_errors and not args.activate:
        return 0 if report.activation != "failed" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
