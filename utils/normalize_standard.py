#!/usr/bin/env python3
"""
Normalize full.raw.md to full.md for GOST R 77.* standards.
Rules:
- Preserve meaning and legal wording
- Remove Word/Pandoc noise (repeated headers/footers, page numbers, excessive empty lines)
- Maintain section numbering
- Add metadata header

Usage (from repo root):
  python utils/normalize_standard.py <standard_number>
  e.g.: python utils/normalize_standard.py 102
"""

import os
import re
import json
import sys
from pathlib import Path

# Resolve repo root regardless of working directory
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent


def normalize_content(raw_content, standard_num):
    """Normalize raw pandoc output to clean markdown."""
    
    lines = raw_content.split('\n')
    result_lines = []
    
    # Track state
    skip_table_header = False
    in_header_table = False
    header_table_rows = 0
    seen_intro = False
    
    # Patterns to detect and remove
    footer_pattern = re.compile(r'^_\s*_+|^\*{2,}\s*\*{2,}$|^#{8,}\s*Дата введения')
    page_break_pattern = re.compile(r'^\*Проект.*редакция\*$|^\*{2,}$')
    toc_entry_pattern = re.compile(r'^\[.*\]\(#_Toc\d+\)$')
    empty_line_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip table of contents entries with _Toc anchors
        if toc_entry_pattern.match(line.strip()):
            i += 1
            continue
        
        # Skip the large header tables (they contain logo, standard number in table form)
        if '<table>' in line and not seen_intro:
            in_header_table = True
            while i < len(lines) and '</table>' not in lines[i]:
                i += 1
            if i < len(lines):
                i += 1  # Skip closing tag too
            result_lines.append('')
            continue
        
        # Skip repeated "Проект, окончательная редакция" markers that appear mid-document
        if '*Проект' in line and 'редакция*' in line and i > 50:
            i += 1
            continue
        
        # Skip pure decorative lines
        if re.match(r'^[_\-\*]{10,}$', line.strip()):
            i += 1
            continue
        
        # Skip empty lines but track them
        if line.strip() == '':
            empty_line_count += 1
            if empty_line_count <= 2:  # Allow max 2 consecutive empty lines
                result_lines.append(line)
            i += 1
            continue
        else:
            empty_line_count = 0
        
        # Clean up some common artifacts
        cleaned = line
        
        # Remove anchor spans like <span id="_Toc..."></span>
        cleaned = re.sub(r'<span id="[^"]*"\s*class="anchor"\s*></span>\s*', '', cleaned)
        
        # Fix underscore sequences used as separators
        if re.match(r'^_{10,}$', cleaned.strip()):
            i += 1
            continue
        
        result_lines.append(cleaned)
        i += 1
    
    # Join and post-process
    text = '\n'.join(result_lines)
    
    # Remove multiple consecutive empty lines (more than 2)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    return text


def extract_title(raw_content):
    """Extract the Russian title from the document."""
    lines = raw_content.split('\n')
    
    title = ""
    subtitle = ""
    
    for line in lines[:100]:
        stripped = line.strip()
        if '**Система поддержки жизненного цикла изделия**' in stripped and not title:
            title = "Система поддержки жизненного цикла изделия"
        elif '**ИНФОРМАЦИОННАЯ МОДЕЛЬ ИЗДЕЛИЯ**' in stripped:
            subtitle = "Информационная модель изделия"
        elif '**Термины и определения**' in stripped and 'Область применения' not in stripped:
            subtitle = "Термины и определения"
        elif '**Общие требования**' in stripped and 'Область применения' not in stripped:
            subtitle = "Общие требования"
        elif '**Модель жизненного цикла изделия**' in stripped:
            subtitle = "Модель жизненного цикла изделия"
        elif '**Основные положения**' in stripped and 'Область применения' not in stripped:
            if not subtitle:
                subtitle = "Основные положения"
        elif '**Виды программных средств поддержки жизненного цикла**' in stripped:
            subtitle = "Виды программных средств поддержки жизненного цикла"
        elif '**Интероперабельность программных средств**' in stripped:
            subtitle = "Интероперабельность программных средств"
        elif '**Цифровые двойники изделий**' in stripped:
            subtitle = "Цифровые двойники изделий"
        elif '**Управление конфигурацией изделия**' in stripped:
            subtitle = "Управление конфигурацией изделия"
        elif '**Управление данными об изделии**' in stripped:
            subtitle = "Управление данными об изделии"
        elif '**Классификатор видов деятельности по поддержке жизненного цикла изделия**' in stripped:
            subtitle = "Классификатор видов деятельности"
    
    if title and subtitle:
        return f"{title}. {subtitle}"
    elif title:
        return title
    elif subtitle:
        return subtitle
    else:
        return f"ГОСТ Р 77.{standard_num}"


def extract_terms(raw_content):
    """Extract terms from the 'Terms and definitions' section."""
    terms = []
    
    term_pattern = re.compile(r'^(\d+\.\d+\.\d+)\s+\*\*(.+?)\*\*[:\s]*(.+?)(?=\n\s*\n|\n\d|\Z)', 
                              re.MULTILINE | re.DOTALL)
    
    matches = term_pattern.findall(raw_content)
    for match in matches:
        term_num, term_name, definition = match
        term_name = re.sub(r'\*\*', '', term_name).strip()
        if ';' in term_name:
            term_name = term_name.split(';')[0].strip()
        if term_name and len(term_name) > 2:
            terms.append(term_name)
    
    return terms[:20]


def extract_keywords(raw_content):
    """Extract keywords from the document."""
    keywords = []
    
    common_kw = [
        "жизненный цикл", "поддержка жизненного цикла", "изделие", 
        "машиностроение", "системная инженерия", "цифровая трансформация",
        "информационная модель", "цифровой двойник", "управление данными",
        "управление конфигурацией", "интероперабельность", "программные средства",
        "термины и определения", "классификация", "стандартизация"
    ]
    
    text_lower = raw_content.lower()
    for kw in common_kw:
        if kw in text_lower:
            keywords.append(kw)
    
    return keywords[:10]


def extract_related_standards(raw_content):
    """Extract references to other GOST standards."""
    related = set()
    
    gost_pattern = re.compile(r'ГОСТ\s*[Р]?[\s\.]?(\d+\.\d+)', re.IGNORECASE)
    matches = gost_pattern.findall(raw_content)
    for match in matches:
        related.add(f"ГОСТ Р 77.{match}")
    
    ref_pattern = re.compile(r'ГОСТ\s*Р\s*77\.(\d{3})')
    matches = ref_pattern.findall(raw_content)
    for match in matches:
        related.add(f"ГОСТ Р 77.{match}")
    
    return sorted(list(related))[:15]


def create_metadata(standard_num, raw_content, source_file):
    """Create metadata.json content."""
    title = extract_title(raw_content)
    terms = extract_terms(raw_content)
    keywords = extract_keywords(raw_content)
    related = extract_related_standards(raw_content)
    
    status = "project"
    if "окончательная редакция" in raw_content:
        status = "project"
    elif "первая редакция" in raw_content:
        status = "draft"
    
    metadata = {
        "id": f"gost-r-77-{standard_num}",
        "standard_number": f"ГОСТ Р 77.{standard_num}",
        "title": title,
        "status": status,
        "revision": None,
        "source_url": None,
        "source_file": source_file,
        "language": "ru",
        "keywords": keywords,
        "glossary_terms": terms,
        "related_standards": related,
        "processing_stage": "normalized-from-docx-v1"
    }
    
    return metadata


def create_summary(raw_content, standard_num, metadata):
    """Create summary.md content."""
    title = metadata['title']
    terms = metadata['glossary_terms']
    related = metadata['related_standards']
    
    scope_text = ""
    scope_match = re.search(r'(?:^|\n)\s*1\.\s*Область применения\s*\n(.+?)(?=\n\s*2\.)', 
                            raw_content, re.DOTALL)
    if scope_match:
        scope_text = scope_match.group(1).strip()
        scope_text = re.sub(r'\n+', '\n', scope_text)
        scope_lines = [l.strip() for l in scope_text.split('\n') if l.strip() and not l.strip().startswith('*')]
        scope_points = scope_lines[:7]
    else:
        scope_points = []
    
    key_provisions = []
    section_pattern = re.compile(r'(?:^|\n)(\d+\.\d+)\s+([^\n]+)')
    sections = section_pattern.findall(raw_content)
    for sec_num, sec_title in sections[:15]:
        if sec_title and len(sec_title) > 5:
            key_provisions.append(f"{sec_num} {sec_title.strip()}")
    
    summary = f"""# ГОСТ Р 77.{standard_num} — краткое содержание

## Область применения

{chr(10).join('- ' + p for p in scope_points) if scope_points else 'Информация извлекается из полного текста стандарта.'}

## Ключевые положения

{chr(10).join('- ' + p for p in key_provisions) if key_provisions else 'См. полный текст стандарта.'}

## Ключевые термины

{chr(10).join('- ' + t for t in terms) if terms else 'Термины не выделены или отсутствуют в данном стандарте.'}

## Связанные документы

{chr(10).join('- ' + r for r in related) if related else 'Нет явных ссылок на другие стандарты.'}

---

*Это краткое содержание создано автоматически на основе нормализованной версии стандарта. Для точной информации обращайтесь к полному тексту full.md.*
"""
    
    return summary


def normalize_standard(raw_path, standard_num):
    """Main function to normalize a standard."""
    
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    if not raw_content.strip():
        print(f"ERROR: {raw_path} is empty")
        return False
    
    normalized = normalize_content(raw_content, standard_num)
    
    source_file = f"source-docx/77.{standard_num}.docx"
    title = extract_title(raw_content)
    
    header = f"""---
standard: ГОСТ Р 77.{standard_num}
title: {title}
source: {source_file}
note: Нормализованная Markdown-версия, полученная из DOCX файла
---

"""
    
    full_content = header + normalized
    
    dir_path = Path(raw_path).parent
    full_md_path = dir_path / 'full.md'
    
    with open(full_md_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    metadata = create_metadata(standard_num, raw_content, source_file)
    metadata_path = dir_path / 'metadata.json'
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    summary = create_summary(raw_content, standard_num, metadata)
    summary_path = dir_path / 'summary.md'
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✓ Processed 77.{standard_num}: full.md ({len(full_content)} bytes), metadata.json, summary.md")
    return True


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python utils/normalize_standard.py <standard_number>")
        print("Example: python utils/normalize_standard.py 102")
        sys.exit(1)
    
    standard_num = sys.argv[1]
    raw_path = REPO_ROOT / 'standards' / f'77-{standard_num}' / 'full.raw.md'
    
    if not raw_path.exists():
        print(f"ERROR: {raw_path} not found")
        sys.exit(1)
    
    success = normalize_standard(raw_path, standard_num)
    sys.exit(0 if success else 1)
