# Аудит подготовки к ЕГЭ — Вячеслав (2026)

Отчёты о подготовке ученика: диагностика, динамика баллов, банк ФИПИ, аудит экзамена.

- **Репозиторий:** [d8239993/vyacheslav-ege-audit](https://github.com/d8239993/vyacheslav-ege-audit)
- **Математика (профиль):** [https://d8239993.github.io/vyacheslav-ege-audit/](https://d8239993.github.io/vyacheslav-ege-audit/)
- **Физика:** [https://d8239993.github.io/vyacheslav-ege-audit/physics/](https://d8239993.github.io/vyacheslav-ege-audit/physics/)
- **Информатика:** [https://d8239993.github.io/vyacheslav-ege-audit/informatics/](https://d8239993.github.io/vyacheslav-ege-audit/informatics/)

## Структура

- `index.html` — отчёт по профильной математике
- `physics/index.html` — отчёт по физике
- `informatics/index.html` — отчёт по информатике
- `css/styles.css` — общие стили (mobile-first)
- `physics/css/physics.css` — тема отчёта по физике
- `informatics/css/informatics.css` — тема отчёта по информатике
- `js/lightbox.js` — увеличение таблиц и диаграмм по клику
- `charts/` — диаграммы (PNG), в т.ч. `charts/physics/`, `charts/informatics/`
- `package_for_pages.py` — сборка `_site` для GitHub Pages
- `.github/workflows/pages.yml` — автодеплой при push в `main`
- `generate_report.py`, `generate_physics_report.py`, `generate_informatics_report.py` — локальная перегенерация графиков

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
