"""Тесты доменного сервиса, лежащего в основе MCP-инструментов (раздел 9 Шаг 8 ТЗ).

Тестируется gost_registry.service.RegistryService напрямую — это тот же
код, который вызывают обёртки в mcp_server.py; такой подход проверяет
бизнес-логику без необходимости подниматься по stdio-транспорту.
"""
from pathlib import Path

import pytest

from gost_registry.importer import run_import
from gost_registry.service import RegistryService

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def service(tmp_path):
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
    svc = RegistryService(db_path)
    yield svc
    svc.close()


def test_resolve_standard_exact_gost_2_103(service):
    result = service.resolve_standard("ГОСТ 2.103-2013")
    assert result.verdict == "verified_designation_only"
    assert result.canonical["designation_normalized"] == "ГОСТ 2.103-2013"


def test_resolve_standard_exact_gost_r_2_101(service):
    result = service.resolve_standard("ГОСТ Р 2.101-2023")
    assert result.verdict == "verified_designation_only"
    assert result.canonical["title_ru"] == "Единая система конструкторской документации. Виды изделий"


def test_verify_reference_verified_when_title_matches(service):
    result = service.verify_reference(
        "ГОСТ Р 2.101-2023",
        "Единая система конструкторской документации. Виды изделий",
    )
    assert result.verdict == "verified"
    assert result.confidence == 1.0


def test_verify_reference_title_mismatch(service):
    result = service.verify_reference(
        "ГОСТ Р 2.101-2023",
        "Единая система конструкторской документации. Стадии разработки",
    )
    assert result.verdict == "title_mismatch"
    assert result.canonical["title_ru"] == "Единая система конструкторской документации. Виды изделий"


def test_verify_reference_designation_not_found(service):
    result = service.verify_reference("ГОСТ Р 99.999-2099")
    assert result.verdict == "designation_not_found"
    assert any("снимк" in d for d in result.diagnostics)


def test_verify_reference_distinguishes_gost_and_gost_r(service):
    # ГОСТ 2.101-2023 не импортирован (только ГОСТ Р 2.101-2023 есть в наборе)
    result = service.verify_reference("ГОСТ 2.101-2023")
    assert result.verdict == "designation_not_found"


def test_verify_reference_distinguishes_iso_and_iso_cyrillic(service):
    iso = service.verify_reference("ГОСТ ISO 9001-2011")
    iso_cyr = service.verify_reference("ГОСТ ИСО 9001-2011")
    assert iso.verdict == "verified_designation_only"
    assert iso_cyr.verdict == "verified_designation_only"
    assert iso.canonical["standard_id"] != iso_cyr.canonical["standard_id"]


def test_search_standards_returns_candidates_by_title_fragment(service):
    result = service.search_standards(query="конструкторской документации")
    assert result.verdict == "candidates_found"
    assert len(result.candidates) >= 2
    for c in result.candidates:
        assert c.match_type in ("exact", "prefix", "token", "fuzzy")


def test_search_standards_filters_by_ics_prefix(service):
    result = service.search_standards(ics_code_prefix="01.110")
    assert result.verdict == "candidates_found"
    assert all("01.110" in "".join(c.ics_codes) for c in result.candidates)


def test_search_standards_no_candidates_returns_diagnostics(service):
    result = service.search_standards(query="совершенно несуществующая тема запроса")
    assert result.verdict == "no_candidates"
    assert result.diagnostics


def test_get_registry_provenance_contains_limitation_text(service):
    prov = service.get_registry_provenance()
    assert prov.active_snapshot_id is not None
    assert "не подтверждает" in prov.limitation
    assert prov.total_records_imported == 6


def test_normalize_designation_tool_level(service):
    result = service.normalize_designation("гост р2.101–2023")
    assert result.designation_normalized == "ГОСТ Р 2.101-2023"
    assert result.year == 2023


def test_verify_reference_empty_designation_is_invalid_input(service):
    result = service.verify_reference("")
    assert result.verdict == "invalid_input"
