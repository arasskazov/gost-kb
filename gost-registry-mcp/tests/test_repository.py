from pathlib import Path

from gost_registry.importer import run_import

FIXTURES = Path(__file__).parent / "fixtures"


def _prepare_db(tmp_path: Path):
    incoming = tmp_path / "incoming"
    incoming.mkdir()
    for name in ("gost_sample.json", "gost_r_sample.json"):
        (incoming / name).write_text((FIXTURES / name).read_text(encoding="utf-8"), encoding="utf-8")
    db_path = tmp_path / "registry.sqlite"
    run_import(
        input_dir=incoming,
        db_path=db_path,
        snapshot_date="2026-08-11",
        activate=True,
        allow_conflicts=False,
        report_path=tmp_path / "report.json",
    )
    return db_path


def test_no_active_snapshot_before_any_import(tmp_path):
    from gost_registry import repository as repo

    db_path = tmp_path / "empty.sqlite"
    conn = repo.connect(db_path)
    repo.init_schema(conn)
    assert repo.get_active_snapshot_id(conn) is None


def test_switching_active_snapshot_supersedes_previous(tmp_path):
    from gost_registry import repository as repo

    db_path = _prepare_db(tmp_path)
    conn = repo.connect(db_path)
    first_active = repo.get_active_snapshot_id(conn)
    assert first_active is not None

    # Второй импорт того же набора создаёт новый снимок и должен
    # переключить активный снимок, переведя первый в 'superseded'.
    incoming2 = tmp_path / "incoming2"
    incoming2.mkdir()
    for name in ("gost_sample.json", "gost_r_sample.json"):
        (incoming2 / name).write_text((FIXTURES / name).read_text(encoding="utf-8"), encoding="utf-8")

    report2 = run_import(
        input_dir=incoming2,
        db_path=db_path,
        snapshot_date="2026-08-12",
        activate=True,
        allow_conflicts=False,
        report_path=tmp_path / "report2.json",
    )

    conn2 = repo.connect(db_path)
    assert repo.get_active_snapshot_id(conn2) == report2.snapshot_id
    prev_row = repo.get_snapshot_row(conn2, first_active)
    assert prev_row["status"] == "superseded"


def test_integrity_check_passes_on_clean_db(tmp_path):
    from gost_registry import repository as repo

    db_path = _prepare_db(tmp_path)
    conn = repo.connect(db_path)
    assert repo.integrity_check(conn) == []
