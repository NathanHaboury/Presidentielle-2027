"""Graphiques du chapitre « Défense et Europe ».
Les données sont sourcées en commentaire, et dans le chapitre (defense_europe.md).
Usage, depuis la racine du dépôt : python3 defense-europe/scripts/charts.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from pathlib import Path
import numpy as np

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
LIGHTBLUE = "#9cc3ef"
LIGHTGREY = "#e4e3dc"

plt.rcParams.update({
    "font.family": FONT, "font.size": 10.5, "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE, "xtick.color": MUTED, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlelocation": "left", "axes.titlesize": 12, "axes.titleweight": "semibold",
    "legend.frameon": False, "hatch.color": SURFACE, "hatch.linewidth": 1.2,
})


def fr(v, d=1):
    """Nombre au format français (virgule décimale, espace des milliers, signe moins typographique)."""
    return f"{v:,.{d}f}".replace(",", " ").replace(".", ",").replace("-", "−")


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
# 1. Budget des armées 2017-2030 (graphique clé de « L'essentiel »)
# ===========================================================================
def budget_armees():
    # Crédits de paiement de la mission « Défense », hors pensions, Md€ courants.
    # 2017-2023 : ministère des Armées, projet de loi de finances 2023, « LPM année 5 » (séries des lois de finances).
    # 2024-2030 : loi n° 2026-791 du 16 août 2026 actualisant la programmation militaire (texte adopté n° 325 de
    # l'Assemblée nationale, 1er juillet 2026), sauf 2027 : projet de loi de finances 2027 (63,4 Md€, ministère des
    # Armées, 8 octobre 2026 ; la loi prévoit 63,3 Md€).
    # Programmation initiale : loi n° 2023-703 du 1er août 2023 (2024-2030).
    yrs = list(range(2017, 2031))
    v = [32.3, 34.1, 35.8, 37.5, 39.2, 40.9, 43.9, 47.2, 50.5, 57.1, 63.4, 69.5, 72.6, 75.7]
    ini = {2024: 47.2, 2025: 50.5, 2026: 53.7, 2027: 56.9, 2028: 60.4, 2029: 63.9, 2030: 67.4}
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.06, right=0.98, top=0.82, bottom=0.14)
    for y, val in zip(yrs, v):
        if y <= 2026:
            ax.bar(y, val, color=BLUE, width=0.68)
        elif y == 2027:
            ax.bar(y, val, color=LIGHTBLUE, width=0.68, hatch="///")
        else:
            ax.bar(y, val, color=BASE, width=0.68, hatch="///")
        ax.text(y, val + 1.0, fr(val), ha="center", fontsize=9.6, color=INK,
                fontweight="semibold" if y in (2017, 2026, 2027, 2030) else "normal")
    ax.plot(list(ini.keys()), list(ini.values()), color=ORANGE, linewidth=2, linestyle=(0, (3, 2)),
            marker="o", markersize=4)
    handles = [Patch(facecolor=BLUE, label="Lois de finances votées"),
               Patch(facecolor=LIGHTBLUE, hatch="///", edgecolor=SURFACE, label="Projet de budget 2027 (non voté)"),
               Patch(facecolor=BASE, hatch="///", edgecolor=SURFACE, label="Programmation actualisée (loi du 16 août 2026)"),
               Line2D([0], [0], color=ORANGE, linewidth=2, linestyle=(0, (3, 2)), marker="o", markersize=4,
                      label="Programmation initiale (loi de 2023)")]
    ax.legend(handles=handles, loc="upper left", fontsize=9.4)
    ax.set_xticks(yrs, [str(y) for y in yrs])
    ax.set_ylim(0, 84)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: fr(x, 0)))
    hgrid(ax)
    finish(fig, "01_budget_armees.png",
           "Le budget des armées passe de 32 Md€ en 2017 à 63 Md€ prévus en 2027, en euros courants",
           "Crédits de la mission Défense, hors pensions, en milliards d'euros courants",
           "Sources : ministère des Armées (lois de finances 2017-2026 ; projet de loi de finances 2027) ; lois de programmation "
           "militaire du 1er août 2023 et du 16 août 2026.\nHors inflation, la hausse de 2017 à 2027 est d'environ 55 à 60 %, selon l'inflation de 2026-2027 (calcul, section 1.1). 2027 : projet de loi de finances, non voté.")


# ===========================================================================
# 2. Effort de défense de la France en % du PIB, 1960-2024
# ===========================================================================
def effort_long():
    # Banque mondiale, indicateur MS.MIL.XPND.GD.ZS (« Military expenditure (% of GDP) »), France,
    # mis à jour le 13 juillet 2026 (données du SIPRI). Valeurs annuelles 1960-2024.
    v = [5.43, 5.30, 5.16, 4.74, 4.54, 4.40, 4.29, 4.30, 4.14, 3.68, 3.46, 3.32, 3.23, 3.14, 3.09, 3.20, 3.16,
         3.23, 3.15, 3.14, 3.16, 3.25, 3.22, 3.24, 3.19, 3.14, 3.09, 3.12, 3.00, 2.92, 2.84, 2.85, 2.73, 2.72,
         2.69, 2.52, 2.44, 2.39, 2.25, 2.20, 2.09, 2.04, 2.06, 2.11, 2.11, 2.03, 1.98, 1.91, 1.90, 2.10, 1.97,
         1.89, 1.87, 1.85, 1.86, 1.87, 1.85, 1.85, 1.85, 1.85, 2.02, 1.98, 1.96, 1.95, 2.05]
    yrs = list(range(1960, 2025))
    assert len(v) == len(yrs)
    fig, ax = plt.subplots(figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.06, right=0.86, top=0.82, bottom=0.12)
    ax.fill_between(yrs, v, color=LIGHTBLUE, alpha=0.35, linewidth=0)
    ax.plot(yrs, v, color=BLUE, linewidth=2.6)
    ax.axhline(3.5, color=ORANGE, linewidth=1.6, linestyle=(0, (3, 2)))
    ax.text(2025.0, 3.5, "Objectif de l'OTAN\npour 2035 : 3,5 %", va="center", ha="left", fontsize=9.4, color=ORANGE)
    ax.axhline(2.0, color=INK2, linewidth=1.2, linestyle=(0, (2, 2)))
    ax.text(2025.0, 2.0, "Objectif de l'OTAN\nde 2014 : 2 %", va="center", ha="left", fontsize=9.4, color=INK2)
    for y, val, dy in [(1960, 5.43, 0.22), (1990, 2.84, 0.25), (2017, 1.85, -0.38), (2024, 2.05, 0.28)]:
        ax.plot(y, val, "o", color=BLUE, markersize=5)
        ax.text(y + (1.5 if y == 1960 else 0), val + dy, f"{y} : {fr(val, 2)} %", ha="left" if y == 1960 else "center",
                fontsize=9.6, color=INK, fontweight="semibold")
    ax.set_xlim(1958, 2025)
    ax.set_ylim(0, 6.2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: fr(x, 0) + " %"))
    hgrid(ax)
    finish(fig, "02_effort_long.png",
           "La part du PIB consacrée à la défense a été divisée par près de trois de 1960 à 2017",
           "Dépenses militaires de la France, en % du PIB, 1960-2024",
           "Source : Banque mondiale, indicateur « Military expenditure (% of GDP) », d'après les données du SIPRI, mise à jour du 13 juillet 2026. "
           "Définition proche de celle de l'OTAN (pensions comprises).")


# ===========================================================================
# 3. Dépenses de défense des alliés en 2025 (OTAN)
# ===========================================================================
def otan_2025():
    # OTAN, « Defence Expenditure of NATO Countries (2014-2025) », tableau 3, estimations 2025 (données au 3 juin 2025),
    # pour tous les pays sauf trois lignes mises à jour le 21 octobre 2026 avec les estimations de l'OTAN
    # du 7 juillet 2026, connues par la presse (le document de l'OTAN de 2026 n'a pas pu être lu) :
    # - France 2,04 % et alliés européens et Canada 2,31 % (2025) : Viralmag, 8 juillet 2026 ;
    # - Allemagne 2,22 % (2025) : Qatar Tribune, 8 juillet 2026 (absente du document de 2025).
    # Les autres valeurs de 2025 ont pu être révisées dans le document de 2026 (points incertains du chapitre).
    rows = [("Pologne", 4.48), ("Lituanie", 4.00), ("Lettonie", 3.73), ("Estonie", 3.38), ("Norvège", 3.35),
            ("États-Unis", 3.22), ("Danemark", 3.22), ("Grèce", 2.85), ("Pays-Bas", 2.49), ("Royaume-Uni", 2.40),
            ("Alliés européens et Canada", 2.31), ("Allemagne", 2.22), ("France", 2.04), ("Italie", 2.01),
            ("Canada", 2.01), ("Espagne", 2.00), ("Belgique", 2.00)]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 6.5))
    fig.subplots_adjust(left=0.2, right=0.84, top=0.84, bottom=0.1)
    cols = [BLUE if n == "France" else (INK2 if n.startswith("Alliés") else BASE) for n, _ in rows]
    ax.barh(range(len(rows)), [val for _, val in rows], color=cols, height=0.66)
    for i, (n, val) in enumerate(rows):
        bold = n == "France" or n.startswith("Alliés")
        ax.text(val + 0.05, i, fr(val, 2) + " %", va="center", fontsize=9.8, color=INK,
                fontweight="semibold" if bold else "normal", zorder=5,
                bbox=dict(facecolor=SURFACE, edgecolor="none", pad=0.6))
    ax.set_yticks(range(len(rows)), [n for n, _ in rows])
    for lab in ax.get_yticklabels():
        if lab.get_text() in ("France", "Alliés européens et Canada"):
            lab.set_fontweight("semibold")
            lab.set_color(INK)
    ax.axvline(3.5, color=ORANGE, linewidth=1.6, linestyle=(0, (3, 2)))
    ax.text(3.53, 0.4, "Objectif 2035 :\n3,5 % (plus jusqu'à\n1,5 % de dépenses liées)", fontsize=9.2, color=ORANGE, va="bottom")
    ax.axvline(2.0, color=INK2, linewidth=1.0, linestyle=(0, (2, 2)))
    ax.set_xlim(0, 5.2)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: fr(x, 0) + " %"))
    vgrid(ax)
    finish(fig, "03_otan_2025.png",
           "En 2025, l'effort de défense de la France est sous la moyenne des alliés européens et du Canada",
           "Dépenses de défense en % du PIB, définition de l'OTAN (pensions comprises), estimations 2025",
           "Source : OTAN, « Defence Expenditure of NATO Countries (2014-2025) », tableau 3 (données au 3 juin 2025).\n"
           "France, Allemagne et moyenne des alliés : estimations de l'OTAN de juillet 2026, d'après la presse (Viralmag, Qatar Tribune).")


# ===========================================================================
# 4. Aide à l'Ukraine en % du PIB (Institut de Kiel)
# ===========================================================================
def aide_ukraine():
    # Institut de Kiel, Ukraine Support Tracker, Release 31 (données jusqu'à août 2026, publiée le 7 octobre 2026),
    # explorateur de données (fichiers data_explorer.csv et eu_aid_shares.csv). Aide allouée du 24 janvier 2022
    # au dernier mois connu, en % du PIB de 2021. Part de l'UE : aide des institutions de l'UE attribuée à chaque
    # État membre au prorata de sa contribution au budget de l'UE (méthode de la note n° 217). Pas de part UE
    # pour les pays hors UE. La Facilité européenne pour la paix n'est pas comptée.
    rows = [("Danemark", 3.49, 0.68), ("Estonie", 3.07, 0.70), ("Norvège", 2.83, 0), ("Lituanie", 2.66, 0.64),
            ("Lettonie", 2.16, 0.68), ("Suède", 2.11, 0.62), ("Finlande", 1.51, 0.75), ("Pays-Bas", 1.31, 0.56),
            ("Pologne", 1.02, 0.69), ("Royaume-Uni", 0.86, 0), ("Allemagne", 0.86, 0.63), ("Belgique", 0.66, 0.76),
            ("États-Unis", 0.59, 0), ("France", 0.32, 0.77), ("Italie", 0.24, 0.77), ("Espagne", 0.22, 0.75)]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    fig.subplots_adjust(left=0.13, right=0.97, top=0.84, bottom=0.13)
    y = np.arange(len(rows))
    bil = [b for _, b, _ in rows]
    eu = [e for _, _, e in rows]
    c1 = [BLUE if n == "France" else INK2 for n, _, _ in rows]
    c2 = [LIGHTBLUE if n == "France" else LIGHTGREY for n, _, _ in rows]
    ax.barh(y, bil, color=c1, height=0.66)
    ax.barh(y, eu, left=bil, color=c2, height=0.66)
    for i, (n, b, e) in enumerate(rows):
        bold = n == "France"
        txt = fr(b, 2) + " %" + (f"  (+ {fr(e, 2)} % via l'UE)" if e else "")
        ax.text(b + e + 0.05, i, txt, va="center", fontsize=9.4, color=INK, fontweight="semibold" if bold else "normal")
    ax.set_yticks(y, [n for n, _, _ in rows])
    for lab in ax.get_yticklabels():
        if lab.get_text() == "France":
            lab.set_fontweight("semibold")
            lab.set_color(INK)
    ax.set_xlim(0, 5.4)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: fr(x, 0) + " %"))
    handles = [Patch(facecolor=INK2, label="Aide bilatérale (directe)"),
               Patch(facecolor=LIGHTGREY, label="Part attribuée de l'aide versée par les institutions de l'UE")]
    ax.legend(handles=handles, loc="lower right", fontsize=9.4)
    vgrid(ax)
    finish(fig, "04_aide_ukraine.png",
           "La France donne 0,3 % de son PIB à l'Ukraine en aide directe, 1,1 % avec sa part de l'aide de l'UE",
           "Aide allouée à l'Ukraine depuis janvier 2022 (militaire, financière, humanitaire), en % du PIB de 2021",
           "Source : Institut de Kiel, Ukraine Support Tracker, données jusqu'à août 2026 (publiées le 7 octobre 2026). "
           "Hors Facilité européenne pour la paix. La part de l'UE n'est calculée que pour les États membres.")


# ===========================================================================
# 5. Ce que la France verse au budget de l'UE et ce qu'elle reçoit, 2015-2025
# ===========================================================================
def budget_ue():
    # Commission européenne, « EU spending and revenue », fichier eu_budget_spending_and_revenue_2000-2025.xlsx.
    # Contribution (calcul) = ressources propres totales − droits de douane − cotisations sucre + soldes et ajustements.
    # Dépenses = « TOTAL EXPENDITURE » en France ; plan de relance = « TOTAL NGEU » (à partir de 2021).
    yrs = list(range(2015, 2026))
    contrib = [19.0, 20.5, 16.2, 20.6, 21.0, 23.7, 26.4, 24.2, 23.9, 22.3, 23.0]
    dep = [14.5, 11.3, 13.5, 15.0, 15.1, 15.8, 15.7, 16.9, 16.5, 16.5, 16.4]
    ngeu = [0, 0, 0, 0, 0, 0, 5.6, 8.2, 12.3, 8.9, 2.2]
    x = np.arange(len(yrs))
    w = 0.38
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.06, right=0.98, top=0.82, bottom=0.14)
    ax.bar(x - w / 2, contrib, width=w, color=BLUE)
    ax.bar(x + w / 2, dep, width=w, color=BASE)
    ax.bar(x + w / 2, ngeu, width=w, bottom=dep, color=AQUA)
    for i in range(len(yrs)):
        ax.text(x[i] - w / 2, contrib[i] + 0.5, fr(contrib[i]), ha="center", fontsize=8.8, color=INK, fontweight="semibold")
        top = dep[i] + ngeu[i]
        ax.text(x[i] + w / 2, top + 0.5, fr(top), ha="center", fontsize=8.8, color=INK2)
    handles = [Patch(facecolor=BLUE, label="Ce que la France verse (contribution nationale)"),
               Patch(facecolor=BASE, label="Dépenses de l'UE en France, hors plan de relance"),
               Patch(facecolor=AQUA, label="Plan de relance européen (NextGenerationEU)")]
    ax.legend(handles=handles, loc="upper left", fontsize=9.4)
    ax.set_xticks(x, [str(y) for y in yrs])
    ax.set_ylim(0, 36)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: fr(v, 0)))
    hgrid(ax)
    finish(fig, "05_budget_ue.png",
           "La France verse plus au budget de l'UE qu'elle n'en reçoit, sauf en 2022-2024 avec le plan de relance",
           "Contribution de la France et dépenses de l'UE en France, en milliards d'euros courants",
           "Source : Commission européenne, « EU spending and revenue » (données 2000-2025) ; calculs du chapitre. "
           "Droits de douane non comptés dans la contribution.\nLe plan de relance sera remboursé par le budget de l'UE de 2028 à 2058.")


if __name__ == "__main__":
    budget_armees()
    effort_long()
    otan_2025()
    aide_ukraine()
    budget_ue()
    print("Graphiques écrits dans", OUT)
