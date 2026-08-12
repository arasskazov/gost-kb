# Развёртывание

Установка и запуск MCP-сервиса «ГОСТ-реестр» на локальной машине под
Pop!_OS без Docker. Соответствует разделу 10 ТЗ («Развёртывание»),
раздел 10.1 (локальный режим); раздел 10.2 ТЗ (контейнерный режим) не
применяется по решению пользователя — используется только локальный
процесс Python.

## 1. Системные требования

- Python 3.10 или новее. В Pop!_OS 22.04 системный `python3` — 3.10; в
  Pop!_OS 24.04 — 3.12. Обоих достаточно.
- Модуль `venv` и `pip`:

  ```bash
  sudo apt update
  sudo apt install -y python3-venv python3-pip
  ```

- Docker не требуется и не используется ни на одном этапе.

## 2. Установка пакета

```bash
cd ~/gost-registry-mcp        # каталог, куда распакован проект
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

Зависимость MCP SDK зафиксирована в `pyproject.toml` как
`mcp>=1.2.0,<2.0.0`. Это осознанное ограничение, а не случайность:
ветка `mcp` 2.0.0 переименовала класс `FastMCP` в `MCPServer` и
изменила внутренний API инспекции инструментов. `mcp_server.py`
написан и проверен под стабильную линию 1.x. Если верхняя граница
версии будет снята и `pip` установит 2.x — сервер не запустится без
адаптации кода; это не баг ТЗ, а требование к обновлению зависимости.

## 3. Проверка до первого запуска (тесты)

```bash
python -m pytest -q
```

Ожидаемый результат: все тесты пройдены (37/37 на момент сдачи —
нормализация обозначений, импорт, конфликты/дубли, репозиторий,
доменная логика всех пяти MCP-инструментов). Прогоняйте тесты после
любого изменения кода и перед переимпортом данных в продуктивную базу.

## 4. Запуск MCP-сервера

### 4.1. Локальный запуск по требованию (stdio) — основной режим

```bash
source .venv/bin/activate
python -m gost_registry.mcp_server --transport stdio --db ./data/gost_registry.sqlite
```

Для большинства MCP-клиентов (в том числе Qwen Code) процесс не нужно
запускать вручную — клиент сам стартует и завершает его по конфигурации
из `mcpServers` (см. раздел 5 ниже и `docs/USAGE.md`).

### 4.2. Автозапуск как пользовательская служба (опционально, без Docker)

Если требуется постоянно работающий процесс (например, для сетевого
транспорта из п. 4.3), можно завести юнит `systemd --user` — это
обычный процесс Linux, не контейнер:

```ini
# ~/.config/systemd/user/gost-registry-mcp.service
[Unit]
Description=MCP gost-registry (stdio)

[Service]
Type=simple
ExecStart=/home/%u/gost-registry-mcp/.venv/bin/python -m gost_registry.mcp_server --transport stdio --db /home/%u/gost-registry-mcp/data/gost_registry.sqlite
Restart=on-failure

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now gost-registry-mcp.service
```

### 4.3. Сетевой транспорт (опционально, без Docker)

```bash
python -m gost_registry.mcp_server \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8080 \
  --db ./data/gost_registry.sqlite
```

Публикуйте порт только на `127.0.0.1`, либо разместите за отдельным
reverse proxy с TLS и аутентификацией, устанавливаемым обычным пакетом
(`nginx`, `caddy` через `apt`) — без Docker. Сам сервис аутентификацию
не реализует (раздел 3.3 ТЗ: MCP-сервер только читает данные, не
предоставляет инструментов изменения).

## 5. Подключение к Qwen Code

Факт, подтверждённый документацией Qwen Code: конфигурация MCP-серверов
хранится в `mcpServers` внутри `settings.json` — пользовательский
масштаб `~/.qwen/settings.json` (действует во всех проектах) либо
проектный `.qwen/settings.json` (только в текущем проекте). Формат
полей (`command`, `args`, `env`, `cwd`, `timeout`, `trust`) совпадает с
тем, что уже использовался в исходном README — код сервиса не требует
изменений для совместимости с Qwen Code. [Qwen Code Docs — Connect Qwen Code to tools via MCP](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/)

### 5.1. Вариант A — редактирование `settings.json` напрямую

```bash
mkdir -p ~/.qwen
```

Добавьте в `~/.qwen/settings.json` (пользовательский масштаб) или в
`.qwen/settings.json` в корне вашего рабочего проекта (проектный
масштаб — приоритетнее, если нужно ограничить сервис одним проектом):

```json
{
  "mcpServers": {
    "gost-registry": {
      "command": "/home/<user>/gost-registry-mcp/.venv/bin/python",
      "args": [
        "-m",
        "gost_registry.mcp_server",
        "--transport",
        "stdio",
        "--db",
        "/home/<user>/gost-registry-mcp/data/gost_registry.sqlite"
      ],
      "timeout": 15000,
      "trust": false
    }
  }
}
```

Замените `<user>` и пути на реальные для вашей машины. `trust: false`
оставлен намеренно — сервис не изменяет данные, но пусть подтверждение
вызовов инструментов остаётся под вашим контролем; при желании можно
поставить `true`, чтобы не подтверждать каждый вызов (сервис не
предоставляет опасных операций — все пять инструментов только читают).

### 5.2. Вариант B — через команду `qwen mcp add`

```bash
qwen mcp add --scope user gost-registry \
  /home/<user>/gost-registry-mcp/.venv/bin/python \
  -- -m gost_registry.mcp_server --transport stdio --db /home/<user>/gost-registry-mcp/data/gost_registry.sqlite
```

Команда создаёт ту же запись в `mcpServers`, что и ручное редактирование
из 5.1. Используйте `--scope project`, если конфигурация должна
действовать только в текущем рабочем каталоге.

### 5.3. Проверка подключения

1. Если Qwen Code уже был запущен — перезапустите его в том же проекте
   (сервер MCP подхватывается при старте сессии).
2. Откройте диалог управления MCP-серверами внутри `qwen` (команда
   `/mcp` в интерактивном режиме, либо через меню MCP) и убедитесь, что
   `gost-registry` в статусе подключён, со списком пяти инструментов:
   `normalize_designation`, `resolve_standard`, `verify_reference`,
   `search_standards`, `get_registry_provenance`.
3. Попросите модель проверить конкретное обозначение (например,
   «проверь через gost-registry ГОСТ Р 2.101-2023») — это должно
   вызвать `verify_reference`, а не внутренние знания модели (см.
   промпт субагента в `docs/USAGE.md`).

## 6. Ручная проверка живого протокола (без клиента)

```bash
python tests/manual_stdio_client_check.py .venv/bin/python ./data/gost_registry.sqlite
```

Скрипт поднимает настоящего MCP stdio-клиента (из того же SDK) и
вызывает все пять инструментов на активном снимке — используется как
разовая проверка перед первым подключением клиента, не входит в
автоматический набор `pytest`.

## 7. Известные ограничения этого раздела

- Проверено вживую только с эталонным `stdio_client` из MCP Python SDK
  (см. п. 6). Поведение конкретно внутри Qwen Code при первом
  подключении не проверялось средствами данной сдачи — раздел 5
  составлен по официальной документации Qwen Code, а не по факту
  запуска в этом продукте.
- Сетевой транспорт (`streamable-http`, п. 4.3) не нагружался и не
  тестировался на данной сдаче.
