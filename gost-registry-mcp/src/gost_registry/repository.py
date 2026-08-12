"""Схема БД и репозиторий (раздел 4, 9 Шаг 4 ТЗ).

Хранилище — SQLite (раздел 3.2 ТЗ, локальный однопользовательский режим).
Все операции импорта выполняются в одной транзакции на снимок; активный
снимок переключается атомарно через таблицу `registry_state`.

Отклонение от буквального текста раздела 4.1 ТЗ: таблица
`registry_snapshots` в ТЗ описана с единственными полями
`source_filename`/`source_sha256`, что подходит для снимка из одного
файла. Раздел 2.2 ТЗ явно допускает снимок из произвольного числа
файлов, а раздел 7.4 определяет отчёт со списком `files`. Поэтому здесь
`registry_snapshots` хранит агрегат снимка (даты, итоговые счётчики,
статус), а файловый уровень вынесен в дочернюю таблицу `snapshot_files`
— без потери ни одного поля, требуемого ТЗ, только с более нормальной
формой хранения для многофайловых снимков.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS registry_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    imported_at TEXT NOT NULL,
    snapshot_date TEXT,
    records_read INTEGER NOT NULL DEFAULT 0,
    records_imported INTEGER NOT NULL DEFAULT 0,
    records_rejected INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('staged','active','failed','superseded'))
);

CREATE TABLE IF NOT EXISTS snapshot_files (
    snapshot_id TEXT NOT NULL REFERENCES registry_snapshots(snapshot_id) ON DELETE CASCADE,
    source_filename TEXT NOT NULL,
    source_sha256 TEXT NOT NULL,
    records_read INTEGER NOT NULL DEFAULT 0,
    records_imported INTEGER NOT NULL DEFAULT 0,
    records_rejected INTEGER NOT NULL DEFAULT 0,
    duplicates INTEGER NOT NULL DEFAULT 0,
    conflicts INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (snapshot_id, source_filename)
);

CREATE TABLE IF NOT EXISTS standards_registry (
    standard_id TEXT PRIMARY KEY,
    snapshot_id TEXT NOT NULL REFERENCES registry_snapshots(snapshot_id) ON DELETE CASCADE,
    designation_raw TEXT NOT NULL,
    designation_normalized TEXT NOT NULL,
    series TEXT NOT NULL,
    number_part TEXT,
    year INTEGER,
    title_ru_raw TEXT NOT NULL,
    title_ru_normalized TEXT NOT NULL,
    status TEXT,
    ics_codes_json TEXT NOT NULL,
    needs_review INTEGER NOT NULL DEFAULT 0,
    record_hash TEXT NOT NULL,
    source_filename TEXT NOT NULL,
    UNIQUE (snapshot_id, designation_normalized)
);

CREATE INDEX IF NOT EXISTS idx_standards_snapshot_designation
    ON standards_registry (snapshot_id, designation_normalized);

CREATE INDEX IF NOT EXISTS idx_standards_snapshot_title
    ON standards_registry (snapshot_id, title_ru_normalized);

CREATE TABLE IF NOT EXISTS import_rejections (
    rejection_id TEXT PRIMARY KEY,
    snapshot_id TEXT NOT NULL,
    source_filename TEXT NOT NULL,
    record_index INTEGER NOT NULL,
    raw_record_json TEXT NOT NULL,
    error_code TEXT NOT NULL,
    error_message TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS registry_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    active_snapshot_id TEXT REFERENCES registry_snapshots(snapshot_id)
);
"""


def connect(db_path: Path | str) -> sqlite3.Connection:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def get_active_snapshot_id(conn: sqlite3.Connection) -> Optional[str]:
    row = conn.execute(
        "SELECT active_snapshot_id FROM registry_state WHERE id = 1"
    ).fetchone()
    return row["active_snapshot_id"] if row else None


def set_active_snapshot(conn: sqlite3.Connection, snapshot_id: str) -> None:
    """Атомарно переключает активный снимок (раздел 7.2 п.12 ТЗ)."""
    cur = conn.execute("SELECT snapshot_id, status FROM registry_snapshots WHERE snapshot_id = ?", (snapshot_id,))
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"Снимок {snapshot_id} не найден, активация невозможна.")

    prev_active = get_active_snapshot_id(conn)
    conn.execute("UPDATE registry_snapshots SET status = 'active' WHERE snapshot_id = ?", (snapshot_id,))
    if prev_active and prev_active != snapshot_id:
        conn.execute(
            "UPDATE registry_snapshots SET status = 'superseded' WHERE snapshot_id = ?",
            (prev_active,),
        )
    conn.execute("INSERT OR REPLACE INTO registry_state (id, active_snapshot_id) VALUES (1, ?)", (snapshot_id,))
    conn.commit()


def insert_snapshot(
    conn: sqlite3.Connection,
    snapshot_id: str,
    imported_at: str,
    snapshot_date: Optional[str],
    status: str = "staged",
) -> None:
    conn.execute(
        "INSERT INTO registry_snapshots (snapshot_id, imported_at, snapshot_date, status) "
        "VALUES (?, ?, ?, ?)",
        (snapshot_id, imported_at, snapshot_date, status),
    )


def update_snapshot_counters(
    conn: sqlite3.Connection,
    snapshot_id: str,
    records_read: int,
    records_imported: int,
    records_rejected: int,
) -> None:
    conn.execute(
        "UPDATE registry_snapshots SET records_read = ?, records_imported = ?, "
        "records_rejected = ? WHERE snapshot_id = ?",
        (records_read, records_imported, records_rejected, snapshot_id),
    )


def mark_snapshot_failed(conn: sqlite3.Connection, snapshot_id: str) -> None:
    conn.execute(
        "UPDATE registry_snapshots SET status = 'failed' WHERE snapshot_id = ?",
        (snapshot_id,),
    )


def upsert_snapshot_file(
    conn: sqlite3.Connection,
    snapshot_id: str,
    source_filename: str,
    source_sha256: str,
    records_read: int,
    records_imported: int,
    records_rejected: int,
    duplicates: int,
    conflicts: int,
) -> None:
    conn.execute(
        """
        INSERT INTO snapshot_files
            (snapshot_id, source_filename, source_sha256, records_read,
             records_imported, records_rejected, duplicates, conflicts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (snapshot_id, source_filename) DO UPDATE SET
            source_sha256 = excluded.source_sha256,
            records_read = excluded.records_read,
            records_imported = excluded.records_imported,
            records_rejected = excluded.records_rejected,
            duplicates = excluded.duplicates,
            conflicts = excluded.conflicts
        """,
        (
            snapshot_id,
            source_filename,
            source_sha256,
            records_read,
            records_imported,
            records_rejected,
            duplicates,
            conflicts,
        ),
    )


def insert_standard(conn: sqlite3.Connection, record: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO standards_registry
            (standard_id, snapshot_id, designation_raw, designation_normalized,
             series, number_part, year, title_ru_raw, title_ru_normalized,
             status, ics_codes_json, needs_review, record_hash, source_filename)
        VALUES (:standard_id, :snapshot_id, :designation_raw, :designation_normalized,
                :series, :number_part, :year, :title_ru_raw, :title_ru_normalized,
                :status, :ics_codes_json, :needs_review, :record_hash, :source_filename)
        """,
        record,
    )


def find_by_designation_normalized(
    conn: sqlite3.Connection, snapshot_id: str, designation_normalized: str
) -> Optional[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM standards_registry WHERE snapshot_id = ? AND designation_normalized = ?",
        (snapshot_id, designation_normalized),
    ).fetchone()


def get_existing_record_hash(
    conn: sqlite3.Connection, snapshot_id: str, designation_normalized: str
) -> Optional[str]:
    row = conn.execute(
        "SELECT record_hash FROM standards_registry WHERE snapshot_id = ? AND designation_normalized = ?",
        (snapshot_id, designation_normalized),
    ).fetchone()
    return row["record_hash"] if row else None


def insert_rejection(conn: sqlite3.Connection, rejection: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO import_rejections
            (rejection_id, snapshot_id, source_filename, record_index,
             raw_record_json, error_code, error_message)
        VALUES (:rejection_id, :snapshot_id, :source_filename, :record_index,
                :raw_record_json, :error_code, :error_message)
        """,
        rejection,
    )


def all_records_for_snapshot(conn: sqlite3.Connection, snapshot_id: str) -> Iterable[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM standards_registry WHERE snapshot_id = ?", (snapshot_id,)
    ).fetchall()


def get_snapshot_row(conn: sqlite3.Connection, snapshot_id: str) -> Optional[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM registry_snapshots WHERE snapshot_id = ?", (snapshot_id,)
    ).fetchone()


def list_snapshot_files(conn: sqlite3.Connection, snapshot_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM snapshot_files WHERE snapshot_id = ?", (snapshot_id,)
    ).fetchall()


def integrity_check(conn: sqlite3.Connection) -> list[str]:
    """Раздел 7.2 п.10 ТЗ — базовые проверки целостности перед активацией."""
    problems: list[str] = []
    result = conn.execute("PRAGMA foreign_key_check;").fetchall()
    if result:
        problems.append(f"Нарушены внешние ключи: {len(result)} строк.")
    quick = conn.execute("PRAGMA quick_check;").fetchone()
    if quick and quick[0] != "ok":
        problems.append(f"quick_check не пройден: {quick[0]}")
    return problems
