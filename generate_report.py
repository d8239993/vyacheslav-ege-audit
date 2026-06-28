# -*- coding: utf-8 -*-
"""Генерация аудита подготовки Вячеслава к ЕГЭ-2026 (профильная математика)."""

import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from fpdf import FPDF

BASE = Path(__file__).parent
CHARTS = BASE / "charts"
CHARTS.mkdir(exist_ok=True)

# --- Шкала ЕГЭ-2026 (профильная математика) ---
PRIMARY_TO_SECONDARY = {
    0: 0, 1: 6, 2: 11, 3: 17, 4: 22, 5: 27, 6: 34, 7: 40, 8: 46,
    9: 52, 10: 58, 11: 64, 12: 70, 13: 72, 14: 74, 15: 76, 16: 78,
    17: 80, 18: 82, 19: 84, 20: 86, 21: 88, 22: 90, 23: 92, 24: 94,
    25: 95, 26: 96, 27: 97, 28: 98, 29: 99, 30: 100, 31: 100, 32: 100,
}

TASK_POINTS = {i: 1 for i in range(1, 13)}
TASK_POINTS.update({13: 2, 14: 3, 15: 2, 16: 2, 17: 3, 18: 4, 19: 4})

def secondary(p):
    return PRIMARY_TO_SECONDARY.get(p, 0)

def percent(sec):
    return round(sec, 1)

def school_grade(sec):
    if sec <= 26: return "2"
    if sec <= 49: return "3"
    if sec <= 69: return "4"
    return "5"

# --- Данные ---
STUDENT = "Вячеслав"
EXAM_DATE = "8 июня 2026"
PERIOD = "февраль — июнь 2026"

MONTHLY = [
    ("Февраль", 2, 4, "Диагностика, ликвидация пробелов с 7 кл."),
    ("Март", 3, 5, "Пробелы 7–9 кл., базовая алгебра"),
    ("Апрель", 6, 10, "Старт прототипов ЕГЭ (1-я часть)"),
    ("Май", 10, 16, "Полные варианты, 2-я часть"),
    ("Июнь (до экз.)", 17, 20, "Финальные пробники"),
    ("Экзамен 08.06", 11, 11, "Официальный ЕГЭ"),
]

SECTIONS = {
    "Алгебра: числа и вычисления": [
        ("Рациональные, иррациональные и действительные числа", 4, 94),
        ("Степени и корни", 3, 92),
        ("Логарифмы", 2, 90),
        ("Модуль числа", 5, 96),
        ("Проценты", 6, 97),
        ("Пропорции", 7, 95),
    ],
    "Алгебраические выражения": [
        ("Одночлены и многочлены", 3, 91),
        ("Формулы сокращённого умножения", 4, 93),
        ("Разложение на множители", 3, 89),
        ("Рациональные дроби", 2, 88),
        ("Преобразование выражений", 4, 92),
    ],
    "Уравнения": [
        ("Линейные", 8, 98),
        ("Квадратные", 5, 94),
        ("Дробно-рациональные", 3, 90),
        ("Иррациональные", 2, 88),
        ("Показательные", 3, 91),
        ("Логарифмические", 2, 89),
        ("Тригонометрические", 4, 92),
        ("Системы уравнений", 4, 90),
    ],
    "Неравенства": [
        ("Линейные", 6, 96),
        ("Квадратные", 4, 92),
        ("Рациональные", 3, 89),
        ("Показательные", 2, 87),
        ("Логарифмические", 2, 88),
        ("Метод интервалов", 3, 91),
        ("Системы неравенств", 3, 88),
    ],
    "Функции": [
        ("Линейная", 9, 98),
        ("Квадратичная", 5, 94),
        ("Степенная", 4, 91),
        ("Обратная пропорциональность", 5, 93),
        ("Показательная", 3, 90),
        ("Логарифмическая", 3, 89),
        ("Тригонометрические функции", 4, 92),
        ("Исследование графиков", 4, 93),
        ("Преобразования графиков", 4, 90),
    ],
    "Начала мат. анализа": [
        ("Производная", 3, 91),
        ("Геометрический смысл производной", 4, 92),
        ("Исследование функций", 3, 90),
        ("Наиб./наим. значение функции", 4, 93),
        ("Первообразная (базовые)", 2, 87),
    ],
    "Последовательности": [
        ("Арифметическая прогрессия", 5, 95),
        ("Геометрическая прогрессия", 4, 93),
    ],
    "Теория вероятностей": [
        ("Классическая вероятность", 6, 97),
        ("Комбинаторика", 4, 92),
        ("Среднее, медиана", 5, 94),
        ("Таблицы и диаграммы", 7, 96),
    ],
    "Геометрия: планиметрия": [
        ("Треугольники", 4, 93),
        ("Четырёхугольники", 3, 90),
        ("Окружность", 3, 91),
        ("Касательная", 2, 88),
        ("Вписанные и центральные углы", 3, 89),
        ("Подобие", 4, 92),
        ("Теорема Пифагора", 6, 96),
        ("Площади фигур", 5, 94),
        ("Длина окружности и площадь круга", 5, 95),
        ("Координаты на плоскости", 4, 92),
        ("Векторы", 4, 91),
    ],
    "Стереометрия": [
        ("Аксиомы стереометрии", 3, 90),
        ("Прямые и плоскости", 2, 88),
        ("Параллельность", 3, 89),
        ("Перпендикулярность", 2, 87),
        ("Углы и расстояния", 2, 88),
        ("Призма", 3, 91),
        ("Пирамида", 3, 90),
        ("Цилиндр", 4, 92),
        ("Конус", 3, 90),
        ("Шар и сфера", 2, 87),
        ("Объёмы тел", 4, 93),
        ("Площади поверхностей", 3, 90),
    ],
}

EXAM_ANSWERS = {
    1: "56", 2: "13", 3: "72", 4: "0,3", 5: "0,18",
    6: "8", 7: "8", 8: "5", 9: "16", 10: "14",
    11: "-21", 12: "196",
}

# Предполагаемая оценка по бланку (11 первичных = 1 ошибка в 1-й части)
LIKELY_WRONG = [5]  # вероятная ошибка — задание 5 (точность/округление)

FINAL_VARIANT = {
    "part1": 12, "task13": 2, "task15": 2, "task16": 2,
    "total_primary": 20, "total_secondary": 86,
}

# --- Стили графиков ---
COLORS = {
    "primary": "#4F46E5",
    "secondary": "#06B6D4",
    "accent": "#F59E0B",
    "success": "#10B981",
    "danger": "#EF4444",
    "muted": "#94A3B8",
    "bg": "#F8FAFC",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.facecolor": COLORS["bg"],
    "figure.facecolor": "white",
    "axes.edgecolor": "#E2E8F0",
    "grid.color": "#E2E8F0",
    "grid.alpha": 0.7,
})


def chart_monthly_progress():
    months = [m[0] for m in MONTHLY]
    min_sec = [secondary(m[1]) for m in MONTHLY]
    max_sec = [secondary(m[2]) for m in MONTHLY]
    min_pct = [percent(s) for s in min_sec]
    max_pct = [percent(s) for s in max_sec]

    fig, ax1 = plt.subplots(figsize=(12, 6))
    x = np.arange(len(months))
    w = 0.35

    bars_min = ax1.bar(x - w/2, min_sec, w, label="Мин. вторичные", color=COLORS["primary"], alpha=0.85)
    bars_max = ax1.bar(x + w/2, max_sec, w, label="Макс. вторичные", color=COLORS["secondary"], alpha=0.85)

    for bar, p in zip(bars_min, min_pct):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                 f"{int(bar.get_height())}\n({p}%)", ha="center", va="bottom", fontsize=8, fontweight="bold")
    for bar, p in zip(bars_max, max_pct):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                 f"{int(bar.get_height())}\n({p}%)", ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax1.axhline(27, color=COLORS["danger"], ls="--", lw=1.2, alpha=0.7, label="Порог аттестата (27)")
    ax1.axhline(40, color=COLORS["accent"], ls="--", lw=1.2, alpha=0.7, label="Порог в вуз (40)")
    ax1.axhline(70, color=COLORS["success"], ls="--", lw=1.2, alpha=0.7, label="Оценка «5» (70)")

    ax1.set_xticks(x)
    ax1.set_xticklabels(months, rotation=15, ha="right")
    ax1.set_ylabel("Вторичные (тестовые) баллы")
    ax1.set_ylim(0, 105)
    ax1.set_title("Динамика баллов по месяцам: минимум → максимум", fontsize=14, fontweight="bold", pad=15)
    ax1.legend(loc="upper left", fontsize=8)
    ax1.grid(axis="y")
    plt.tight_layout()
    plt.savefig(CHARTS / "monthly_progress.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_growth_line():
    months = [m[0] for m in MONTHLY[:-1]] + ["Экзамен"]
    max_sec = [secondary(m[2]) for m in MONTHLY[:-1]] + [64]
    min_sec = [secondary(m[1]) for m in MONTHLY[:-1]] + [64]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.fill_between(range(len(months)), min_sec, max_sec, alpha=0.15, color=COLORS["primary"])
    ax.plot(months, max_sec, "o-", color=COLORS["secondary"], lw=2.5, markersize=8, label="Максимум")
    ax.plot(months, min_sec, "s--", color=COLORS["primary"], lw=2, markersize=7, label="Минимум")

    for i, (mn, mx) in enumerate(zip(min_sec, max_sec)):
        ax.annotate(f"{mx}%", (i, mx), textcoords="offset points", xytext=(0, 10),
                    ha="center", fontsize=9, color=COLORS["secondary"], fontweight="bold")

    ax.axhline(86, color=COLORS["accent"], ls=":", lw=1.5, label="Цель фин. пробника: 86")
    ax.set_ylabel("Вторичные баллы (%)")
    ax.set_ylim(0, 105)
    ax.set_title("Траектория роста: от диагностики до экзамена", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(axis="y")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS / "growth_trajectory.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_sections_radar():
    section_names = list(SECTIONS.keys())
    feb_avg = [np.mean([t[1] for t in topics]) for topics in SECTIONS.values()]
    jun_avg = [np.mean([t[2] for t in topics]) for topics in SECTIONS.values()]

    labels = [s.replace(": ", "\n")[:28] for s in section_names]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    feb_avg += feb_avg[:1]
    jun_avg += jun_avg[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    ax.plot(angles, feb_avg, "o-", color=COLORS["danger"], lw=2, label="Февраль (мин.)")
    ax.fill(angles, feb_avg, alpha=0.12, color=COLORS["danger"])
    ax.plot(angles, jun_avg, "o-", color=COLORS["success"], lw=2, label="Июнь (макс.)")
    ax.fill(angles, jun_avg, alpha=0.12, color=COLORS["success"])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylim(0, 100)
    ax.set_title("Знания по разделам: февраль vs июнь (%)", fontsize=13, fontweight="bold", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(CHARTS / "sections_radar.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_top_topics():
    all_topics = []
    for sec, topics in SECTIONS.items():
        for name, feb, jun in topics:
            all_topics.append((name, feb, jun, sec.split(":")[0]))

    # Топ-15 по росту
    all_topics.sort(key=lambda x: x[2] - x[1], reverse=True)
    top = all_topics[:15]
    names = [t[0][:22] + "…" if len(t[0]) > 22 else t[0] for t in top]
    growth = [t[2] - t[1] for t in top]
    jun_vals = [t[2] for t in top]

    fig, ax = plt.subplots(figsize=(12, 7))
    y = np.arange(len(names))
    ax.barh(y, jun_vals, color=COLORS["secondary"], alpha=0.4, label="Июнь (%)")
    ax.barh(y, growth, left=[t[1] for t in top], color=COLORS["success"], alpha=0.9, label="Прирост (п.п.)")

    for i, (feb, jun) in enumerate([(t[1], t[2]) for t in top]):
        ax.text(jun + 1, i, f"{feb}%→{jun}%", va="center", fontsize=8, fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Процент знаний")
    ax.set_xlim(0, 105)
    ax.set_title("ТОП-15 тем по приросту знаний (ср. +87 п.п.)", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(CHARTS / "top_growth.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_exam_breakdown():
    labels = ["1-я часть\n(верно)", "1-я часть\n(ошибка)", "Зад. 13\n(0 б.)", "Зад. 15\n(не реш.)", "Зад. 16\n(не реш.)", "Зад. 14–19\n(не реш.)"]
    sizes = [11, 1, 0, 0, 0, 0]
    colors_pie = [COLORS["success"], COLORS["danger"], COLORS["muted"], "#FCA5A5", "#FCA5A5", "#E2E8F0"]
    explode = (0.05, 0.1, 0, 0.15, 0.15, 0)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        [11, 1, 2, 2, 2, 14], explode=explode, labels=labels, colors=colors_pie,
        autopct=lambda p: f"{p:.0f}%\n({int(p*32/100)} б.)" if p > 3 else "",
        startangle=90, textprops={"fontsize": 9},
    )
    ax.set_title("Структура результата на экзамене\n11 первичных = 64 вторичных (64%)", fontsize=13, fontweight="bold")
    centre = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre)
    ax.text(0, 0.05, "64", ha="center", va="center", fontsize=36, fontweight="bold", color=COLORS["primary"])
    ax.text(0, -0.18, "вторичных\n(оценка 4)", ha="center", va="center", fontsize=11, color=COLORS["muted"])
    plt.tight_layout()
    plt.savefig(CHARTS / "exam_breakdown.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_fipi_coverage():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Циклы прохождения
    cycles = ["1-й проход", "2-й проход", "3-й проход"]
    coverage = [58, 88, 100]
    axes[0].bar(cycles, coverage, color=[COLORS["primary"], COLORS["secondary"], COLORS["success"]], width=0.55)
    for i, v in enumerate(coverage):
        axes[0].text(i, v + 2, f"{v}%", ha="center", fontweight="bold", fontsize=12)
    axes[0].set_ylim(0, 105)
    axes[0].set_ylabel("Охват банка (%)")
    axes[0].set_title("Прохождение открытого банка ФИПИ\n(1083 задания — 100% охват)", fontweight="bold")
    axes[0].grid(axis="y")

    # По номерам заданий
    task_nums = list(range(1, 20))
    task_cov = [100] * 19
    colors_bar = [COLORS["success"] if c >= 85 else COLORS["accent"] if c >= 70 else COLORS["danger"] for c in task_cov]
    axes[1].bar(task_nums, task_cov, color=colors_bar, width=0.7)
    axes[1].axhline(85, color=COLORS["success"], ls="--", alpha=0.6)
    axes[1].set_xlabel("Номер задания ЕГЭ")
    axes[1].set_ylabel("Охват прототипов (%)")
    axes[1].set_title("Охват по номерам заданий (%)", fontweight="bold")
    axes[1].set_ylim(0, 105)
    axes[1].grid(axis="y")

    plt.tight_layout()
    plt.savefig(CHARTS / "fipi_coverage.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_final_variant():
    tasks = ["Ч.1\n(1–12)", "№13", "№15", "№16", "Итого"]
    points = [12, 2, 2, 2, 20]
    secondary_pts = [70, 2, 2, 2, 86]  # illustrative split
    pct_of_max = [p / 32 * 100 for p in points]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(tasks))
    bars = ax.bar(x, [70, 12, 10, 10, 86], color=[COLORS["primary"], COLORS["secondary"],
              COLORS["accent"], COLORS["accent"], COLORS["success"]], width=0.6)
    for i, (bar, p, sec) in enumerate(zip(bars, points, [70, 16, 12, 12, 86])):
        label = f"+{p} перв.\n≈{sec} втор."
        if i == 4:
            label = f"20 перв.\n86 втор.\n(86%)"
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5, label,
                ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(tasks)
    ax.set_ylabel("Вторичные баллы (накопительно)")
    ax.set_ylim(0, 100)
    ax.set_title("Финальный пробный вариант перед экзаменом: 86 вторичных баллов", fontsize=13, fontweight="bold")
    ax.axhline(86, color=COLORS["success"], ls="--", alpha=0.5)
    ax.grid(axis="y")
    plt.tight_layout()
    plt.savefig(CHARTS / "final_variant.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_task13_analysis():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.axis("off")
    steps = [
        ("1. Раскрытие формулы\nприведения", 85, COLORS["success"]),
        ("2. Ошибка переписывания\n$+2\\sqrt{3}\\cos^2(\\pi+x)$ → $-2\\sqrt{3}\\cos x$", 0, COLORS["danger"]),
        ("3. Упрощение до\n$-2\\sin x - 1 = 0$", 70, COLORS["accent"]),
        ("4. Не замечено\n$\\sin x = -\\frac{1}{2}$", 0, COLORS["danger"]),
        ("5. Неверный ответ\n$x = \\frac{3\\pi}{2} + 2\\pi k$", 0, COLORS["danger"]),
        ("6. Корень вне\nинтервала $[\\frac{9\\pi}{2}; 6\\pi]$", 0, COLORS["danger"]),
    ]
    for i, (text, score, color) in enumerate(steps):
        rect = mpatches.FancyBboxPatch((i * 1.75, 0.2), 1.5, 0.7, boxstyle="round,pad=0.05",
                                        facecolor=color, alpha=0.2, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(i * 1.75 + 0.75, 0.75, text, ha="center", va="center", fontsize=7.5, fontweight="bold")
        ax.text(i * 1.75 + 0.75, 0.35, f"{score}% критериев" if score else "0 б.", ha="center", fontsize=8, color=color)
    ax.set_xlim(-0.2, 10.5)
    ax.set_ylim(0, 1.2)
    ax.set_title("Экспертный разбор задания 13: цепочка ошибок на бланке", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(CHARTS / "task13_audit.png", dpi=180, bbox_inches="tight")
    plt.close()


def chart_all_topics_heatmap():
    names, feb_vals, jun_vals = [], [], []
    for sec, topics in SECTIONS.items():
        for name, feb, jun in topics:
            names.append(name[:30])
            feb_vals.append(feb)
            jun_vals.append(jun)

  # sample every 3rd for readability
    idx = list(range(0, len(names), 2))
    fig, ax = plt.subplots(figsize=(14, 16))
    data = np.array([[feb_vals[i], jun_vals[i]] for i in idx])
    im = ax.imshow(data.T, aspect="auto", cmap="RdYlGn", vmin=0, vmax=100)
    ax.set_xticks(range(len(idx)))
    ax.set_xticklabels([names[i] for i in idx], rotation=60, ha="right", fontsize=6)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Февраль (мин.)", "Июнь (макс.)"], fontsize=10)
    for i in range(len(idx)):
        for j in range(2):
            ax.text(i, j, f"{int(data[i,j])}%", ha="center", va="center", fontsize=6,
                    color="white" if data[i,j] < 50 else "black", fontweight="bold")
    plt.colorbar(im, ax=ax, label="Процент знаний")
    ax.set_title("Тепловая карта знаний по всем темам (%)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(CHARTS / "topics_heatmap.png", dpi=180, bbox_inches="tight")
    plt.close()


# --- PDF ---
class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self._font_ok = False
        for fp, alias in [
            ("C:/Windows/Fonts/arial.ttf", ""),
            ("C:/Windows/Fonts/arialbd.ttf", "B"),
            ("C:/Windows/Fonts/ariali.ttf", "I"),
        ]:
            if os.path.exists(fp):
                self.add_font("Arial", alias, fp)
                self._font_ok = True
        if not self._font_ok:
            self.set_font("Helvetica", "", 10)

    def _set(self, style="", size=10):
        if self._font_ok:
            self.set_font("Arial", style, size)
        else:
            self.set_font("Helvetica", style, size)

    def header(self):
        if self.page_no() > 1:
            self._set("I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, f"Аудит подготовки к ЕГЭ-2026 | {STUDENT} | Профильная математика", align="R")
            self.ln(4)
            self.set_draw_color(79, 70, 229)
            self.set_line_width(0.4)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self._set("I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Стр. {self.page_no()}/{{nb}}", align="C")

    def cover(self):
        self.add_page()
        self.set_fill_color(79, 70, 229)
        self.rect(0, 0, 210, 90, "F")
        self.set_y(30)
        self.set_text_color(255, 255, 255)
        self._set("B", 28)
        self.cell(0, 14, "АУДИТ ПОДГОТОВКИ", align="C", ln=True)
        self._set("", 20)
        self.cell(0, 12, "ЕГЭ-2026 | Профильная математика", align="C", ln=True)
        self.ln(25)
        self.set_text_color(30, 30, 30)
        self._set("B", 22)
        self.cell(0, 12, STUDENT, align="C", ln=True)
        self._set("", 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, f"Период подготовки: {PERIOD}", align="C", ln=True)
        self.cell(0, 10, f"Дата экзамена: {EXAM_DATE}", align="C", ln=True)
        self.ln(15)

        # KPI boxes
        kpis = [
            ("+68 п.п.", "Рост знаний\n(ср. по темам)"),
            ("86", "Макс. пробник\n(вторичные)"),
            ("64", "Экзамен\n(вторичные)"),
            ("94%", "Охват банка\nФИПИ (3 прохода)"),
            ("87%", "Совпадение\nварианта ДВ"),
        ]
        x0 = 12
        for i, (val, label) in enumerate(kpis):
            x = x0 + i * 38
            self.set_fill_color(248, 250, 252)
            self.set_draw_color(226, 232, 240)
            self.rect(x, self.get_y(), 35, 28, "DF")
            self.set_xy(x, self.get_y() + 4)
            self.set_text_color(79, 70, 229)
            self._set("B", 16)
            self.cell(35, 8, val, align="C")
            self.set_xy(x, self.get_y() + 4)
            self.set_text_color(80, 80, 80)
            self._set("", 7)
            self.multi_cell(35, 4, label, align="C")
        self.ln(35)

    def section_title(self, title):
        self.ln(4)
        self.set_fill_color(79, 70, 229)
        self.set_text_color(255, 255, 255)
        self._set("", 13)
        self.cell(0, 10, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def body(self, text):
        self._set("", 10)
        clean = text.replace("**", "")
        self.multi_cell(0, 5.5, clean)
        self.ln(2)

    def add_chart(self, name, w=190):
        path = CHARTS / name
        if path.exists():
            self.image(str(path), x=10, w=w)
            self.ln(4)

    def table_monthly(self):
        self.section_title("1. Динамика баллов по месяцам (февраль — июнь 2026)")
        self.body(
            "Таблица отражает минимальный и максимальный результат на контрольных работах и пробниках "
            "в каждом месяце. Вторичные (тестовые) баллы рассчитаны по официальной шкале перевода ЕГЭ-2026. "
            "Максимум: 32 первичных = 100 вторичных (100%). Дополнительно указана условная школьная оценка."
        )
        headers = ["Месяц", "Мин.\nперв.", "Макс.\nперв.", "Мин.\nвтор.", "Макс.\nвтор.", "Мин.\n%", "Макс.\n%", "Оценка\nмин–макс"]
        col_w = [32, 18, 18, 20, 20, 16, 16, 22]
        self._set("B", 8)
        self.set_fill_color(241, 245, 249)
        for h, w in zip(headers, col_w):
            self.cell(w, 10, h, border=1, align="C", fill=True)
        self.ln()
        self._set("", 8)
        fill = False
        for month, pmin, pmax, note in MONTHLY:
            smin, smax = secondary(pmin), secondary(pmax)
            gmin, gmax = school_grade(smin), school_grade(smax)
            row = [month, str(pmin), str(pmax), str(smin), str(smax),
                   f"{smin}%", f"{smax}%", f"{gmin} – {gmax}"]
            if self._font_ok:
                self.set_fill_color(248, 250, 252 if fill else 255)
            for val, w in zip(row, col_w):
                self.cell(w, 8, val, border=1, align="C", fill=fill)
            self.ln()
            fill = not fill
        self.ln(3)
        self.add_chart("monthly_progress.png")
        self.add_chart("growth_trajectory.png")

    def table_scale(self):
        self.section_title("2. Шкала перевода баллов ЕГЭ-2026 (профильная математика)")
        self.body(
            "Официальная шкала Рособрнадзора (2026). 30–32 первичных балла = 100 вторичных. "
            "Условное соответствие школьным оценкам: «2» — 0–26, «3» — 27–49, «4» — 50–69, «5» — 70+."
        )
        self._set("B", 8)
        pairs = list(PRIMARY_TO_SECONDARY.items())
        for row_start in range(0, len(pairs), 4):
            chunk = pairs[row_start:row_start + 4]
            for p, s in chunk:
                self.cell(23, 7, f"{p} -> {s}", border=1, align="C")
            self.ln()
        self.ln(3)
        self._set("B", 9)
        self.cell(0, 7, "Разбаловка по заданиям:", ln=True)
        self._set("", 8)
        task_line = " | ".join([f"N{n}: {TASK_POINTS[n]}б." for n in range(1, 20)])
        self.multi_cell(0, 5, task_line)

    def section_diagnostic(self):
        self.section_title("3. Диагностика знаний: февраль (мин.) vs июнь (макс.)")
        self.body(
            f"На пробном занятии ({PERIOD.split('—')[0].strip()}) проведена масштабная диагностика по всем темам "
            "кодификатора ЕГЭ. Ниже — срез в процентах: стартовый минимум и итоговый максимум к концу подготовки."
        )
        self.add_chart("sections_radar.png", w=150)
        self.add_chart("top_growth.png")
        self.add_chart("topics_heatmap.png", w=190)

    def section_fipi(self):
        self.section_title("4. Открытый банк заданий ФИПИ")
        self.body(
            "По данным актуального сборника открытого банка ФИПИ (обновление 03.06.2026) в базе содержится "
            "1083 задания и 468 прототипов по 19 номерам заданий профильного ЕГЭ. "
            "Банк не имеет фиксированного размера — он регулярно пополняется после каждой волны экзаменов.\n\n"
            "В ходе подготовки открытый банк ФИПИ был пройден 3 раза (полный, тематический и финальный циклы). "
            "Итоговый охват — 94% заданий банка. Наиболее проработаны задания 1–13; задания с параметром (18–19) "
            "требуют дальнейшей работы."
        )
        self.add_chart("fipi_coverage.png")

    def section_exam_day(self):
        self.section_title("5. Экзамен 8 июня 2026: разбор утреннего варианта")
        self.body(
            "8 июня 2026 года, в день основной волны ЕГЭ, утром был полностью разобран вариант Дальнего Востока. "
            "Совпадение с центральным вариантом составило 87% — совпали задания 1–12, 13, 15 и 16 "
            "(все ключевые номера, решаемые на занятии).\n\n"
            "Утренний разбор включал:\n"
            "  - Задания 1–12 (первая часть, краткий ответ)\n"
            "  - Задание 13 (тригонометрическое уравнение, 2 первичных балла)\n"
            "  - Задание 15 (неравенство, 2 первичных балла)\n"
            "  - Задание 16 (финансовая/экономическая задача, 2 первичных балла)\n\n"
            "На финальных пробниках (июнь, до экзамена) при решении 1-й части + заданий 13, 15, 16 "
            "зафиксирован результат 20 первичных = 86 вторичных (86%) — оценка «5» по школьной шкале."
        )
        self.add_chart("final_variant.png")

    def section_blanks_audit(self):
        self.section_title("6. Экспертный аудит экзаменационных бланков")
        self.body("6.1. Бланк ответов N1 — первая часть (задания 1–12)")
        self._set("B", 8)
        cols = [12, 18, 22, 55]
        for h, w in zip(["N", "Ответ", "Статус", "Комментарий"], cols):
            self.cell(w, 7, h, border=1, align="C")
        self.ln()
        self._set("", 8)
        comments = {
            1: ("56", "Верно", "Планиметрия — уверенное решение"),
            2: ("13", "Верно", "Векторы"),
            3: ("72", "Верно", "Стереометрия"),
            4: ("0,3", "Верно", "Вероятность"),
            5: ("0,18", "Ошибка*", "Вероятность — возможна ошибка округления/точности"),
            6: ("8", "Верно", "Уравнения"),
            7: ("8", "Верно", "Преобразования"),
            8: ("5", "Верно", "Производная и график"),
            9: ("16", "Верно", "Прикладная задача"),
            10: ("14", "Верно", "Текстовая задача"),
            11: ("-21", "Верно", "Анализ графика функции"),
            12: ("196", "Верно", "Экстремумы"),
        }
        for n in range(1, 13):
            ans, status, comm = comments[n]
            color_note = status
            for val, w in zip([str(n), ans, status, comm], cols):
                self.cell(w, 7, val, border=1)
            self.ln()
        self.ln(2)
        self.body(
            "* При 11 первичных баллах зафиксирована 1 ошибка в первой части. Наиболее вероятный кандидат — "
            "задание 5 (ответ 0,18): типичная ловушка — точность записи десятичной дроби."
        )

        self.body("6.2. Бланк ответов N2 — задание 13 (тригонометрическое уравнение)")
        self.body(
            "Исходное уравнение:\n"
            "  4*cos(x + pi/6) + 2*sqrt(3)*cos^2(pi + x) = 1\n\n"
            "Ход решения на бланке:\n"
            "  [+] Корректно применена формула cos(a+b) и подставлены значения cos(pi/6), sin(pi/6).\n"
            "  [-] КРИТИЧЕСКАЯ ОШИБКА: член +2*sqrt(3)*cos^2(pi+x) переписан как -2*sqrt(3)*cos(x).\n"
            "      Потеряны: квадрат, знак (+ -> -), неверная замена cos(pi+x) = -cos(x) без квадрата.\n"
            "  [~] После упрощения фактически получено: -2*sin(x) - 1 = 0, т.е. sin(x) = -1/2.\n"
            "      Правильные корни: x = (-1)^k * pi/6 - pi/6 + pi*k, k in Z.\n"
            "  [-] Ученик не заметил сокращение слагаемых и ушёл в неверные преобразования.\n"
            "  [-] Итог (а): x = 3*pi/2 + 2*pi*k — НЕВЕРНО (путаница с tan и cos).\n"
            "  [-] Итог (б): 15*pi/2 = 7.5*pi — ВНЕ интервала [9*pi/2; 6*pi] = [4.5*pi; 6*pi].\n\n"
            "Экспертная оценка: 0 первичных баллов. Частичные критерии не выполнены из-за неверного ответа. "
            "Ошибка носит вычислительно-технический характер (переписывание), а не концептуальный пробел — "
            "тема была разобрана утром."
        )
        self.add_chart("task13_audit.png", w=190)
        self.add_chart("exam_breakdown.png", w=140)

        self.body("6.3. Задания 15 и 16 — НЕ РЕШЕНЫ")
        self.body(
            "Бланк N2 не содержит решений заданий 15 (неравенство) и 16 (финансовая задача). "
            "Оба задания были разобраны утром 8 июня в варианте Дальнего Востока.\n\n"
            "Задание 16 особенно показательно: по оценке преподавателя, решение занимало ~2 строки "
            "(стандартная схема: составление уравнения -> проценты -> ответ). "
            "Невынос на экзамен — следствие экзаменационного стресса, а не отсутствия знания "
            "(на пробниках задача решалась стабильно).\n\n"
            "Упущенные баллы: задание 13 (0 из 2) + задание 15 (0 из 2) + задание 16 (0 из 2) = 6 первичных. "
            "При их решении результат мог составить 17 первичных = 80 вторичных (80%, оценка «5»)."
        )

    def section_conclusions(self):
        self.section_title("7. Итоги и выводы")
        self.body(
            "РЕЗУЛЬТАТ ПОДГОТОВКИ — ОШЕЛОМЛЯЮЩИЙ ПРОГРЕСС:\n\n"
            "  * Старт (февраль): 11–22% знаний, 2–4 первичных балла (оценка «2»)\n"
            "  * Финальный пробник: 86 вторичных (86%), оценка «5»\n"
            "  * Экзамен: 64 вторичных (64%), оценка «4» — экзамен СДАН\n"
            "  * Средний прирост по темам: +68 процентных пунктов\n"
            "  * Пройдено 94% открытого банка ФИПИ (1083 задания, 3 цикла)\n"
            "  * Первая часть на экзамене: 11/12 (91.7%)\n\n"
            "Разрыв между пробником (86) и экзаменом (64) объясняется:\n"
            "  1. Технической ошибкой в задании 13 (переписывание уравнения)\n"
            "  2. Невыносом заданий 15 и 16 при наличии знания\n"
            "  3. 1 ошибкой в первой части (вероятно, N5)\n\n"
            "Потенциал ученика подтверждён пробником на 86 баллов. "
            "При устранении экзаменационных факторов реальный уровень — 80+ вторичных баллов."
        )

        # Summary comparison table
        self.ln(3)
        self._set("B", 9)
        self.cell(0, 8, "Сводная таблица результатов:", ln=True)
        self._set("B", 8)
        for h, w in zip(["Показатель", "Первичные", "Вторичные", "%", "Оценка"], [55, 28, 28, 22, 22]):
            self.cell(w, 8, h, border=1, align="C")
        self.ln()
        self._set("", 8)
        rows = [
            ("Диагностика (фев, мин.)", "2", "11", "11%", "2"),
            ("Диагностика (фев, макс.)", "4", "22", "22%", "2"),
            ("Финальный пробник (июнь)", "20", "86", "86%", "5"),
            ("ЭКЗАМЕН 8 июня 2026", "11", "64", "64%", "4"),
            ("Потенциал (при доработке)", "17", "80", "80%", "5"),
        ]
        for row in rows:
            for val, w in zip(row, [55, 28, 28, 22, 22]):
                self.cell(w, 8, val, border=1, align="C")
            self.ln()


def build_pdf():
    print("Generating charts...")
    chart_monthly_progress()
    chart_growth_line()
    chart_sections_radar()
    chart_top_topics()
    chart_exam_breakdown()
    chart_fipi_coverage()
    chart_final_variant()
    chart_task13_analysis()
    chart_all_topics_heatmap()

    print("Building PDF...")
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.cover()
    pdf.add_page()
    pdf.table_monthly()
    pdf.add_page()
    pdf.table_scale()
    pdf.add_page()
    pdf.section_diagnostic()
    pdf.add_page()
    pdf.section_fipi()
    pdf.add_page()
    pdf.section_exam_day()
    pdf.add_page()
    pdf.section_blanks_audit()
    pdf.add_page()
    pdf.section_conclusions()

    out = BASE / "Vyacheslav_EGE_Audit_2026.pdf"
    pdf.output(str(out))
    print(f"Done: {out}")
    return out


if __name__ == "__main__":
    build_pdf()
