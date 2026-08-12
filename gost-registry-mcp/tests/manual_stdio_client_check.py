"""Ручная проверка живого stdio MCP-сервера настоящим клиентом MCP SDK.

Не входит в основной набор pytest (требует поднятия дочернего процесса
сервера) — используется как разовая проверка протокола перед сдачей.
Запуск: python tests/manual_stdio_client_check.py <путь_к_python> <путь_к_db>
"""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main(python_exe: str, db_path: str) -> None:
    params = StdioServerParameters(
        command=python_exe,
        args=["-m", "gost_registry.mcp_server", "--transport", "stdio", "--db", db_path],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("TOOLS:", [t.name for t in tools.tools])

            r1 = await session.call_tool("verify_reference", {"designation": "ГОСТ Р 2.101-2023"})
            print("verify_reference(exists) ->", r1.content[0].text)

            r2 = await session.call_tool(
                "verify_reference",
                {"designation": "ГОСТ Р 2.101-2023", "title_ru": "Заведомо неверное заглавие"},
            )
            print("verify_reference(mismatch) ->", r2.content[0].text)

            r3 = await session.call_tool("verify_reference", {"designation": "ГОСТ Р 99.999-2099"})
            print("verify_reference(not found) ->", r3.content[0].text)

            r4 = await session.call_tool("get_registry_provenance", {})
            print("get_registry_provenance ->", r4.content[0].text[:300])

            r5 = await session.call_tool("normalize_designation", {"designation": "гост р2.101–2023"})
            print("normalize_designation ->", r5.content[0].text)

            r6 = await session.call_tool("search_standards", {"query": "конструкторской документации", "limit": 3})
            print("search_standards ->", r6.content[0].text[:400])


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
