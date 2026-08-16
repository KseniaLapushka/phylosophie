# phylosophie

Личный сайт с конспектами лекций на [MkDocs Material](https://squidfunk.github.io/mkdocs-material/),
опубликованный бесплатно через GitHub Pages.

Сайт: [`https://KseniaLapushka.github.io/phylosophie/`](https://KseniaLapushka.github.io/phylosophie/)

## Структура

```
docs/
  index.md                 <- главная страница (список курсов)
  istina/                  <- курс "Истина"
    index.md               <- описание курса, список занятий
    zanyatie-01-....md
    zanyatie-02-....md
snippets/
  copyright.md             <- текст об авторстве, подключается в конце каждого конспекта
```

Каждый курс/предмет — отдельная папка внутри `docs/`. Внутри — `index.md`
(описание курса) и файлы занятий `zanyatie-NN-tema.md`. Навигация строится
автоматически из структуры файлов — ничего не нужно руками прописывать
в `mkdocs.yml`.

В конце каждого конспекта — строка `--8<-- "copyright.md"`, которая
подключает единый текст об авторстве курса (правки в `snippets/copyright.md`
применятся сразу везде).

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

1. Найди папку курса в `docs/` (например `istina/`) или создай новую по
   тому же образцу.
2. Добавь файл `zanyatie-NN-tema.md`. В конце файла добавь строку
   `--8<-- "copyright.md"`, если конспект основан на чужом курсе.
3. Проверь локально (`mkdocs serve`), закоммить, запушь в `main`.
