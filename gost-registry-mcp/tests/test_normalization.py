from gost_registry.normalization import (
    normalize_dash,
    normalize_title,
    normalize_whitespace,
    parse_designation,
    parse_ics_codes,
)


def test_normalize_whitespace_collapses_and_strips():
    assert normalize_whitespace("  ГОСТ   Р  2.101-2023  ") == "ГОСТ Р 2.101-2023"


def test_normalize_whitespace_nbsp():
    assert normalize_whitespace("ГОСТ\u00a0Р\u00a02.101-2023") == "ГОСТ Р 2.101-2023"


def test_normalize_dash_en_dash_to_ascii():
    assert normalize_dash("2.101\u20132023") == "2.101-2023"


def test_parse_designation_lowercase_and_en_dash():
    result = parse_designation("гост р 2.101\u20132023")
    assert result.parsed is True
    assert result.designation_normalized == "ГОСТ Р 2.101-2023"
    assert result.series == "ГОСТ Р"
    assert result.number_part == "2.101"
    assert result.year == 2023


def test_parse_designation_missing_space_after_series():
    result = parse_designation("ГОСТ Р2.101-2023")
    assert result.parsed is True
    assert result.designation_normalized == "ГОСТ Р 2.101-2023"


def test_parse_designation_padded():
    result = parse_designation(" ГОСТ 2.103-2013 ")
    assert result.designation_normalized == "ГОСТ 2.103-2013"
    assert result.series == "ГОСТ"


def test_parse_designation_distinguishes_gost_and_gost_r():
    a = parse_designation("ГОСТ 2.101-2023")
    b = parse_designation("ГОСТ Р 2.101-2023")
    assert a.series == "ГОСТ"
    assert b.series == "ГОСТ Р"
    assert a.designation_normalized != b.designation_normalized


def test_parse_designation_distinguishes_iso_and_iso_cyrillic():
    a = parse_designation("ГОСТ ISO 9001-2011")
    b = parse_designation("ГОСТ ИСО 9001-2011")
    assert a.series == "ГОСТ ISO"
    assert b.series == "ГОСТ ИСО"
    assert a.designation_normalized != b.designation_normalized


def test_parse_designation_unknown_series_marked_other():
    result = parse_designation("СТО 12345-2020")
    assert result.series == "OTHER"
    assert result.diagnostics


def test_parse_designation_empty_input():
    result = parse_designation("")
    assert result.parsed is False
    assert result.diagnostics


def test_normalize_title_lowercases_and_collapses_spaces():
    assert normalize_title("  Единая  система   КД  ") == "единая система кд"


def test_normalize_title_preserves_words_and_parenthesis():
    title = "Единая система конструкторской документации. Виды изделий (уточнение)"
    normalized = normalize_title(title)
    assert "виды изделий" in normalized
    assert "(уточнение)" in normalized


def test_parse_ics_multiple_codes():
    assert parse_ics_codes("01.110; 35.240.30") == ["01.110", "35.240.30"]


def test_parse_ics_single_code():
    assert parse_ics_codes("01.110") == ["01.110"]


def test_parse_ics_empty():
    assert parse_ics_codes(None) == []
    assert parse_ics_codes("") == []
