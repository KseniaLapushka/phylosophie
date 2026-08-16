# phylosophie

Личный сайт с конспектами лекций на [MkDocs Material](https://squidfunk.github.io/mkdocs-material/),
опубликованный бесплатно через GitHub Pages.

Сайт: [`https://KseniaLapushka.github.io/phylosophie/`](https://KseniaLapushka.github.io/phylosophie/)

## Структура

```
docs/
  index.md                 <- главная страница
  example-course/          <- шаблон одного курса (удали, когда заведёшь свои)
    index.md
    lecture-01-....md
    lecture-02-....md
```

Каждый курс/предмет — отдельная папка внутри `docs/`. Внутри — `index.md`
(описание курса) и файлы лекций `lecture-NN-tema.md`. Навигация строится
автоматически из структуры файлов — ничего не нужно руками прописывать
в `mkdocs.yml`.

## Работа локально

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Откроется `http://127.0.0.1:8000` с live-reload — конспект сохранил, страница
сама обновилась.

## Публикация

Сайт публикуется автоматически при пуше в `main` (см.
`.github/workflows/deploy.yml`) — GitHub Actions собирает сайт и кладёт его
в ветку `gh-pages`. Один раз нужно включить Pages в настройках репозитория:

**Settings → Pages → Source: Deploy from a branch → Branch: `gh-pages` / `root`**

После этого при каждом пуше в `main` сайт обновляется сам за 1-2 минуты.

## Добавить новый конспект

1. Найди папку курса в `docs/` или создай новую по образцу `example-course/`.
2. Добавь файл `lecture-NN-tema.md`.
3. Проверь локально (`mkdocs serve`), закоммить, запушь в `main`.
