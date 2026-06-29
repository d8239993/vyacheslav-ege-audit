# -*- coding: utf-8 -*-
"""Генерация диаграмм для аудита подготовки Вячеслава к ЕГЭ-2026 (информатика)."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).parent
CHARTS = BASE / "charts" / "informatics"
CHARTS.mkdir(parents=True, exist_ok=True)

COLORS = {
    "primary": "#7C3AED",
    "secondary": "#6366F1",
    "accent": "#F59E0B",
    "success": "#10B981",
    "danger": "#EF4444",
    "warn": "#F97316",
    "muted": "#94A3B8",
    "cyan": "#06B6D4",
    "bg": "#F8FAFC",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.facecolor": COLORS["bg"],
    "figure.facecolor": "white",
})

PRIMARY_TO_SECONDARY = {
    0: 0, 1: 7, 2: 14, 3: 20, 4: 27, 5: 34, 6: 40, 7: 43, 8: 46, 9: 48,
    10: 51, 11: 54, 12: 56, 13: 59, 14: 62, 15: 64, 16: 67, 17: 70,
    18: 72, 19: 75, 20: 78, 21: 80, 22: 83, 23: 85, 24: 88, 25: 90,
    26: 93, 27: 95, 28: 98, 29: 100,
}


def donut(ax, sizes, labels, colors, title, center_val, center_sub="", explode=None):
    if explode is None:
        explode = [0.03] * len(sizes)
    ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct=lambda p: f"{p:.0f}%" if p > 4 else "",
        startangle=90, pctdistance=0.78, textprops={"fontsize": 8},
    )
    centre = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre)
    ax.text(0, 0.06, center_val, ha="center", va="center", fontsize=22, fontweight="bold", color=COLORS["primary"])
    ax.text(0, -0.16, center_sub, ha="center", va="center", fontsize=9, color=COLORS["muted"])
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)


def chart_ege_structure():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    donut(axes[0], [25, 4], ["Зад. 1–25\n(по 1)", "Зад. 26–27\n(по 2)"],
          [COLORS["secondary"], COLORS["primary"]], "29 первичных = 100 втор.", "29", "перв. баллов")
    donut(axes[1], [11, 11, 5], ["Базовый\n(1–11)", "Повыш.\n(12–22)", "Высокий\n(23–27)"],
          [COLORS["success"], COLORS["accent"], COLORS["danger"]], "27 заданий · 3 уровня", "27", "КЕГЭ")
    donut(axes[2], [9, 20], ["Верно\n(экзамен)", "Упущено"],
          [COLORS["warn"], "#E2E8F0"], "Результат 18.06.2026", "9", "перв. → 48 втор.")
    plt.tight_layout()
    plt.savefig(CHARTS / "ege_structure.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_diagnostic_start():
    fig, ax = plt.subplots(figsize=(8, 8))
    donut(ax, [5, 95], ["Школьная\nинформатика\n(теория)", "Програм-\nмирование"],
          [COLORS["warn"], COLORS["danger"]], "Старт: программирование с нуля", "0%", "Python / код")
    plt.tight_layout()
    plt.savefig(CHARTS / "diagnostic_start.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_course_modules():
    fig, ax = plt.subplots(figsize=(10, 10))
    modules = [
        "Python:\nосновы", "Циклы\nи списки", "Строки\nи файлы", "Функции\nи рекурсия",
        "Числовые\nсистемы", "Логика\nи графы", "Excel /\nтаблицы", "SQL\nи БД",
        "Шаблоны\n№12–18", "Шаблоны\n№19–25", "№26–27\n(ускор.)",
    ]
    colors = plt.cm.Purples(np.linspace(0.45, 0.95, len(modules)))
    donut(ax, [1] * len(modules), modules, colors, "Авторский курс Python под ЕГЭ", "11", "модулей")
    plt.tight_layout()
    plt.savefig(CHARTS / "course_modules.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_score_timeline():
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ["24.04\nпробник", "12.06\nконтроль", "17.06\nфинал", "18.06\nэкзамен"]
    vals = [70, 18, 70, 48]
    colors = [COLORS["success"], COLORS["danger"], COLORS["success"], COLORS["warn"]]
    bars = ax.bar(labels, vals, color=colors, width=0.55, edgecolor="white", linewidth=2)
    ax.axhline(70, color=COLORS["accent"], ls="--", lw=1.5, label="Порог «5» (70 втор.)")
    ax.axhline(40, color=COLORS["muted"], ls=":", lw=1.2, label="Порог «4» (40 втор.)")
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 1.5, f"{v}",
                ha="center", fontweight="bold", fontsize=12)
    ax.annotate("+30 за 6 дн.", xy=(3, 48), xytext=(2.3, 58),
                arrowprops=dict(arrowstyle="->", color=COLORS["success"], lw=1.5),
                fontsize=10, fontweight="bold", color=COLORS["success"])
    ax.set_ylim(0, 85)
    ax.set_ylabel("Вторичные баллы")
    ax.set_title("Динамика контролей и экзамена", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / "score_timeline.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_data_loss():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    donut(axes[0], [100, 0], ["Утеряно\n(май)", "Сохранено"],
          [COLORS["danger"], "#E2E8F0"], "База знаний на ПК (май)", "0%", "шаблоны + конспекты")
    donut(axes[1], [45, 55], ["Математика\n+ физика", "Информатика\n(пауза)"],
          [COLORS["secondary"], COLORS["muted"]], "Фокус мая — перед экзаменами", "≈0", "занятий по инф.")
    plt.tight_layout()
    plt.savefig(CHARTS / "data_loss.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_intensive_week():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    donut(axes[0], [6, 0], ["Дней\nинтенсива", ""],
          [COLORS["primary"], COLORS["accent"]], "12–18 июня: финальный рывок", "6", "дней")
    donut(axes[1], [18, 30, 48], ["12.06\nстарт", "Прирост\n+30", "18.06\nэкзамен"],
          [COLORS["danger"], COLORS["success"], COLORS["warn"]], "18 → 48 на КЕГЭ", "+30", "втор. за 6 дн.")
    plt.tight_layout()
    plt.savefig(CHARTS / "intensive_week.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_templates():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    donut(axes[0], [50, 50], ["1-й набор\n(до мая)", "2-й набор\n(13.06)"],
          [COLORS["muted"], COLORS["primary"]], "Авторские шаблоны Python", "2×", "разработка")
    donut(axes[1], [70, 30], ["По шаблону\n(контроль)", "Творческий\nподход"],
          [COLORS["success"], COLORS["accent"]], "17.06: шаблоны сработали", "70", "втор. баллов")
    plt.tight_layout()
    plt.savefig(CHARTS / "templates.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_mock_exam():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    donut(axes[0], [70, 30], ["24.04\nпробник", "До максимума"],
          [COLORS["success"], "#E2E8F0"], "Пробник до сбоя ПК", "70", "втор. (17 перв.)")
    donut(axes[1], [17, 12], ["База +\nпрограмм.", "Не решал\n23–27"],
          [COLORS["primary"], COLORS["muted"]], "Структура пробника 24.04", "17", "перв. баллов")
    donut(axes[2], [70, 30], ["17.06\nфинал", "До максимума"],
          [COLORS["success"], "#E2E8F0"], "Финальный контроль", "70", "втор. за сутки до ЕГЭ")
    plt.tight_layout()
    plt.savefig(CHARTS / "mock_exam.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_expected_vs_actual():
    fig, ax = plt.subplots(figsize=(9, 6))
    labels = ["17.06\n(контроль)", "24.04\n(пробник)", "18.06\n(экзамен)"]
    vals = [70, 70, 48]
    colors = [COLORS["success"], COLORS["secondary"], COLORS["danger"]]
    bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=2)
    ax.axhline(70, color=COLORS["accent"], ls="--", lw=1.5, label="Ожидание (70 втор.)")
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 1.5, f"{v} втор.",
                ha="center", fontweight="bold", fontsize=11)
    ax.set_ylim(0, 85)
    ax.set_ylabel("Вторичные баллы")
    ax.set_title("Контроли vs экзамен: разрыв −22 балла", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / "expected_vs_actual.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_exam_day():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    donut(axes[0], [91, 9], ["Совпадение\nс ДВ", "Отличия"],
          [COLORS["success"], COLORS["muted"]], "18.06 утро: вариант ДВ", "91%", "с 2023 — рекорд")
    donut(axes[1], [100, 0], ["Разобрано\nутром", "Пропущено"],
          [COLORS["primary"], "#E2E8F0"], "Задачи с контроля 17.06", "100%", "все номера")
    plt.tight_layout()
    plt.savefig(CHARTS / "exam_day.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_exam_result():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    donut(axes[0], [48, 52], ["Набрано\nна экзамене", "Упущено"],
          [COLORS["warn"], "#E2E8F0"], "ЕГЭ 18.06.2026", "48", "втор. (оценка «3»)")
    lost = ["Программ.\n№12–27", "Поведение\nна КЕГЭ", "Пауза\nв мае", "Потеря\nшаблонов"]
    donut(axes[1], [40, 25, 20, 15], lost,
          [COLORS["danger"], COLORS["warn"], COLORS["accent"], COLORS["muted"]],
          "Структура разрыва: 48 vs 70", "−22", "втор. баллов")
    plt.tight_layout()
    plt.savefig(CHARTS / "exam_result.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_blank_breakdown():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    blocks = ["Базовый\n1–11", "Повыш.\n12–22", "Высокий\n23–27"]
    scored = [9, 0, 0]
    max_pts = [11, 11, 7]
    x = np.arange(len(blocks))
    w = 0.35
    axes[0].bar(x - w / 2, max_pts, w, label="Максимум", color="#E2E8F0", edgecolor="white")
    axes[0].bar(x + w / 2, scored, w, label="Набрано", color=COLORS["primary"], edgecolor="white")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(blocks)
    axes[0].set_ylabel("Первичные баллы")
    axes[0].set_title("Бланк КЕГЭ: баллы по блокам (9 перв.)", fontweight="bold")
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    correct = 9
    wrong = 18
    donut(axes[1], [correct, wrong], ["Верно\n(9 зад.)", "Ошибка /\nне решено"],
          [COLORS["success"], COLORS["danger"]], "27 заданий КИМ", "33%", "заданий верно")
    plt.tight_layout()
    plt.savefig(CHARTS / "blank_breakdown.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_behavior():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    donut(axes[0], [35, 30, 35], ["Низкая\nмотивация", "Объём\nДЗ", "Пауза +\nсбой ПК"],
          [COLORS["danger"], COLORS["warn"], COLORS["accent"]], "Факторы подготовки", "3", "блока")
    donut(axes[1], [55, 45], ["Знания\n(17.06)", "Экзамен\n(18.06)"],
          [COLORS["success"], COLORS["danger"]], "Разрыв 70 → 48", "≈55%", "не в знаниях*")
    donut(axes[2], [9, 17], ["Экзамен\n(9 перв.)", "Контроль\n(17 перв.)"],
          [COLORS["warn"], COLORS["success"]], "За сутки до ЕГЭ", "−8", "перв. баллов")
    plt.tight_layout()
    plt.savefig(CHARTS / "behavior.png", dpi=180, bbox_inches="tight")
    plt.close()


def build_all():
    print("Generating informatics charts...")
    chart_ege_structure()
    chart_diagnostic_start()
    chart_course_modules()
    chart_score_timeline()
    chart_data_loss()
    chart_intensive_week()
    chart_templates()
    chart_mock_exam()
    chart_expected_vs_actual()
    chart_exam_day()
    chart_exam_result()
    chart_blank_breakdown()
    chart_behavior()
    print(f"Done: {CHARTS}")


if __name__ == "__main__":
    build_all()
