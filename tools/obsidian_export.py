#!/usr/bin/env python3
"""Конвертирует конспект сайта (MkDocs Material) в заметку Obsidian.

  python3 tools/obsidian_export.py create <файл.md> <папка_в_vault> [--name "Имя"]
      Новая заметка <папка_в_vault>/<Имя>.md. Имя по умолчанию — title из
      frontmatter. Заголовок H1 сохраняется.

  python3 tools/obsidian_export.py append <файл.md> <заметка_в_vault.md>
      Дописывает конспект В КОНЕЦ существующей заметки (там могут быть
      личные пометки — они не трогаются): разделитель, заголовок
      «## Полный конспект (сайт)», все заголовки сайта сдвинуты на уровень
      вниз, H1 и «Связанные конспекты» убраны.
      Никогда не перезаписывает: create откажется, если заметка уже есть
      (в Obsidian в ней могут быть личные заметки, которых нет на сайте).

Что конвертируется: frontmatter, ссылка-«назад», сниппет copyright, блоки
!!! example/note/... -> коллбоксы Obsidian, HTML-поля домашки -> чек-листы,
относительные ссылки на .md -> [[вики-ссылки]] (по title целевого файла).
"""
import re
import sys
from pathlib import Path

BAD = '\\/:*"<>|'


def note_name(title: str) -> str:
    return ''.join(c for c in title if c not in BAD).strip()


def page_title(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    m = re.match(r'---\n.*?^title:\s*(.+?)\s*$.*?\n---\n', text, flags=re.S | re.M)
    if m:
        return m.group(1).strip().strip('"\'')
    m = re.search(r'^# (.+)$', text, flags=re.M)
    return m.group(1).strip() if m else path.stem


def convert(src: Path, shift: int, drop_h1: bool, drop_related: bool = False) -> str:
    text = src.read_text(encoding='utf-8')
    text = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)
    text = re.sub(r'^\[← .*?\]\(.*?\)\{:\s*\.back-link\s*\}\n+', '', text, flags=re.M)
    text = re.sub(r'\n--8<--\s*"copyright\.md"\s*\n?', '\n', text)
    if drop_h1:
        text = re.sub(r'^# .*\n+', '', text, count=1, flags=re.M)
    if drop_related:  # при дописывании в существующую заметку навигация не нужна
        text = re.sub(r'\n#{1,6} Связанные конспекты\n.*?(?=\n#{1,6} |\Z)', '\n', text, flags=re.S)

    def hw(m):
        p = re.search(r'<p>(.*?)</p>', m.group(0), flags=re.S)
        q = re.sub(r'<br\s*/?>', ' ', p.group(1) if p else '')
        return '- [ ] ' + re.sub(r'\s+', ' ', q).strip()
    text = re.sub(r'<div class="hw-item".*?</div>', hw, text, flags=re.S)

    def adm(m):
        kind, title, body = m.group(1), m.group(2) or '', m.group(3)
        out = [f'> [!{kind}] {title}'.rstrip()]
        for ln in body.rstrip('\n').split('\n'):
            ln = (ln[4:] if ln.startswith('    ') else ln).rstrip()
            out.append('> ' + ln if ln else '>')
        return '\n'.join(out) + '\n\n'
    text = re.sub(r'!!! (\w+)(?: "([^"]*)")?\n\n?((?:(?:    .*)?\n)+)', adm, text)

    def link(m):
        label, target = m.group(1), m.group(2)
        path, _, _anchor = target.partition('#')
        dest = (src.parent / path).resolve()
        if dest.is_file():
            return f'[[{note_name(page_title(dest))}|{label}]]'
        return m.group(0)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+\.md(?:#[^)]*)?)\)', link, text)

    if shift:
        text = re.sub(r'^(#{1,6}) ', lambda m: '#' * (len(m.group(1)) + shift) + ' ',
                      text, flags=re.M)
    return re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'


def main(argv):
    if len(argv) < 4 or argv[1] not in ('create', 'append'):
        print(__doc__)
        return 1
    mode, src, dest = argv[1], Path(argv[2]), Path(argv[3])
    if mode == 'create':
        name = argv[argv.index('--name') + 1] if '--name' in argv else note_name(page_title(src))
        dest.mkdir(parents=True, exist_ok=True)
        target = dest / f'{name}.md'
        if target.exists():
            print(f'Уже существует, не перезаписываю: {target}')
            return 2
        target.write_text(convert(src, 0, False), encoding='utf-8')
    else:
        if not dest.is_file():
            print(f'Нет такой заметки: {dest}')
            return 2
        body = convert(src, 1, True, drop_related=True)
        with dest.open('a', encoding='utf-8') as f:
            f.write('\n---\n\n## Полный конспект (сайт)\n\n' + body)
        target = dest
    print(f'OK: {target}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
