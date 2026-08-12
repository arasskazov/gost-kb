import json
from pathlib import Path

from gost_registry import repository as repo
from gost_registry.importer import run_import

FIXTURES = Path(__file__).parent / "fixtures"


def _copy_fixture(tmp_path: Path, *names: str) -> Path:
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    for name in names:
        (incoming / name).write_text((FIXTURES / name).read_text(encoding="utf-8"), encoding="utf-8")
    return incoming


def test_import_and_activate_full_sample(tmp_path):
    incoming = _copy_fixture(tmp_path, "gost_sample.json", "gost_r_sample.json")
    db_path = tmp_path / "registry.sqlite"
    report_path = tmp_path / "report.json"

    report = run_import(
        input_dir=incoming,
        db_path=db_path,
        snapshot_date="2026-08-11",
        activate=True,
        allow_conflicts=False,
        report_path=report_path,
    )

    assert report.activation == "active"
    assert report.total_records_read == 6
    assert report.total_records_imported == 6
    assert report.total_records_rejected == 0
    assert report_path.exists()

    conn = repo.connect(db_path)
    active_id = repo.get_active_snapshot_id(conn)
    assert active_id == report.snapshot_id
    row = repo.find_by_designation_normalized(conn, active_id, "ГОСТ Р 2.101-2023")
    assert row is not None
    assert row["title_ru_raw"] == "Единая система конструкторской документации. Виды изделий"


def test_import_rejects_record_missing_required_field(tmp_path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    bad_payload = [
        {"Обозначение": "ГОСТ 1.1-2020", "Заглавие на русском языке ": "  "},
        {"Обозначение": "ГОСТ Р 2.101-2023", "Заглавие на русском языке ": "Виды изделий"},
    ]
    (incoming / "bad.json").write_text(json.dumps(bad_payload, ensure_ascii=False), encoding="utf-8")

    db_path = tmp_path / "registry.sqlite"
    report = run_import(
        input_dir=incoming,
        db_path=db_path,
        snapshot_date=None,
        activate=True,
        allow_conflicts=False,
        report_path=tmp_path / "report.json",
    )

    assert report.total_records_rejected == 1
    assert report.total_records_imported == 1
    assert report.activation == "active"

    conn = repo.connect(db_path)
    rejections = conn.execute("SELECT * FROM import_rejections").fetchall()
    assert len(rejections) == 1
    assert rejections[0]["error_code"] == "REQUIRED_FIELD_EMPTY"


def test_import_invalid_json_root_blocks_activation(tmp_path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    (incoming / "not_a_list.json").write_text(json.dumps({"a": 1}), encoding="utf-8")

    db_path = tmp_path / "registry.sqlite"
    report = run_import(
        input_dir=incoming,
        db_path=db_path,
        snapshot_date=None,
        activate=True,
        allow_conflicts=False,
        report_path=tmp_path / "report.json",
    )

    assert report.activation == "failed"
    assert report.blocking_errors

    conn = repo.connect(db_path)
    assert repo.get_active_snapshot_id(conn) is None


def test_import_conflict_blocks_activation_without_allow_conflicts(tmp_path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    file_a = [
        {
            "Обозначение": "ГОСТ Р 2.101-2023",
            "Заглавие на русском языке ": "Заглавие версия А",
            "Статус": "Действует",
            "Код ОКС": "01.110",
        }
    ]
    file_b = [
        {
            "Обозначение": "ГОСТ Р 2.101-2023",
            "Заглавие на русском языке ": "Заглавие версия Б (конфликт)",
            "Статус": "Действует",
            "Код ОКС": "01.110",
        }
    ]
    (incoming / "a_file.json").write_text(json.dumps(file_a, ensure_ascii=False), encoding="utf-8")
    (incoming / "b_file.json").write_text(json.dumps(file_b, ensure_ascii=False), encoding="utf-8")

    db_path = tmp_path / "registry.sqlite"
    report = run_import(
        input_dir=incoming,
        db_path=db_path,
        snapshot_date=None,
        activate=True,
        allow_conflicts=False,
        report_path=tmp_path / "report.json",
    )

    assert report.total_conflicts == 1
    assert report.activation == "staged"  # не активирован из-за конфликта

    conn = repo.connect(db_path)
    assert repo.get_active_snapshot_id(conn) is None


def test_import_conflict_allowed_with_flag(tmp_path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    file_a = [
        {
            "Обозначение": "ГОСТ Р 2.101-2023",
            "Заглавие на русском языке ": "Заглавие версия А",
            "Статус": "Действует",
            "Код ОКС": "01.110",
        }
    ]
    file_b = [
        {
            "Обозначение": "ГОСТ Р 2.101-2023",
            "Заглавие на русском языке ": "Заглавие версия Б (конфликт)",
            "Статус": "Действует",
            "Код ОКС": "01.110",
        }
    ]
    (incoming / "a_file.json").write_text(json.dumps(file_a, ensure_ascii=False), encoding="utf-8")
    (incoming / "b_file.json").write_text(json.dumps(file_b, ensure_ascii=False), encoding="utf-8")

    db_path = tmp_path / "registry.sqlite"
    report = run_import(
        input_dir=incoming,
        db_path=db_path,
        snapshot_date=None,
        activate=True,
        allow_conflicts=True,
        report_path=tmp_path / "report.json",
    )

    assert report.total_conflicts == 1
    assert report.activation == "active"


def test_import_true_duplicate_not_counted_as_conflict(tmp_path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    record = {
        "Обозначение": "ГОСТ Р 2.101-2023",
        "Заглавие на русском языке ": "Единая система конструкторской документации. Виды изделий",
        "Статус": "Действует",
        "Код ОКС": "01.110",
    }
    (incoming / "a_file.json").write_text(json.dumps([record], ensure_ascii=False), encoding="utf-8")
    (incoming / "b_file.json").write_text(json.dumps([record], ensure_ascii=False), encoding="utf-8")

    db_path = tmp_path / "registry.sqlite"
    report = run_import(
        input_dir=incoming,
        db_path=db_path,
        snapshot_date=None,
        activate=True,
        allow_conflicts=False,
        report_path=tmp_path / "report.json",
    )

    assert report.total_conflicts == 0
    assert report.total_duplicates == 1
    assert report.activation == "active"
    assert report.total_records_imported == 1
