"""Graphiques de l'encadré « TotalEnergies : profits et impôts » (finances-publiques/encadre_totalenergies.md).
Toutes les données sont sourcées dans l'encadré. Usage : python3 scripts/charts_totalenergies.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# --- Police & encre --------------------------------------------------------
for f in font_manager.findSystemFonts():
    if "Inter" in f:
        font_manager.fontManager.addfont(f)
FONT = "Inter" if any("Inter" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASE = "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948")

plt.rcParams.update({
    "font.family": FONT, "font.size": 10.5, "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE, "xtick.color": MUTED, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlelocation": "left", "axes.titlesize": 12, "axes.titleweight": "semibold",
    "legend.frameon": False,
})


def finish(fig, name, title, subtitle, source):
    fig.suptitle(title, x=0.02, y=0.995, ha="left", va="top", fontsize=14.5, fontweight="bold", color=INK)
    h = fig.get_figheight()
    fig.text(0.02, 1 - 0.31 / h, subtitle, ha="left", va="top", fontsize=10.5, color=INK2)
    fig.text(0.02, 0.012, source, ha="left", va="bottom", fontsize=8.2, color=MUTED)
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


def hgrid(ax):
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def vgrid(ax):
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)



# ===========================================================================
# 1. Profits, impôts, versements aux actionnaires
# ===========================================================================
def total_profits_impots():
    import numpy as np
    years = ["2021", "2022", "2023", "2024", "2025"]
    adj = [18.06, 36.20, 23.18, 18.26, 15.59]   # résultat net ajusté (communiqués annuels)
    tax = [9.59, 22.24, 13.30, 10.78, 9.09]     # charge d'impôt sur les résultats, monde
    dist = [10.1, 17.0, 16.5, 15.7, 15.6]       # dividendes + rachats d'actions
    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.80, bottom=0.12)
    x = np.arange(len(years))
    w = 0.26
    series = [(adj, BLUE, "Résultat net ajusté"),
              (tax, ORANGE, "Charge d'impôt sur les résultats (comptes consolidés, monde)"),
              (dist, AQUA, "Versé aux actionnaires (dividendes + rachats d'actions)")]
    for i, (vals, col, lab) in enumerate(series):
        bars = ax.bar(x + (i - 1) * (w + 0.02), vals, w, color=col, label=lab)
        for r, v in zip(bars, vals):
            ax.text(r.get_x() + r.get_width() / 2, v + 0.5, f"{v:.1f}".replace(".", ","), ha="center", va="bottom",
                    fontsize=8.8, color=INK2)
    ax.set_xticks(x, years)
    ax.set_ylim(0, 42)
    ax.set_ylabel("Milliards de dollars")
    ax.legend(loc="upper right")
    hgrid(ax)
    finish(fig, "te_01_profits_impots_actionnaires.png",
           "De 2021 à 2025, sauf en 2022, TotalEnergies a versé plus à ses actionnaires que sa charge d'impôt sur les résultats",
           "En milliards de dollars. Charge d'impôt des comptes consolidés, monde entier (taux effectif ≈ 38 à 41 %). "
           "Au 1er semestre 2026 : 6,9 d'impôt, 6,5 versés.",
           "Sources : communiqués de résultats annuels TotalEnergies 2021-2025 (résultat net ajusté, charge "
           "d'impôt, dividendes et rachats d'actions). 2021 : rachats y compris plans salariés.")


# ===========================================================================
# 2. Bénéfices et impôts pays par pays (2023)
# ===========================================================================
def total_pays_par_pays():
    import numpy as np
    cats = ["Norvège", "Royaume-Uni", "Nigeria", "France",
            "« Reste du monde »\n(pays non détaillés,\ndont Suisse et Singapour)"]
    pbt = [5.19, 2.72, 1.95, -4.38, 9.19]
    tax = [4.90, 2.38, 1.20, -0.16, 0.73]
    notes = ["≈ 94 %", "≈ 88 %", "≈ 61 %", "perte comptable ;\nIS dû 0,14 Md\\$", "≈ 8 %"]
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    fig.subplots_adjust(left=0.2, right=0.96, top=0.82, bottom=0.12)
    y = np.arange(len(cats))[::-1]
    h = 0.36
    ax.barh(y + h / 2 + 0.01, pbt, h, color=BLUE, label="Bénéfice avant impôt")
    ax.barh(y - h / 2 - 0.01, tax, h, color=ORANGE, label="Impôt sur les sociétés payé")
    for yy, p, t, n in zip(y, pbt, tax, notes):
        ax.text(p + (0.15 if p >= 0 else -0.15), yy + h / 2, f"{p:.1f}".replace(".", ","), va="center",
                ha="left" if p >= 0 else "right", fontsize=9, color=INK2)
        ax.text(t + (0.15 if t >= 0 else -0.15), yy - h / 2, f"{t:.2f}".replace(".", ","), va="center",
                ha="left" if t >= 0 else "right", fontsize=9, color=INK2)
        ax.text(10.6, yy, n, va="center", fontsize=9.5, color=INK, fontweight="semibold")
    ax.text(10.6, len(cats) - 0.45, "Impôt / bénéfice", fontsize=9, color=MUTED, va="center")
    ax.axvline(0, color=BASE, linewidth=1)
    ax.set_yticks(y, cats)
    ax.set_xlim(-6, 12.6)
    ax.set_xlabel("Milliards de dollars (2023)")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", "−").replace(".", ",")))
    ax.legend(loc="lower left")
    vgrid(ax)
    finish(fig, "te_02_pays_par_pays_2023.png",
           "TotalEnergies paie l'essentiel de ses impôts dans les pays où il extrait du pétrole et du gaz",
           "Bénéfice avant impôt et impôt sur les sociétés payé, par pays, en 2023. Presque rien en France "
           "(pertes), peu dans les centres de négoce.",
           "Source : TotalEnergies, Tax Transparency Report 2023 (déclaration pays par pays). Impôt payé en "
           "trésorerie : décalages possibles d'une année sur l'autre. Total groupe : 28,6 Md\\$ de bénéfice, "
           "12,8 Md\\$ d'IS payé.")


if __name__ == "__main__":
    total_profits_impots()
    total_pays_par_pays()
    print("ok")
