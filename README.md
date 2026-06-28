# Аудит подготовки к ЕГЭ — Вячеслав (профильная математика, 2026)

Отчёт о подготовке ученика: диагностика, динамика баллов, банк ФИПИ, аудит бланков.

- **Локальный путь:** `C:\Users\82399\Documents\Vyacheslav_EGE_Audit`
- **Публичный сайт:** после деплоя — `https://d8239993.github.io/vyacheslav-ege-audit/`

## Структура

- `index.html` — основной отчёт
- `css/styles.css` — стили (mobile-first)
- `charts/` — диаграммы (PNG)
- `package_for_pages.py` — сборка `_site` для GitHub Pages
- `.github/workflows/pages.yml` — автодеплой при push в `main`
- `generate_report.py` — локальная перегенерация графиков (не публикуется)

## Локальный просмотр

```bash
python package_for_pages.py
python -m http.server 8765 --directory _site
```

Открыть: http://127.0.0.1:8765/

## Публикация на GitHub Pages

1. `git add .`
2. `git commit -m "update report"`
3. `git push`

Или первый раз: `pwsh -File .\publish_to_github.ps1`

После push GitHub Actions собирает `_site` и публикует сайт.
