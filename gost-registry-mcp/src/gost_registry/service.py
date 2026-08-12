"""Доменный сервис (раздел 6, 9 Шаг 6 ТЗ) — без зависимости от MCP-транспорта.

Реализует: normalize_designation, resolve_standard, verify_reference,
search_standards, get_registry_provenance. Все операции — только чтение
активного снимка реестра.
"""
from __future__ import annotations

import difflib
import json
import sqlite3
from pathlib import Path
from typing import Optional

from . import repository as repo
from .config import NEGATIVE_RESULT_DISCLAIMER, PROVENANCE_DISCLAIMER
from .models import (
    NormalizedDesignation,
    ProvenanceInfo,
    RegistrySnapshotRef,
    SearchCandidate,
    SearchResult,
    VerificationResult,
)
from .normalization import normalize_title, parse_designation


class NoActiveSnapshotError(RuntimeError):
    """Нет активного снимка реестра — реестр пуст либо не активирован."""


class RegistryService:
    """Сервис только для чтения над активным снимком локального реестра."""

    def __init__(self, db_path: Path | str):
        self._db_path = Path(db_path)
        self._conn: Optional[sqlite3.Connection] = None

    def _connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = repo.connect(self._db_path)
            repo.init_schema(self._conn)
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _active_snapshot_id(self) -> str:
        conn = self._connection()
        snapshot_id = repo.get_active_snapshot_id(conn)
        if not snapshot_id:
            raise NoActiveSnapshotError(
                "В базе нет активного снимка реестра. Выполните импорт с флагом --activate."
            )
        return snapshot_id

    def _snapshot_ref(self, snapshot_id: str) -> RegistrySnapshotRef:
        row = repo.get_snapshot_row(self._connection(), snapshot_id)
        snapshot_date = row["snapshot_date"] if row else None
        return RegistrySnapshotRef(snapshot_id=snapshot_id, snapshot_date=snapshot_date)

    # ------------------------------------------------------------------ #
    # 6.2 normalize_designation
    # ------------------------------------------------------------------ #
    def normalize_designation(self, designation: str) -> NormalizedDesignation:
        return parse_designation(designation)

    # ------------------------------------------------------------------ #
    # 6.3 resolve_standard
    # ------------------------------------------------------------------ #
    def resolve_standard(self, designation: str) -> VerificationResult:
        if not designation or not designation.strip():
            return VerificationResult(
                verdict="invalid_input",
                input={"designation": designation},
                diagnostics=["Обозначение пусто."],
            )

        try:
            snapshot_id = self._active_snapshot_id()
        except NoActiveSnapshotError as exc:
            return VerificationResult(
                verdict="designation_not_found",
                input={"designation": designation},
                diagnostics=[str(exc), NEGATIVE_RESULT_DISCLAIMER],
            )

        parsed = parse_designation(designation)
        if not parsed.designation_normalized:
            return VerificationResult(
                registry_snapshot=self._snapshot_ref(snapshot_id),
                verdict="invalid_input",
                input={"designation": designation},
                diagnostics=parsed.diagnostics or ["Обозначение не разобрано."],
            )

        row = repo.find_by_designation_normalized(self._connection(), snapshot_id, parsed.designation_normalized)
        if row is None:
            return VerificationResult(
                registry_snapshot=self._snapshot_ref(snapshot_id),
                verdict="designation_not_found",
                confidence=0.0,
                input={"designation": designation},
                diagnostics=[
                    f"Обозначение '{parsed.designation_normalized}' не найдено в активном снимке.",
                    NEGATIVE_RESULT_DISCLAIMER,
                ],
            )

        return VerificationResult(
            registry_snapshot=self._snapshot_ref(snapshot_id),
            verdict="verified_designation_only",
            confidence=0.95,
            input={"designation": designation},
            canonical=_row_to_canonical_dict(row),
            diagnostics=["Обозначение найдено. Заглавие не передано для сверки."],
        )

    # ------------------------------------------------------------------ #
    # 6.4 verify_reference
    # ------------------------------------------------------------------ #
    def verify_reference(
        self, designation: str, title_ru: Optional[str] = None, require_active_status: bool = False
    ) -> VerificationResult:
        if not designation or not designation.strip():
            return VerificationResult(
                verdict="invalid_input",
                input={"designation": designation, "title_ru": title_ru},
                diagnostics=["Обозначение пусто."],
            )

        try:
            snapshot_id = self._active_snapshot_id()
        except NoActiveSnapshotError as exc:
            return VerificationResult(
                verdict="designation_not_found",
                input={"designation": designation, "title_ru": title_ru},
                diagnostics=[str(exc), NEGATIVE_RESULT_DISCLAIMER],
            )

        parsed = parse_designation(designation)
        input_payload = {"designation": designation, "title_ru": title_ru}

        if not parsed.designation_normalized or not parsed.parsed:
            # Обозначение не разобрано синтаксически — не подтверждаем и не
            # отклоняем однозначно; предлагаем кандидатов, если есть заглавие.
            candidates = []
            if title_ru:
                candidates = self._fuzzy_candidates(snapshot_id, title_ru, limit=5)
            verdict = "ambiguous" if candidates else "designation_not_found"
            diags = list(parsed.diagnostics)
            if verdict == "designation_not_found":
                diags.append(NEGATIVE_RESULT_DISCLAIMER)
            return VerificationResult(
                registry_snapshot=self._snapshot_ref(snapshot_id),
                verdict=verdict,
                confidence=0.0,
                input=input_payload,
                candidates=[c.model_dump() for c in candidates],
                diagnostics=diags,
            )

        row = repo.find_by_designation_normalized(self._connection(), snapshot_id, parsed.designation_normalized)
        if row is None:
            return VerificationResult(
                registry_snapshot=self._snapshot_ref(snapshot_id),
                verdict="designation_not_found",
                confidence=0.0,
                input=input_payload,
                diagnostics=[
                    f"Обозначение '{parsed.designation_normalized}' не найдено в активном снимке.",
                    NEGATIVE_RESULT_DISCLAIMER,
                ],
            )

        canonical = _row_to_canonical_dict(row)

        if require_active_status and row["status"] and row["status"] != "Действует":
            diag_status = [f"Статус в снимке: '{row['status']}' (запрошено 'Действует')."]
        else:
            diag_status = []

        if title_ru is None or not title_ru.strip():
            return VerificationResult(
                registry_snapshot=self._snapshot_ref(snapshot_id),
                verdict="verified_designation_only",
                confidence=0.95,
                input=input_payload,
                canonical=canonical,
                diagnostics=["Обозначение найдено. Заглавие не передано для сверки."] + diag_status,
            )

        title_norm_input = normalize_title(title_ru)
        if title_norm_input == row["title_ru_normalized"]:
            return VerificationResult(
                registry_snapshot=self._snapshot_ref(snapshot_id),
                verdict="verified",
                confidence=1.0,
                input=input_payload,
                canonical=canonical,
                diagnostics=["Обозначение и заглавие совпадают с канонической записью."] + diag_status,
            )

        return VerificationResult(
            registry_snapshot=self._snapshot_ref(snapshot_id),
            verdict="title_mismatch",
            confidence=0.95,
            input=input_payload,
            canonical=canonical,
            diagnostics=[
                "Обозначение найдено, переданное заглавие не совпадает с каноническим.",
                f"Каноническое заглавие: '{row['title_ru_raw']}'.",
            ]
            + diag_status,
        )

    # ------------------------------------------------------------------ #
    # 6.5 search_standards
    # ------------------------------------------------------------------ #
    def search_standards(
        self,
        query: Optional[str] = None,
        series: Optional[str] = None,
        ics_code_prefix: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 10,
    ) -> SearchResult:
        try:
            snapshot_id = self._active_snapshot_id()
        except NoActiveSnapshotError as exc:
            return SearchResult(verdict="no_candidates", diagnostics=[str(exc)])

        if limit <= 0:
            return SearchResult(
                registry_snapshot=self._snapshot_ref(snapshot_id),
                verdict="invalid_input",
                diagnostics=["limit должен быть положительным целым числом."],
            )

        conn = self._connection()
        sql = "SELECT * FROM standards_registry WHERE snapshot_id = ?"
        params: list = [snapshot_id]
        if series:
            sql += " AND series = ?"
            params.append(series)
        if status:
            sql += " AND status = ?"
            params.append(status)
        rows = conn.execute(sql, params).fetchall()

        if ics_code_prefix:
            rows = [r for r in rows if any(c.startswith(ics_code_prefix) for c in json.loads(r["ics_codes_json"]))]

        candidates: list[SearchCandidate] = []
        if query and query.strip():
            candidates = self._rank_by_query(rows, query, limit)
        else:
            for r in rows[:limit]:
                candidates.append(_row_to_candidate(r, "exact", 1.0))

        verdict = "candidates_found" if candidates else "no_candidates"
        diagnostics = [] if candidates else ["Кандидаты не найдены по заданным фильтрам."]

        return SearchResult(
            registry_snapshot=self._snapshot_ref(snapshot_id),
            verdict=verdict,
            candidates=candidates,
            diagnostics=diagnostics,
        )

    def _rank_by_query(self, rows: list[sqlite3.Row], query: str, limit: int) -> list[SearchCandidate]:
        query_norm = normalize_title(query)
        query_tokens = set(query_norm.split())
        scored: list[tuple[float, str, sqlite3.Row]] = []

        for r in rows:
            title_norm = r["title_ru_normalized"]
            if query_norm == title_norm:
                scored.append((1.0, "exact", r))
                continue
            if title_norm.startswith(query_norm) or query_norm in title_norm:
                scored.append((0.85, "prefix", r))
                continue
            title_tokens = set(title_norm.split())
            overlap = query_tokens & title_tokens
            if overlap:
                score = len(overlap) / max(len(query_tokens), 1)
                scored.append((0.5 + 0.3 * score, "token", r))
                continue
            ratio = difflib.SequenceMatcher(None, query_norm, title_norm).ratio()
            if ratio >= 0.6:
                scored.append((ratio * 0.6, "fuzzy", r))

        scored.sort(key=lambda t: t[0], reverse=True)
        return [_row_to_candidate(r, match_type, score) for score, match_type, r in scored[:limit]]

    def _fuzzy_candidates(self, snapshot_id: str, title_ru: str, limit: int) -> list[SearchCandidate]:
        rows = repo.all_records_for_snapshot(self._connection(), snapshot_id)
        return self._rank_by_query(list(rows), title_ru, limit)

    # ------------------------------------------------------------------ #
    # 6.6 get_registry_provenance
    # ------------------------------------------------------------------ #
    def get_registry_provenance(self) -> ProvenanceInfo:
        conn = self._connection()
        active_id = repo.get_active_snapshot_id(conn)
        if not active_id:
            return ProvenanceInfo(limitation=PROVENANCE_DISCLAIMER)

        row = repo.get_snapshot_row(conn, active_id)
        files = repo.list_snapshot_files(conn, active_id)
        return ProvenanceInfo(
            registry_snapshot=self._snapshot_ref(active_id),
            active_snapshot_id=active_id,
            imported_at=row["imported_at"] if row else None,
            files=[dict(f) for f in files],
            total_records_imported=row["records_imported"] if row else 0,
            total_records_rejected=row["records_rejected"] if row else 0,
            limitation=PROVENANCE_DISCLAIMER,
        )


def _row_to_canonical_dict(row: sqlite3.Row) -> dict:
    return {
        "standard_id": row["standard_id"],
        "designation_raw": row["designation_raw"],
        "designation_normalized": row["designation_normalized"],
        "series": row["series"],
        "number_part": row["number_part"],
        "year": row["year"],
        "title_ru": row["title_ru_raw"],
        "status": row["status"],
        "ics_codes": json.loads(row["ics_codes_json"]),
        "needs_review": bool(row["needs_review"]),
        "source_filename": row["source_filename"],
    }


def _row_to_candidate(row: sqlite3.Row, match_type: str, score: float) -> SearchCandidate:
    return SearchCandidate(
        match_type=match_type,  # type: ignore[arg-type]
        score=round(score, 4),
        designation_normalized=row["designation_normalized"],
        title_ru_raw=row["title_ru_raw"],
        status=row["status"],
        ics_codes=json.loads(row["ics_codes_json"]),
        standard_id=row["standard_id"],
    )
