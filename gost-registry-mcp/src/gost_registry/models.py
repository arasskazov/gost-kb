"""Pydantic-модели входных, внутренних и выходных структур (раздел 4, 9 ТЗ)."""
from __future__ import annotations

import datetime as dt
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .config import FIELD_DESIGNATION, FIELD_ICS, FIELD_STATUS, FIELD_TITLE

Verdict = Literal[
    "verified",
    "verified_designation_only",
    "title_mismatch",
    "designation_not_found",
    "ambiguous",
    "invalid_input",
]

ImportStatus = Literal["staged", "active", "failed", "superseded"]


class RawStandardRecord(BaseModel):
    """Исходная запись ровно в том виде, в котором она пришла из JSON.

    Модель принимает только известные поля (raise на неизвестных ключах
    не выполняется намеренно: раздел 2.3 ТЗ требует не отклонять записи
    только из-за дополнительных полей — они будут проигнорированы, но
    факт их наличия не блокирует импорт). Обязательные поля — обозначение
    и заглавие; статус и ОКС могут быть не заданы.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    designation: str = Field(alias=FIELD_DESIGNATION)
    title_ru: str = Field(alias=FIELD_TITLE)
    status: Optional[str] = Field(default=None, alias=FIELD_STATUS)
    ics_raw: Optional[str] = Field(default=None, alias=FIELD_ICS)


class NormalizedDesignation(BaseModel):
    """Результат синтаксического разбора обозначения (раздел 5.1, 6.2 ТЗ)."""

    input: str
    designation_normalized: Optional[str] = None
    series: Optional[str] = None
    number_part: Optional[str] = None
    year: Optional[int] = None
    parsed: bool = False
    diagnostics: list[str] = Field(default_factory=list)


class CanonicalStandardRecord(BaseModel):
    """Каноническая запись реестра (таблица standards_registry, раздел 4.2)."""

    standard_id: str
    snapshot_id: str
    designation_raw: str
    designation_normalized: str
    series: str
    number_part: Optional[str] = None
    year: Optional[int] = None
    title_ru_raw: str
    title_ru_normalized: str
    status: Optional[str] = None
    ics_codes: list[str] = Field(default_factory=list)
    needs_review: bool = False
    record_hash: str
    source_filename: str


class RejectedRecord(BaseModel):
    """Отклонённая при импорте запись (таблица import_rejections, раздел 4.3)."""

    rejection_id: str
    snapshot_id: str
    source_filename: str
    record_index: int
    raw_record: dict
    error_code: str
    error_message: str


class FileImportResult(BaseModel):
    filename: str
    sha256: str
    records_read: int = 0
    records_imported: int = 0
    records_rejected: int = 0
    duplicates: int = 0
    conflicts: int = 0


class ImportReport(BaseModel):
    """Итоговый отчёт импорта (раздел 7.4 ТЗ)."""

    snapshot_id: str
    snapshot_date: Optional[str] = None
    imported_at: str
    files: list[FileImportResult] = Field(default_factory=list)
    total_records_read: int = 0
    total_records_imported: int = 0
    total_records_rejected: int = 0
    total_duplicates: int = 0
    total_conflicts: int = 0
    activation: ImportStatus = "staged"
    blocking_errors: list[str] = Field(default_factory=list)


class RegistrySnapshotRef(BaseModel):
    """Ссылка на снимок реестра, включаемая в каждый ответ MCP (раздел 6.1)."""

    snapshot_id: str
    snapshot_date: Optional[str] = None
    source_scope: str = "local_registry"


class VerificationResult(BaseModel):
    """Результат `verify_reference` / `resolve_standard` (раздел 6.3, 6.4)."""

    registry_snapshot: Optional[RegistrySnapshotRef] = None
    verdict: Verdict
    confidence: float = 0.0
    input: dict = Field(default_factory=dict)
    canonical: Optional[dict] = None
    candidates: list[dict] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)


class SearchCandidate(BaseModel):
    match_type: Literal["exact", "prefix", "token", "fuzzy"]
    score: float
    designation_normalized: str
    title_ru_raw: str
    status: Optional[str] = None
    ics_codes: list[str] = Field(default_factory=list)
    standard_id: str


class SearchResult(BaseModel):
    registry_snapshot: Optional[RegistrySnapshotRef] = None
    verdict: Literal["candidates_found", "no_candidates", "invalid_input"] = "no_candidates"
    candidates: list[SearchCandidate] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)


class ProvenanceInfo(BaseModel):
    registry_snapshot: Optional[RegistrySnapshotRef] = None
    active_snapshot_id: Optional[str] = None
    imported_at: Optional[str] = None
    files: list[dict] = Field(default_factory=list)
    total_records_imported: int = 0
    total_records_rejected: int = 0
    limitation: str
