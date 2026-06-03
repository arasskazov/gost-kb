#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOST RAG Pipeline — локальный CLI-режим
=======================================
Запуск на чистой машине (только python + pip):
    python GOST_RAG_Pipeline.py

Переменные окружения (можно задать в .env или в системе):
    GOST_KB_URL        URL репозитория с документами (raw GitHub)
    CHROMA_PATH        Путь к папке ChromaDB (локальный кэш индекса)
    LLM_PROVIDER       Провайдер LLM: deepseek | qwen | openai  (default: deepseek)
    LLM_API_KEY        API-ключ выбранного провайдера
    LLM_MODEL          Имя модели (default: deepseek-chat / qwen-plus)
    LLM_API_BASE       API base URL (опционально, по умолчанию — стандартный для провайдера)
    EMBED_MODEL        HuggingFace модель эмбеддингов (default: intfloat/multilingual-e5-large)

Пример .env:
    GOST_KB_URL=https://raw.githubusercontent.com/arasskazov/gost-kb/main
    CHROMA_PATH=/var/data/gost-chroma
    LLM_PROVIDER=deepseek
    LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
    LLM_MODEL=deepseek-chat
"""

from __future__ import annotations

import os
import re
import sys
import subprocess
import importlib
import textwrap
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Шаг 1 — Проверка и авто-установка зависимостей
# ─────────────────────────────────────────────────────────────────────────────

REQUIRED_PACKAGES = {
    "llama_index": "llama-index",
    "llama_index.vector_stores.chroma": "llama-index-vector-stores-chroma",
    "llama_index.embeddings.huggingface": "llama-index-embeddings-huggingface",
    "llama_index.llms.openai_like": "llama-index-llms-openai-like",
    "chromadb": "chromadb",
    "sentence_transformers": "sentence-transformers",
    "openai": "openai",
    "requests": "requests",
    "dotenv": "python-dotenv",
}


def _pip_install(package: str) -> None:
    print(f"  📦 Устанавливаю {package} ...", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", package],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ❌ Ошибка установки {package}:\n{result.stderr.strip()}")
        sys.exit(1)


def ensure_dependencies() -> None:
    missing = []
    for module, pip_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append((module, pip_name))

    if not missing:
        print("✅ Все зависимости установлены")
        return

    print(f"⚙️  Не найдено пакетов: {[p for _, p in missing]}")
    print("   Устанавливаю...")
    for _, pip_name in missing:
        _pip_install(pip_name)
    print("✅ Зависимости установлены\n")


# Вызываем ДО любых import из этих пакетов
ensure_dependencies()

# ─────────────────────────────────────────────────────────────────────────────
# Шаг 2 — Загрузка конфигурации из .env / переменных окружения
# ─────────────────────────────────────────────────────────────────────────────

from dotenv import load_dotenv  # noqa: E402 — после ensure_dependencies

load_dotenv()  # читает .env из текущей директории, если существует


# ── Конфигурация репозитория ──────────────────────────────────────────────────
GOST_KB_URL: str = os.environ.get(
    "GOST_KB_URL",
    "https://raw.githubusercontent.com/arasskazov/gost-kb/main"
).rstrip("/")

# ── Конфигурация векторной базы ───────────────────────────────────────────────
CHROMA_PATH: str = os.environ.get(
    "CHROMA_PATH",
    str(Path.home() / ".cache" / "gost-kb" / "chroma")
)
CHROMA_COLLECTION: str = "gost_standards"

# ── Конфигурация модели эмбеддингов ───────────────────────────────────────────
EMBED_MODEL_NAME: str = os.environ.get(
    "EMBED_MODEL",
    "intfloat/multilingual-e5-large"
)

# ── Конфигурация LLM ─────────────────────────────────────────────────────────
LLM_PROVIDER_DEFAULTS = {
    "deepseek": {
        "api_base": "https://api.deepseek.com",
        "model":    "deepseek-chat",
    },
    "qwen": {
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model":    "qwen-plus",
    },
    "openai": {
        "api_base": "https://api.openai.com/v1",
        "model":    "gpt-4o-mini",
    },
}

LLM_PROVIDER: str = os.environ.get("LLM_PROVIDER", "deepseek").lower()
LLM_API_KEY:  Optional[str] = os.environ.get("LLM_API_KEY")
LLM_MODEL:    str = os.environ.get(
    "LLM_MODEL",
    LLM_PROVIDER_DEFAULTS.get(LLM_PROVIDER, {}).get("model", "deepseek-chat")
)
LLM_API_BASE: str = os.environ.get(
    "LLM_API_BASE",
    LLM_PROVIDER_DEFAULTS.get(LLM_PROVIDER, {}).get("api_base", "https://api.deepseek.com")
)

SYSTEM_PROMPT = textwrap.dedent("""
    Ты — эксперт-нормировщик по стандартам серии ГОСТ Р 77.*
    (управление жизненным циклом изделий).

    Правила:
    1. Отвечай ТОЛЬКО на основе предоставленных фрагментов стандартов.
    2. Всегда указывай номер ГОСТ и раздел/пункт (например: ГОСТ Р 77.001, п. 3.4).
    3. Если информация в предоставленных фрагментах отсутствует — так и скажи,
       не придумывай нормы.
    4. При противоречиях между стандартами — укажи оба варианта с источниками.
    5. Используй точные формулировки из текста стандарта.
""").strip()


# ─────────────────────────────────────────────────────────────────────────────
# Шаг 3 — Проверка окружения
# ─────────────────────────────────────────────────────────────────────────────

def check_environment() -> bool:
    """Проверяет наличие обязательных переменных и доступность сервисов."""
    import requests as req

    ok = True

    print("\n🔍 Проверка окружения...")

    # Проверка API-ключа
    if not LLM_API_KEY:
        print(f"  ❌ LLM_API_KEY не задан (провайдер: {LLM_PROVIDER})")
        print(f"     Задайте переменную окружения или создайте .env:")
        print(f"       LLM_PROVIDER={LLM_PROVIDER}")
        print(f"       LLM_API_KEY=ваш_ключ")
        ok = False
    else:
        print(f"  ✅ LLM_API_KEY задан ({LLM_PROVIDER} / {LLM_MODEL})")

    # Проверка доступности репозитория
    try:
        r = req.get(f"{GOST_KB_URL}/INDEX.md", timeout=10)
        if r.status_code == 200:
            print(f"  ✅ Репозиторий доступен: {GOST_KB_URL}")
        else:
            print(f"  ❌ Репозиторий вернул статус {r.status_code}: {GOST_KB_URL}")
            ok = False
    except Exception as e:
        print(f"  ❌ Репозиторий недоступен: {e}")
        ok = False

    # Проверка пути ChromaDB
    chroma_dir = Path(CHROMA_PATH)
    try:
        chroma_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ ChromaDB путь: {CHROMA_PATH}")
    except Exception as e:
        print(f"  ❌ Не могу создать ChromaDB директорию {CHROMA_PATH}: {e}")
        ok = False

    return ok


# ─────────────────────────────────────────────────────────────────────────────
# Шаг 4 — Загрузка документов из репозитория
# ─────────────────────────────────────────────────────────────────────────────

def load_documents() -> list:
    """Динамически загружает все full.md + summary.md через INDEX.md."""
    import requests as req
    from llama_index.core import Document

    print("\n📥 Загрузка документов из репозитория...")
    idx_resp = req.get(f"{GOST_KB_URL}/INDEX.md", timeout=15)
    idx_resp.raise_for_status()

    full_md_paths = re.findall(r"\(standards/[^)]+/full\.md\)", idx_resp.text)
    full_md_paths = [p.strip("()") for p in full_md_paths]
    print(f"   Найдено стандартов в INDEX.md: {len(full_md_paths)}")

    documents: list[Document] = []
    failed: list[str] = []

    for rel_path in full_md_paths:
        parts = rel_path.split("/")
        domain = parts[1] if len(parts) >= 4 else "unknown"
        std_id = parts[2] if len(parts) >= 4 else rel_path

        url_full = f"{GOST_KB_URL}/{rel_path}"
        r = req.get(url_full, timeout=15)
        if r.status_code == 200 and len(r.text) > 100:
            documents.append(Document(
                text=r.text,
                metadata={"standard": std_id, "domain": domain,
                          "source": url_full, "type": "full"}
            ))
            print(f"   ✅ {domain}/{std_id}: {len(r.text):,} символов")
        else:
            failed.append(rel_path)
            print(f"   ❌ {rel_path}: статус {r.status_code}")

        url_sum = url_full.replace("/full.md", "/summary.md")
        r2 = req.get(url_sum, timeout=15)
        if r2.status_code == 200 and len(r2.text) > 50:
            documents.append(Document(
                text=r2.text,
                metadata={"standard": std_id, "domain": domain,
                          "source": url_sum, "type": "summary"}
            ))

    print(f"\n   Итого загружено: {len(documents)} документов")
    if failed:
        print(f"   ⚠️  Не загружены: {failed}")
    return documents


# ─────────────────────────────────────────────────────────────────────────────
# Шаг 5 — Построение / восстановление векторного индекса
# ─────────────────────────────────────────────────────────────────────────────

def build_index(documents: list):
    """Строит индекс ChromaDB или восстанавливает из кэша."""
    import chromadb
    from llama_index.core import VectorStoreIndex, StorageContext, Settings
    from llama_index.core.node_parser import MarkdownNodeParser
    from llama_index.vector_stores.chroma import ChromaVectorStore
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    print("\n🔄 Загружаем модель эмбеддингов...")
    embed_model = HuggingFaceEmbedding(
        model_name=EMBED_MODEL_NAME,
        query_instruction="query: ",
        text_instruction="passage: ",
        max_length=512,
    )
    Settings.embed_model = embed_model
    Settings.node_parser = MarkdownNodeParser()
    print(f"   ✅ Модель: {EMBED_MODEL_NAME}")

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = chroma_client.get_or_create_collection(
        CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    existing = chroma_collection.count()
    if existing > 0:
        print(f"   ✅ Индекс восстановлен из кэша ({CHROMA_PATH}): {existing} чанков")
        return VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context
        )

    print(f"   🔄 Индексируем {len(documents)} документов (первый запуск ~5-8 мин)...")
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True
    )
    print(f"   ✅ Индекс построен: {chroma_collection.count()} чанков → {CHROMA_PATH}")
    return index


# ─────────────────────────────────────────────────────────────────────────────
# Шаг 6 — Инициализация LLM (мультипровайдерная)
# ─────────────────────────────────────────────────────────────────────────────

def build_llm():
    """Создаёт LLM-клиент для выбранного провайдера."""
    from llama_index.llms.openai_like import OpenAILike

    print(f"\n🤖 Инициализация LLM: {LLM_PROVIDER} / {LLM_MODEL}")
    print(f"   API base: {LLM_API_BASE}")

    llm = OpenAILike(
        model=LLM_MODEL,
        api_base=LLM_API_BASE,
        api_key=LLM_API_KEY,
        temperature=0.1,
        max_tokens=2048,
        is_chat_model=True,
        system_prompt=SYSTEM_PROMPT,
    )
    print("   ✅ LLM готов")
    return llm


# ─────────────────────────────────────────────────────────────────────────────
# Шаг 7 — CLI-диалог
# ─────────────────────────────────────────────────────────────────────────────

def ask(query_engine, question: str, show_sources: bool = True) -> None:
    print(f"\n❓ {question}")
    print("─" * 70)
    response = query_engine.query(question)
    print(f"💬 {response}")
    if show_sources:
        seen: set[str] = set()
        sources = []
        for node in response.source_nodes:
            domain   = node.metadata.get("domain", "?")
            std      = node.metadata.get("standard", "?")
            src_type = node.metadata.get("type", "?")
            score    = node.score or 0.0
            key = f"{domain}/{std}/{src_type}"
            if key not in seen:
                sources.append(f"  → {domain}/{std} ({src_type})  релевантность: {score:.3f}")
                seen.add(key)
        if sources:
            print("\n📎 Источники:")
            print("\n".join(sources))


HELP_TEXT = textwrap.dedent("""
    Команды:
      <вопрос>        — задать вопрос по стандартам
      /info           — показать текущую конфигурацию
      /rebuild        — очистить кэш и пересобрать индекс
      /help           — эта справка
      /exit, выход    — выйти
""").strip()


def cli_loop(query_engine, index_ref: dict) -> None:
    """Основной диалоговый цикл в терминале."""
    print("\n" + "═" * 70)
    print("  🏛️  ГОСТ-эксперт  |  база знаний ГОСТ Р 77.*")
    print("═" * 70)
    print(HELP_TEXT)
    print()

    while True:
        try:
            raw = input("🔹 Вопрос: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nСессия завершена.")
            break

        if not raw:
            continue

        cmd = raw.lower()

        if cmd in ("/exit", "выход", "exit", "quit"):
            print("Сессия завершена.")
            break

        elif cmd == "/help":
            print(HELP_TEXT)

        elif cmd == "/info":
            print(f"  Репозиторий : {GOST_KB_URL}")
            print(f"  ChromaDB    : {CHROMA_PATH}")
            print(f"  LLM         : {LLM_PROVIDER} / {LLM_MODEL} @ {LLM_API_BASE}")
            print(f"  Эмбеддинги  : {EMBED_MODEL_NAME}")

        elif cmd == "/rebuild":
            import chromadb as _chroma
            print("🗑️  Очищаю кэш...")
            _client = _chroma.PersistentClient(path=CHROMA_PATH)
            try:
                _client.delete_collection(CHROMA_COLLECTION)
            except Exception:
                pass
            docs = load_documents()
            new_index = build_index(docs)
            from llama_index.core import Settings
            index_ref["engine"] = new_index.as_query_engine(
                similarity_top_k=6, response_mode="compact"
            )
            print("✅ Индекс пересобран")

        else:
            try:
                ask(index_ref["engine"], raw)
            except Exception as e:
                print(f"❌ Ошибка при запросе: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    from llama_index.core import Settings

    # 1. Проверяем окружение
    if not check_environment():
        print("\n❌ Окружение не готово. Исправьте ошибки выше и запустите снова.")
        sys.exit(1)

    # 2. Загружаем документы только если индекс отсутствует
    import chromadb as _chroma
    _client = _chroma.PersistentClient(path=CHROMA_PATH)
    _col = _client.get_or_create_collection(CHROMA_COLLECTION)
    documents = [] if _col.count() > 0 else load_documents()

    # 3. Строим / восстанавливаем индекс
    index = build_index(documents)

    # 4. Подключаем LLM
    Settings.llm = build_llm()

    # 5. Создаём поисковый движок
    query_engine = index.as_query_engine(
        similarity_top_k=6,
        response_mode="compact",
    )

    # 6. CLI-диалог
    index_ref = {"engine": query_engine}
    cli_loop(query_engine, index_ref)


if __name__ == "__main__":
    main()
