#!/usr/bin/env python3
"""
Build INDEX.md, GLOSSARY.md, and llms.txt for the GOST R 77.* knowledge base.
"""

import os
import json
from pathlib import Path

def load_metadata(standards_dir):
    """Load metadata from all standards across all domains."""
    metadata_list = []

    standards_path = Path(standards_dir)
    
    # Iterate over domains (first level: lci, eskd, interop, ...)
    for domain_dir in sorted(standards_path.iterdir()):
        if not domain_dir.is_dir():
            continue
        
        # Skip directories starting with underscore (e.g., _template)
        if domain_dir.name.startswith('_'):
            continue
        
        # Iterate over standards within each domain
        for std_dir in sorted(domain_dir.iterdir()):
            if not std_dir.is_dir():
                continue
            
            metadata_path = std_dir / 'metadata.json'
            full_md_path = std_dir / 'full.md'
            summary_md_path = std_dir / 'summary.md'
            
            if not metadata_path.exists() or not full_md_path.exists():
                continue
            
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Add domain field
            metadata['domain'] = domain_dir.name
            
            # Add paths relative to standards/
            # rel_path is used for local file access (e.g., GLOSSARY.md build)
            metadata['rel_path'] = f"{domain_dir.name}/{std_dir.name}"
            # full_md_path, summary_md_path, metadata_json_path are used in INDEX.md and llms.txt
            metadata['full_md_path'] = f"standards/{domain_dir.name}/{std_dir.name}/full.md"
            metadata['summary_md_path'] = f"standards/{domain_dir.name}/{std_dir.name}/summary.md"
            metadata['metadata_json_path'] = f"standards/{domain_dir.name}/{std_dir.name}/metadata.json"
            
            metadata_list.append(metadata)

    return metadata_list


def create_index(metadata_list, output_path):
    """Create INDEX.md with table of all standards."""

    content = """# Индекс стандартов ГОСТ Р 77.*

Система поддержки жизненного цикла изделия

## Обработанные стандарты

| Номер | Название | Полный текст | Краткое содержание | Статус | Описание |
|-------|----------|--------------|-------------------|--------|----------|
"""

    for meta in metadata_list:
        std_num = meta['standard_number']
        title = meta['title']
        full_path = meta['full_md_path']
        summary_path = meta['summary_md_path']
        status = meta.get('status', 'unknown')
        keywords = meta.get('keywords', [])

        # Create short description from first keyword
        desc = keywords[0] if keywords else ''

        content += f"| {std_num} | {title} | [full.md]({full_path}) | [summary.md]({summary_path}) | {status} | {desc} |\n"

    content += """

## Структура репозитория

```
standards/
└── standards/ # Стандарты в Markdown
    ├── _template/ # Шаблоны для новых стандартов
    │   ├── full.md        # Шаблон полной версии
    │   ├── summary.md     # Шаблон краткого описания
    │   ├── metadata.json  # Шаблон метаданных
    │   └── media/            — изображения
    ├── lci/ # Стандарты жизненного цикла (LCI)
    │   └── 77-XXX/
    ├── eskd/ # Стандарты ЕСКД
    │   └── XXXX/
    └── interop/ # Стандарты интероперабельности
        └── XXXXX/├── 77-001/
```

## Использование

- **full.md** — канонический справочный текст стандарта
- **summary.md** — быстрое ознакомление с основными положениями
- **metadata.json** — машиночитаемые метаданные для интеграции
- **GLOSSARY.md** — общий глоссарий терминов из всех стандартов

---

*Этот индекс создан автоматически. Для точной информации обращайтесь к полным текстам стандартов.*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Created INDEX.md with {len(metadata_list)} standards")


def create_glossary(metadata_list, standards_dir, output_path):
    """Create GLOSSARY.md aggregating terms from all standards."""

    # Collect all terms with their sources
    terms_dict = {}

    for meta in metadata_list:
        std_num = meta['standard_number']
        std_path = Path(standards_dir) / meta['rel_path']
        full_md_path = std_path / 'full.md'

        # Get terms from metadata
        glossary_terms = meta.get('glossary_terms', [])

        for term in glossary_terms:
            if term not in terms_dict:
                terms_dict[term] = []

            # Try to extract definition from full.md
            definition = extract_definition(full_md_path, term)
            terms_dict[term].append({
                'standard': std_num,
                'definition': definition
            })

    # Build glossary content
    content = """# Глоссарий терминов ГОСТ Р 77.*

Алфавитный указатель терминов из всех стандартов системы поддержки жизненного цикла изделия.

"""

    # Sort terms alphabetically
    sorted_terms = sorted(terms_dict.keys(), key=lambda x: x.lower())

    current_letter = ''
    for term in sorted_terms:
        # Group by first letter
        first_letter = term[0].upper()
        if first_letter != current_letter:
            current_letter = first_letter
            content += f"\n## {current_letter}\n\n"

        content += f"### {term}\n\n"

        for source in terms_dict[term]:
            std_num = source['standard']
            definition = source['definition']

            if definition:
                content += f"- **{std_num}**: {definition}\n"
            else:
                content += f"- **{std_num}**: [см. полный текст стандарта]\n"

        content += "\n"

    content += """
---

*Глоссарий создан автоматически на основе метаданных и текстов стандартов. Для точных определений обращайтесь к соответствующим разделам full.md каждого стандарта.*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Created GLOSSARY.md with {len(sorted_terms)} terms")


def extract_definition(full_md_path, term):
    """Try to extract definition for a term from full.md."""
    if not os.path.exists(full_md_path):
        return ""

    try:
        with open(full_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for term followed by definition pattern
        # Clean the term for regex
        clean_term = term.replace('(', r'\(').replace(')', r'\)').replace('*', '')

        # Pattern: **term**: definition or **term:** definition
        import re
        pattern = rf'\*\*{re.escape(term)}\*\*[:\s]*(.+?)(?=\n\n|\n\d|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            definition = match.group(1).strip()
            # Limit length
            if len(definition) > 500:
                definition = definition[:500] + "..."
            return definition

        return ""
    except Exception:
        return ""


def create_llms_txt(metadata_list, output_path):
    """Create llms.txt describing the repository for LLM consumption."""

    content = """# GOST R 77.* Knowledge Base

Репозиторий содержит нормализованные Markdown-версии национальных стандартов Российской Федерации серии ГОСТ Р 77.*
«Система поддержки жизненного цикла изделия».

## Назначение

Эта база знаний предназначена для использования LLM и другими автоматизированными системами для:
- Поиска информации по стандартам системы поддержки ЖЦ изделия
- Извлечения терминов и определений
- Анализа взаимосвязей между стандартами
- Поддержки инженерных и проектных задач

## Ключевые файлы

### Общие
- `INDEX.md` — полный список обработанных стандартов
- `GLOSSARY.md` — агрегированный глоссарий терминов
- `reports/build-report.md` — отчёт о сборке и качестве обработки

### Стандарты

Для каждого стандарта доступны:
- `standards/77-XXX/full.md` — **канонический справочный текст** (используйте как основной источник)
- `standards/77-XXX/summary.md` — краткое содержание для быстрого ознакомления
- `standards/77-XXX/metadata.json` — машиночитаемые метаданные

#### Список стандартов

"""

    for meta in metadata_list:
        std_num = meta['standard_number']
        title = meta['title']
        full_path = meta['full_md_path']
        summary_path = meta['summary_md_path']
        metadata_path = meta['metadata_json_path']

        content += f"- **{std_num}** {title}\n"
        content += f"  - Полный текст: `{full_path}`\n"
        content += f"  - Кратко: `{summary_path}`\n"
        content += f"  - Метаданные: `{metadata_path}`\n\n"

    content += """
## Важные примечания

1. **Канонический текст**: Файлы `full.md` являются нормализованными версиями оригинальных DOCX файлов.
   Они сохраняют смысл и формулировки оригинала, но могут содержать незначительные артефакты конвертации.

2. **Статус стандартов**: Все стандарты находятся в статусе «проект» или «черновик» и не являются официальными публикациями.

3. **Язык**: Все документы на русском языке.

4. **Изображения**: Графические материалы находятся в папках `standards/77-XXX/media/`.

## Лицензирование

Национальные стандарты РФ являются объектами авторского права.
Использование должно соответствовать законодательству РФ об авторском праве и правилам Федерального агентства по техническому регулированию и метрологии.

---

*Repository generated automatically from GOST R 77.* DOCX source files.*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Created llms.txt")


if __name__ == '__main__':
    standards_dir = Path('standards')

    # Load all metadata
    metadata_list = load_metadata(standards_dir)

    if not metadata_list:
        print("ERROR: No metadata found")
        exit(1)

    # Create outputs
    create_index(metadata_list, 'INDEX.md')
    create_glossary(metadata_list, standards_dir, 'GLOSSARY.md')
    create_llms_txt(metadata_list, 'llms.txt')

    print(f"\n✓ Built global index for {len(metadata_list)} standards")
