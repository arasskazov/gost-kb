"""Чистые функции нормализации (раздел 5, 9 Шаг 3 ТЗ).

Все функции детерминированные, без обращения к БД и без нечёткого
сравнения. Нечёткое сопоставление реализовано отдельно в service.py
и используется только для формирования кандидатов поиска.
"""
from __future__ import annotations

import re
import unicodedata

from .models import NormalizedDesignation

# Известные префиксы серий в порядке убывания длины/специфичности —
# порядок важен для корректного сопоставления самого длинного префикса
# первым (иначе "ГОСТ" перехватит "ГОСТ Р" и "ГОСТ ISO").
_SERIES_PREFIXES: tuple[str, ...] = (
    "ГОСТ ISO",
    "ГОСТ ИСО",
    "ГОСТ Р",
    "ГОСТ",
    "ПНСТ",
)

_NBSP_CHARS = "\u00a0\u202f\u2007"
_DASH_CHARS = "\u2010\u2011\u2012\u2013\u2014\u2212"  # разные виды дефисов и тире, минус

_NUMBER_YEAR_RE = re.compile(r"^([0-9]+(?:[./][0-9A-Za-zА-Яа-я]+)*)-([0-9]{4})$")


def normalize_whitespace(value: str) -> str:
    """Неразрывные пробелы -> обычные; повтор пробелов -> один; обрезка краёв."""
    if value is None:
        return ""
    s = value
    for ch in _NBSP_CHARS:
        s = s.replace(ch, " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def normalize_dash(value: str) -> str:
    """En dash, em dash и иные варианты тире -> ASCII-дефис '-'."""
    s = value
    for ch in _DASH_CHARS:
        s = s.replace(ch, "-")
    return s


def parse_designation(raw: str) -> NormalizedDesignation:
    """Синтаксический разбор обозначения стандарта (раздел 5.1, 6.2 ТЗ).

    Не отождествляет серии, не угадывает отсутствующие части — при
    невозможности разбора возвращает parsed=False и диагностику, но
    designation_raw никогда не изменяется (хранится вызывающей стороной
    отдельно).
    """
    diagnostics: list[str] = []
    if raw is None or not str(raw).strip():
        return NormalizedDesignation(
            input=raw or "",
            parsed=False,
            diagnostics=["Пустое обозначение."],
        )

    s = normalize_whitespace(str(raw))
    s = normalize_dash(s)

    s_upper = s.upper()

    matched_prefix: str | None = None
    for prefix in _SERIES_PREFIXES:
        if s_upper.startswith(prefix):
            matched_prefix = prefix
            break

    if matched_prefix is None:
        diagnostics.append(
            "Серия не распознана среди известных префиксов "
            f"({', '.join(_SERIES_PREFIXES)}); запись помечена как OTHER."
        )
        # Пытаемся разобрать хотя бы номер/год из хвоста строки, но серию
        # не угадываем.
        remainder = s
        series_canonical = "OTHER"
        designation_normalized = s_upper
    else:
        remainder = s[len(matched_prefix):].lstrip()
        series_canonical = matched_prefix
        designation_normalized = f"{series_canonical} {remainder}".strip()

    number_part: str | None = None
    year: int | None = None
    m = _NUMBER_YEAR_RE.match(remainder.strip())
    if m:
        number_part = m.group(1)
        year = int(m.group(2))
        parsed = matched_prefix is not None
    else:
        parsed = False
        diagnostics.append(
            "Не удалось выделить номер и год по шаблону 'номер-ГГГГ' из "
            f"остатка обозначения: '{remainder}'."
        )

    return NormalizedDesignation(
        input=raw,
        designation_normalized=designation_normalized if designation_normalized else None,
        series=series_canonical,
        number_part=number_part,
        year=year,
        parsed=parsed,
        diagnostics=diagnostics,
    )


def normalize_title(value: str) -> str:
    """Производная форма заглавия для технического сравнения (раздел 5.3).

    Разрешено: NFC, замена NBSP, свёртка пробелов, унификация тире,
    приведение к нижнему регистру. Запрещено удалять слова, номера
    частей и скобочные уточнения — эта функция не удаляет ничего,
    кроме пробельного шума, и не переставляет фразы.
    """
    if value is None:
        return ""
    s = unicodedata.normalize("NFC", value)
    s = normalize_whitespace(s)
    s = normalize_dash(s)
    return s.lower()


def parse_ics_codes(value: str | None) -> list[str]:
    """Разбор поля 'Код ОКС' по разделителю ';' (раздел 5.4 ТЗ)."""
    if not value:
        return []
    parts = [p.strip() for p in str(value).split(";")]
    return [p for p in parts if p]
