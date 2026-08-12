"""MCP-сервер только для чтения (раздел 3.3, 6, 9 Шаг 7 ТЗ).

Публикует ровно пять инструментов согласно контракту раздела 6 ТЗ:
normalize_designation, resolve_standard, verify_reference,
search_standards, get_registry_provenance. Инструментов изменения,
удаления или произвольного SQL-доступа нет и не может быть добавлено
без пересмотра ТЗ.

Транспорт по умолчанию — stdio (обязателен для MVP, раздел 3.3 ТЗ).
Сетевые транспорты (streamable-http) поддержаны SDK, но по умолчанию
не публикуются наружу — см. README, раздел «Развёртывание».

Зависимость зафиксирована как `mcp>=1.2.0,<2.0.0` (см. pyproject.toml):
mcp 2.0.0 переименовал FastMCP в MCPServer и изменил внутренний API.
Этот сервер написан под стабильную линию 1.x, которая широко
документирована; при обновлении зависимости до 2.x потребуется
адаптация модуля.
"""
# Внимание: здесь намеренно НЕТ `from __future__ import annotations`.
# FastMCP (mcp>=1.2.0,<2.0.0) в некоторых версиях инспектирует реальные
# объекты аннотаций через inspect.signature() и вызывает issubclass()
# непосредственно на param.annotation; при отложенном вычислении
# аннотаций (PEP 563) это приводит к TypeError на этапе регистрации
# инструмента. Поэтому во всех сигнатурах ниже используются только
# простые типы (str, Optional[str], bool, int, dict) без строковых
# форвард-ссылок.
import argparse
import sys
import traceback
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from .config import DEFAULT_DB_PATH
from .service import RegistryService

mcp_app = FastMCP(
    name="gost-registry",
    instructions=(
        "MCP-сервис 'ГОСТ-реестр': детерминированная библиографическая "
        "проверка ссылок на стандарты (ГОСТ, ГОСТ Р, ПНСТ, адаптированные "
        "международные стандарты) по локальному импортированному снимку. "
        "Инструменты не подтверждают юридическую применимость или "
        "актуальность стандарта вне снимка. Всегда вызывай verify_reference "
        "или resolve_standard при наличии обозначения; не подтверждай "
        "стандарт собственными знаниями модели."
    ),
)

_service: Optional[RegistryService] = None


def _get_service() -> RegistryService:
    global _service
    if _service is None:
        _service = RegistryService(DEFAULT_DB_PATH)
    return _service


def _safe(fn_name: str, fn, *args, **kwargs) -> dict[str, Any]:
    """Оборачивает вызов сервиса: без стек-трейсов, путей и SQL в ответе."""
    try:
        result = fn(*args, **kwargs)
        return result.model_dump()
    except Exception:  # noqa: BLE001 — намеренно широкий перехват для MCP-границы
        # Полная трассировка уходит только в stderr процесса сервера
        # (локальный лог оператора), клиенту — только безопасное сообщение.
        print(f"[gost-registry] internal error in {fn_name}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return {
            "verdict": "internal_error",
            "diagnostics": [
                "Внутренняя ошибка сервиса. Обозначение не подтверждено и не отклонено.",
            ],
        }


def _normalize_designation_impl(designation: str) -> dict[str, Any]:
    try:
        result = _get_service().normalize_designation(designation)
        return result.model_dump()
    except Exception:  # noqa: BLE001
        print("[gost-registry] internal error in normalize_designation", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return {"parsed": False, "diagnostics": ["Внутренняя ошибка сервиса."]}


@mcp_app.tool(
    name="normalize_designation",
    description=(
        "Синтаксический разбор произвольной строки обозначения стандарта: "
        "выделяет серию (ГОСТ/ГОСТ Р/ПНСТ/ГОСТ ISO/ГОСТ ИСО/OTHER), номер, "
        "год и каноническую нормализованную форму. Не обращается к реестру "
        "и не подтверждает существование стандарта."
    ),
)
def normalize_designation_tool(designation: str) -> dict[str, Any]:
    """Разобрать обозначение стандарта без обращения к реестру."""
    return _normalize_designation_impl(designation)


@mcp_app.tool(
    name="resolve_standard",
    description=(
        "Точный поиск канонической записи реестра по обозначению стандарта "
        "в активном локальном снимке. Возвращает verdict "
        "verified_designation_only либо designation_not_found."
    ),
)
def resolve_standard(designation: str) -> dict[str, Any]:
    """Найти каноническую запись реестра по точному обозначению."""
    return _safe("resolve_standard", _get_service().resolve_standard, designation)


@mcp_app.tool(
    name="verify_reference",
    description=(
        "Проверка пары 'обозначение + (опционально) заглавие' против "
        "активного локального снимка реестра. verdict: verified, "
        "verified_designation_only, title_mismatch, designation_not_found, "
        "ambiguous, invalid_input. Не отождествляет ГОСТ/ГОСТ Р, "
        "ГОСТ ISO/ГОСТ ИСО, разные годы и части."
    ),
)
def verify_reference(
    designation: str,
    title_ru: Optional[str] = None,
    require_active_status: bool = False,
) -> dict[str, Any]:
    """Проверить ссылку на стандарт по обозначению и опциональному заглавию."""
    return _safe(
        "verify_reference",
        _get_service().verify_reference,
        designation,
        title_ru,
        require_active_status,
    )


@mcp_app.tool(
    name="search_standards",
    description=(
        "Поиск кандидатов по фрагменту заглавия, серии, префиксу кода ОКС "
        "и/или статусу в активном снимке реестра. Результат — только "
        "кандидаты (exact/prefix/token/fuzzy), не является подтверждением "
        "ссылки. Для подтверждения используйте verify_reference."
    ),
)
def search_standards(
    query: Optional[str] = None,
    series: Optional[str] = None,
    ics_code_prefix: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Найти кандидатов по фрагменту заглавия и/или фильтрам."""
    return _safe(
        "search_standards",
        _get_service().search_standards,
        query,
        series,
        ics_code_prefix,
        status,
        limit,
    )


@mcp_app.tool(
    name="get_registry_provenance",
    description=(
        "Возвращает происхождение активного снимка реестра: дату импорта, "
        "список файлов-снимков с контрольными суммами, число импортированных "
        "и отклонённых записей, а также обязательную формулировку "
        "ограничения достоверности данных."
    ),
)
def get_registry_provenance() -> dict[str, Any]:
    """Получить происхождение и ограничения активного снимка реестра."""
    return _safe("get_registry_provenance", _get_service().get_registry_provenance)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m gost_registry.mcp_server",
        description="MCP-сервер только для чтения реестра стандартов ГОСТ/ГОСТ Р/ПНСТ.",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Транспорт MCP. Для MVP обязателен stdio (раздел 3.3 ТЗ).",
    )
    parser.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH), help="Путь к файлу SQLite реестра.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Хост для сетевых транспортов.")
    parser.add_argument("--port", type=int, default=8080, help="Порт для сетевых транспортов.")
    return parser


def main(argv: list[str] | None = None) -> int:
    global _service
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    _service = RegistryService(args.db)

    if args.transport in ("sse", "streamable-http"):
        mcp_app.settings.host = args.host
        mcp_app.settings.port = args.port
        print(
            f"[gost-registry] Внимание: сетевой транспорт '{args.transport}' на "
            f"{args.host}:{args.port}. Публикуйте только за reverse proxy с TLS "
            "и аутентификацией (раздел 10.2 ТЗ).",
            file=sys.stderr,
        )

    mcp_app.run(transport=args.transport)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
