# -*- coding: utf-8 -*-
"""Генерация диаграмм для аудита подготовки Вячеслава к ЕГЭ-2026 (физика)."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).parent
CHARTS = BASE / "charts" / "physics"
CHARTS.mkdir(parents=True, exist_ok=True)

COLORS = {
    "primary": "#0D9488",
    "secondary": "#0891B2",
    "accent": "#F59E0B",
    "success": "#10B981",
    "danger": "#EF4444",
    "warn": "#F97316",
    "muted": "#94A3B8",
    "purple": "#7C3AED",
    "blue": "#3B82F6",
    "bg": "#F8FAFC",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.facecolor": COLORS["bg"],
    "figure.facecolor": "white",
})

# --- Шкала ЕГЭ-2026 (физика): 45 перв. = 100 втор. ---
PRIMARY_TO_SECONDARY = {
    0: 0, 1: 5, 2: 9, 3: 14, 4: 18, 5: 23, 6: 27, 7: 32, 8: 36, 9: 39,
    10: 40, 11: 43, 12: 44, 13: 46, 14: 48, 15: 49, 16: 51, 17: 53, 18: 54,
    19: 56, 20: 58, 21: 59, 22: 61, 23: 62, 24: 64, 25: 65, 26: 67, 27: 68,
    28: 70, 29: 71, 30: 73, 31: 74, 32: 76, 33: 77, 34: 79, 35: 80, 36: 82,
    37: 84, 38: 86, 39: 88, 40: 90, 41: 92, 42: 94, 43: 96, 44: 98, 45: 100,
}

TASK_POINTS = {
    1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 1, 8: 1, 9: 2, 10: 2,
    11: 1, 12: 1, 13: 1, 14: 2, 15: 2, 16: 1, 17: 2, 18: 2, 19: 1, 20: 1,
    21: 3, 22: 2, 23: 2, 24: 3, 25: 3, 26: 4,
}


def donut(ax, sizes, labels, colors, title, center_val, center_sub="", explode=None):
    if explode is None:
        explode = [0.03] * len(sizes)
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct=lambda p: f"{p:.0f}%" if p > 4 else "",
        startangle=90, pctdistance=0.78, textprops={"fontsize": 8},
    )
    centre = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre)
    ax.text(0, 0.06, center_val, ha="center", va="center", fontsize=22, fontweight="bold", color=COLORS["primary"])
    ax.text(0, -0.16, center_sub, ha="center", va="center", fontsize=9, color=COLORS["muted"])
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    return wedges


def chart_diagnostic_start():
    fig, ax = plt.subplots(figsize=(8, 8))
    sizes = [18, 12, 70]
    labels = ["Кинематика\n(уверенно)", "Догадки\n(1-я часть)", "Не знал /\n2-я часть"]
    colors = [COLORS["success"], COLORS["warn"], COLORS["danger"]]
    donut(ax, sizes, labels, colors, "Входной контроль: структура знаний", "≈12%", "реальный уровень")
    plt.tight_layout()
    plt.savefig(CHARTS / "diagnostic_start.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_gaps_7_10():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    topics = ["СИ и\nизмерения", "Кинематика\n(база)", "Динамика", "Статика", "Сохранение\nэнергии",
              "Колебания", "МКТ", "Термо-\nдинамика", "Электри-\nчество", "Магнит-\nное поле", "Оптика", "Квантовая"]
    start = [15, 35, 8, 5, 5, 3, 4, 3, 6, 4, 5, 2]
    end = [88, 92, 90, 87, 89, 86, 88, 85, 90, 87, 84, 82]
    y = np.arange(len(topics))
    axes[0].barh(y, start, color=COLORS["danger"], alpha=0.85, label="Старт")
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(topics, fontsize=7)
    axes[0].set_xlim(0, 100)
    axes[0].set_title("Пробелы 7–10 кл. на старте (%)", fontweight="bold")
    axes[0].invert_yaxis()
    axes[0].grid(axis="x", alpha=0.3)

    axes[1].barh(y, end, color=COLORS["success"], alpha=0.85, label="После подготовки")
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(topics, fontsize=7)
    axes[1].set_xlim(0, 100)
    axes[1].set_title("Тот же блок после подготовки (%)", fontweight="bold")
    axes[1].invert_yaxis()
    axes[1].grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / "gaps_7_10.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_sections_studied():
    fig, ax = plt.subplots(figsize=(10, 10))
    sections = [
        "Кинематика", "Динамика", "Статика", "Законы\nсохранения",
        "Колебания\nи волны", "Молекулярная\nфизика", "Термо-\nдинамика",
        "Электро-\nдинамика", "Постоянный\nток", "Магнитное\nполе",
        "ЭМ колебания\nи волны", "ЭМ\nиндукция", "Оптика", "Квантовая\nфизика",
    ]
    sizes = [1] * len(sections)
    colors = plt.cm.Greens(np.linspace(0.45, 0.95, len(sections)))
    donut(ax, sizes, sections, colors, "14 разделов курса — пройдены полностью", "14", "разделов")
    plt.tight_layout()
    plt.savefig(CHARTS / "sections_studied.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_thematic_controls():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    donut(axes[0], [67.5, 32.5], ["Верно\n(ср.)", "Ошибки"],
          [COLORS["warn"], "#E2E8F0"], "1-й проход: тематические контроли", "65–72%", "после каждого раздела")
    donut(axes[1], [92.5, 7.5], ["Верно\n(ср.)", "Ошибки"],
          [COLORS["success"], "#E2E8F0"], "2-й проход: повторение всех разделов", "90–95%", "перед вариантами")
    plt.tight_layout()
    plt.savefig(CHARTS / "thematic_controls.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_mock_exam():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    donut(axes[0], [69, 1], ["Набрано\n(ср.)", "Упущено"],
          [COLORS["success"], COLORS["danger"]], "1-я часть на пробниках", "68–70", "из 70 втор. (макс.)")
    donut(axes[1], [7, 2, 8], ["№21–23\n(стабильно)", "№24\n(иногда)", "Не решал\n25–26"],
          [COLORS["primary"], COLORS["accent"], COLORS["muted"]], "2-я часть на пробниках", "+10–12", "втор. баллов")
    donut(axes[2], [82, 18], ["Ожидаемый\nрезультат", "Запас до\n100"],
          [COLORS["success"], "#E2E8F0"], "Суммарный прогноз", "80+", "вторичных баллов")
    plt.tight_layout()
    plt.savefig(CHARTS / "mock_exam.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_fipi_demidova():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    donut(axes[0], [50, 50], ["1-й полный\nпроход", "2-й полный\nпроход"],
          [COLORS["primary"], COLORS["secondary"]], "Открытый банк ФИПИ", "2×", "полных цикла")
    dem_sections = ["Механика\n(1–6)", "Молек.\n(7–10)", "Электро-\n(11–15)", "Квант.\n(16–17)",
                    "2-я часть\n(21–26)"]
    donut(axes[1], [1, 1, 1, 1, 1], dem_sections,
          [COLORS["blue"], COLORS["accent"], COLORS["purple"], COLORS["warn"], COLORS["success"]],
          "Методические материалы Демидовой", "100%", "сопоставлено с программой")
    plt.tight_layout()
    plt.savefig(CHARTS / "fipi_demidova.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_exam_day():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))
    donut(axes[0], [50, 50], ["Использовано\n(≈2 ч)", "Не использовано\n(≈2 ч)"],
          [COLORS["danger"], COLORS["muted"]], "Время на экзамене", "2 из 4", "часов")
    donut(axes[1], [100, 0], ["Разобрано\nбез ошибок", "Затруднений\nне было"],
          [COLORS["success"], "#E2E8F0"], "Утро 11 июня: 1-я часть ДВ", "✓", "самостоятельно")
    plt.tight_layout()
    plt.savefig(CHARTS / "exam_day.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_exam_result():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    donut(axes[0], [53, 47], ["Набрано\nна экзамене", "Упущено\nот максимума"],
          [COLORS["warn"], "#E2E8F0"], "Результат ЕГЭ 2026", "53", "вторичных (оценка «4»)")
    lost = ["Невниматель-\nность", "Страх /\nспешка", "2 ч вместо\n4 ч", "Прочие\nошибки"]
    donut(axes[1], [35, 30, 25, 10], lost,
          [COLORS["danger"], COLORS["warn"], COLORS["accent"], COLORS["muted"]],
          "Структура разрыва: 53 vs 80+ (оценка факторов)", "−27+", "втор. баллов")
    plt.tight_layout()
    plt.savefig(CHARTS / "exam_result.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_expected_vs_actual():
    fig, ax = plt.subplots(figsize=(9, 6))
    labels = ["Пробники\n(ожидание)", "Экзамен\n(факт)"]
    vals = [82, 53]
    colors = [COLORS["success"], COLORS["danger"]]
    bars = ax.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=2)
    ax.axhline(80, color=COLORS["accent"], ls="--", lw=1.5, label="Прогноз по пробникам (80+)")
    ax.axhline(41, color=COLORS["muted"], ls=":", lw=1.2, label="Порог в вуз (41)")
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, v + 1.5, f"{v} втор.",
                ha="center", fontweight="bold", fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Вторичные баллы")
    ax.set_title("Ожидание vs реальность на экзамене", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / "expected_vs_actual.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_ege_structure():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    donut(axes[0], [28, 17], ["Часть 1\n(1–20)", "Часть 2\n(21–26)"],
          [COLORS["primary"], COLORS["secondary"]], "45 первичных = 100 втор.", "45", "перв. баллов")
    donut(axes[1], [6, 4, 5, 2, 3], ["Механика\n(6)", "Молек.\n(4)", "Электро-\n(5)", "Квант.\n(2)", "Интегр.\n+метод.\n(3)"],
          plt.cm.Set2(np.linspace(0, 1, 5)), "Часть 1: блоки по Демидовой / КИМ", "20", "заданий")
    donut(axes[2], [3, 2, 2, 3, 3, 4], ["№21\n(3)", "№22\n(2)", "№23\n(2)", "№24\n(3)", "№25\n(3)", "№26\n(4)"],
          plt.cm.Pastel1(np.linspace(0, 1, 6)), "Часть 2: разбаловка 2026", "17", "перв. баллов")
    plt.tight_layout()
    plt.savefig(CHARTS / "ege_structure.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_behavior():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    donut(axes[0], [40, 35, 25], ["Невниматель-\nность", "Страх", "Спешка\n(2 ч)"],
          [COLORS["danger"], COLORS["warn"], COLORS["accent"]], "Экзаменационное поведение", "3", "фактора")
    donut(axes[1], [85, 15], ["Знания\n(пробники)", "Поведение\n(экзамен)"],
          [COLORS["success"], COLORS["danger"]], "Разрыв 80+ → 53: причина", "≈85%", "не в знаниях")
    donut(axes[2], [17, 28], ["Экзамен\n(17 перв.)", "Потенциал\n(≈28–33 перв.)"],
          [COLORS["warn"], COLORS["success"]], "Первичные баллы", "17", "из ~33 возможных")
    plt.tight_layout()
    plt.savefig(CHARTS / "behavior.png", dpi=180, bbox_inches="tight")
    plt.close()


def build_all():
    print("Generating physics charts...")
    chart_diagnostic_start()
    chart_gaps_7_10()
    chart_sections_studied()
    chart_thematic_controls()
    chart_mock_exam()
    chart_fipi_demidova()
    chart_exam_day()
    chart_exam_result()
    chart_expected_vs_actual()
    chart_ege_structure()
    chart_behavior()
    print(f"Done: {CHARTS}")


if __name__ == "__main__":
    build_all()
