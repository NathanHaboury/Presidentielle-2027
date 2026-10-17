"""Graphiques du chapitre Finances publiques.
Toutes les données sont sourcées dans le chapitre (finances_publiques.md) et en commentaire ci-dessous.
Valeurs « ≈ » = approximatives. Usage : python3 finances-publiques/scripts/charts.py
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
# 1. Déficit et dette depuis 1974
# ===========================================================================
def deficit_dette():
    sy = [1978, 1980, 1985, 1990, 1993, 1995, 2000, 2005, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
          2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    sv = [-1.7, -0.3, -3.1, -2.5, -6.5, -5.1, -1.3, -3.5, -3.0, -3.5, -7.4, -7.2, -5.3, -5.2, -4.9, -4.6,
          -3.9, -3.8, -3.4, -2.3, -2.4, -8.9, -6.6, -4.7, -5.4, -5.8, -5.1]
    dy = [1974, 1978, 1980, 1985, 1990, 1993, 1995, 2000, 2005, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
          2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    dv = [15.4, 21.2, 20.7, 30.6, 35.2, 46.0, 57.8, 59.7, 68.2, 65.5, 69.8, 84.1, 86.3, 88.7, 91.7, 94.6,
          96.2, 97.0, 98.1, 98.8, 98.5, 98.2, 114.9, 112.8, 111.4, 109.5, 112.6, 115.7]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.14, wspace=0.2)

    ax1.axhline(0, color=BASE, linewidth=1)
    ax1.axhline(-3, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    ax1.text(1979.3, -3.35, "Seuil UE : −3 %", fontsize=8.8, color=INK2, va="top")
    ax1.plot(sy, sv, color=BLUE, linewidth=2, marker="o", markersize=4, markeredgecolor=SURFACE,
             markeredgewidth=1)
    ax1.plot([2025, 2026, 2027], [-5.1, -5.4, -5.0], color=BLUE, linewidth=2, linestyle=(0, (4, 3)),
             marker="o", markersize=4, markerfacecolor=SURFACE)
    for x, y, t in [(2009, -7.4, "Crise\nfinancière"), (2020, -8.9, "Covid"), (1993, -6.5, "Récession\n1993")]:
        ax1.annotate(t, xy=(x, y), xytext=(x - 6.5, y - 0.4), fontsize=8.8, color=INK2,
                     arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax1.text(2026.3, -4.5, "Prév.\n2026-27", fontsize=8.5, color=INK2, ha="center")
    ax1.set_xlim(1973, 2029)
    ax1.set_ylim(-10.2, 1.2)
    ax1.set_ylabel("Solde public, % du PIB")
    ax1.set_title("A. Un déficit chaque année depuis 1975", pad=8)
    hgrid(ax1)

    ax2.axhline(60, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    ax2.text(1975, 62, "Plafond européen : 60 %", fontsize=8.8, color=INK2)
    ax2.plot(dy, dv, color=ORANGE, linewidth=2.2, marker="o", markersize=4, markeredgecolor=SURFACE,
             markeredgewidth=1)
    ax2.plot([2025, 2026, 2027], [115.7, 119.3, 121.7], color=ORANGE, linewidth=2.2, linestyle=(0, (4, 3)),
             marker="o", markersize=4, markerfacecolor=SURFACE)
    ax2.text(2027.3, 121.7, "122 %\n(2027)", fontsize=9, color=INK, va="center")
    ax2.text(1974.5, 19, "15 %\n(1974)", fontsize=9, color=INK)
    ax2.set_xlim(1973, 2031)
    ax2.set_ylim(0, 135)
    ax2.set_ylabel("Dette publique, % du PIB")
    ax2.set_title("B. La dette : de 15 % à plus de 115 % du PIB", pad=8)
    hgrid(ax2)
    finish(fig, "01_deficit_dette_1974_2027.png",
           "Un déficit chaque année depuis 1975 ; la dette augmente à chaque crise",
           "Solde et dette des administrations publiques, en % du PIB, 1974-2027. 2026-2027 : prévisions "
           "du projet de loi de finances 2027 (pointillés).",
           "Sources : Eurostat (1995-2024, notification d'avril 2026) ; Insee (2025, mai 2026) ; FMI, bases "
           "historiques (avant 1995, rupture de série) ; PLF 2027 (prévisions). Avant 2007 : années disponibles.")


# ===========================================================================
# 2. Où va la dépense publique (COFOG 2024)
# ===========================================================================
def depenses_fonctions():
    import numpy as np
    cats = ["Retraites (vieillesse\n+ survivants)", "Autre protection sociale\n(famille, chômage, RSA…)",
            "Santé", "Affaires économiques", "Enseignement", "Administration générale\n(hors intérêts)",
            "Intérêts de la dette", "Défense", "Ordre et sécurité", "Culture, sport, loisirs",
            "Logement, équipements", "Environnement"]
    fr = [14.8, 8.9, 8.9, 5.7, 5.1, 4.2, 2.0, 1.9, 1.8, 1.5, 1.4, 1.0]
    de = [11.8, 8.6, 7.6, 5.4, 4.5, 5.3, 1.1, 1.4, 1.6, 1.1, 0.5, 0.6]
    # Eurostat gov_10a_exp, 2024 (mise à jour du 16/09/2026). UE : santé 7,3 et enseignement 4,7 (vérifiés).
    eu = [12.2, 7.4, 7.3, 5.3, 4.7, 4.2, 1.9, 1.5, 1.7, 1.2, 0.7, 0.8]
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    fig.subplots_adjust(left=0.2, right=0.97, top=0.85, bottom=0.1)
    y = np.arange(len(cats))[::-1]
    h = 0.26
    for i, (vals, col, lab) in enumerate([(fr, BLUE, "France (total 57,3 %)"),
                                          (de, ORANGE, "Allemagne (49,4 %)"),
                                          (eu, AQUA, "Moyenne UE (48,9 %)")]):
        ax.barh(y + (1 - i) * (h + 0.02), vals, h, color=col, label=lab)
        if i == 0:
            for yy, v in zip(y, vals):
                ax.text(v + 0.15, yy + h + 0.02, f"{v:.1f}".replace(".", ","), va="center", fontsize=8.8,
                        color=INK)
    ax.set_yticks(y, cats)
    ax.set_xlim(0, 17)
    ax.set_xlabel("% du PIB (2024)")
    ax.legend(loc="lower right")
    vgrid(ax)
    finish(fig, "02_depenses_par_fonction_2024.png",
           "La France dépense 8,4 points de PIB de plus que la moyenne de l'UE, d'abord pour les retraites et la santé",
           "Dépenses des administrations publiques par fonction, en % du PIB, 2024. Écart avec l'UE (calcul) : "
           "retraites +2,6 points, santé +1,6.",
           "Source : Eurostat, dépenses des administrations publiques par fonction (COFOG), 2024 provisoire, "
           "mise à jour du 16 septembre 2026. Total France : 57,3 % du PIB (57,0 % selon l'Insee).")


# ===========================================================================
# 3. D'où vient l'argent (prélèvements 2024)
# ===========================================================================
def recettes():
    rows = [("Cotisations sociales", 482.3), ("Impôts sur le revenu des ménages\n(IR + CSG + CRDS)", 275.1),
            ("TVA", 206.3), ("Impôt sur les sociétés", 83.8), ("Impôts fonciers", 61.4),
            ("Accises (carburants, tabac…)", 59.1), ("Taxes sur les salaires", 58.0),
            ("Droits de succession et donations", 20.8), ("Autres", 22.4)]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    fig.subplots_adjust(left=0.26, right=0.95, top=0.82, bottom=0.12)
    ax.barh(range(len(rows)), [v for _, v in rows], color=BLUE, height=0.62)
    for i, (n, v) in enumerate(rows):
        ax.text(v + 5, i, f"{v:.0f} Md€  ({v / 1269.2 * 100:.0f} %)", va="center", fontsize=9.5, color=INK2)
    ax.set_yticks(range(len(rows)), [n for n, _ in rows])
    ax.set_xlim(0, 600)
    ax.set_xlabel("Milliards d'euros (2024)")
    vgrid(ax)
    finish(fig, "03_recettes_2024.png",
           "Cotisations sociales et impôts sur le revenu des ménages apportent ≈ 60 % des prélèvements",
           "Impôts et cotisations sociales des administrations publiques, en milliards d'euros, 2024 "
           "(total ≈ 1 269 Md€).",
           "Source : Eurostat, recettes fiscales des administrations publiques et des institutions de l'UE "
           "(gov_10a_taxag), 2024. Catégories européennes (la CSG est classée en impôt sur le revenu).")


# ===========================================================================
# 4. La charge de la dette
# ===========================================================================
def charge_dette():
    years = ["2023", "2024", "2025", "2026\n(prév.)", "2027\n(prév.)"]
    # Insee (2024-2025, mai 2026) ; 2023 calculé d'après l'Insee (+7,1 Md€ en 2024) ; PLF 2027 (2026-2027)
    vals = [51.1, 58.2, 64.7, 79.2, 91.2]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.17)
    cols = [ORANGE, ORANGE, ORANGE, "#f4a583", "#f4a583"]
    bars = ax.bar(years, vals, color=cols, width=0.6)
    for r, v in zip(bars, vals):
        ax.text(r.get_x() + r.get_width() / 2, v + 1.2, f"{v:.0f}", ha="center", fontsize=10, color=INK,
                fontweight="semibold")
    # Cour des comptes (25 juin 2026) : ≈ 100 Md€ en 2029
    b = ax.bar(["2029\n(Cour des\ncomptes)"], [100], color=SURFACE, edgecolor=ORANGE, hatch="///", width=0.6)
    ax.text(5, 101.5, "≈ 100", ha="center", fontsize=10, color=INK, fontweight="semibold")
    ax.set_xlim(-0.6, 5.6)
    ax.set_ylim(0, 112)
    ax.set_ylabel("Milliards d'euros (toutes administrations)")
    hgrid(ax)
    for sp in ["right"]:
        ax.spines[sp].set_visible(False)
    ax.set_clip_on(False)
    finish(fig, "04_charge_de_la_dette.png",
           "Les intérêts de la dette publique augmenteraient de 57 % entre 2024 et 2027",
           "Intérêts versés par l'ensemble des administrations publiques, en milliards d'euros. "
           "Hausse 2024-2027 : calcul.",
           "Sources : Insee (2024-2025, mai 2026) ; 2023 calculé d'après l'Insee ; projet de loi de finances "
           "2027 (2026-2027, prévisions) ; Cour des comptes, juin 2026 (2029, ordre de grandeur).")


# ===========================================================================
# 5. Impôts et cotisations en Europe (2024)
# ===========================================================================
# Eurostat, gov_10a_taxag, indicateur D2_D5_D91_D61_M_D995 (impôts et cotisations sociales, cotisations
# imputées comprises), % du PIB, 2024, mise à jour du 21/07/2026. Allemagne : provisoire.
PRELEVEMENTS_2024 = [
    ("Danemark", 45.5), ("France", 45.3), ("Belgique", 45.1), ("Autriche", 43.8), ("Luxembourg", 42.7),
    ("Italie", 42.5), ("Finlande", 42.3), ("Suède", 42.2), ("Grèce", 41.7), ("Allemagne", 40.9),
    ("Zone euro", 40.8), ("UE", 40.3),
]


def prelevements_europe():
    rows = PRELEVEMENTS_2024[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    fig.subplots_adjust(left=0.14, right=0.95, top=0.82, bottom=0.12)
    cols = [BLUE if n == "France" else (ORANGE if n in ("UE", "Zone euro") else BASE) for n, _ in rows]
    ax.barh(range(len(rows)), [v for _, v in rows], color=cols, height=0.62)
    for i, (n, v) in enumerate(rows):
        ax.text(v + 0.4, i, f"{v:.1f}".replace(".", ","), va="center", fontsize=9.5,
                color=INK if n == "France" else INK2, fontweight="semibold" if n == "France" else "normal")
    ax.set_yticks(range(len(rows)), [n for n, _ in rows])
    ax.set_xlim(0, 52)
    ax.set_xlabel("% du PIB (2024)")
    vgrid(ax)
    finish(fig, "05_prelevements_europe_2024.png",
           "Impôts et cotisations : la France est 2e de l'UE en 2024, à 0,2 point du Danemark",
           "Impôts et cotisations sociales, en % du PIB, 2024 : les dix pays les plus élevés de l'UE, "
           "la zone euro et l'UE.",
           "Source : Eurostat (gov_10a_taxag), mise à jour du 21 juillet 2026 ; Allemagne : provisoire. Définition "
           "européenne, cotisations imputées comprises : 45,3 % pour la France, contre 42,7 % selon l'Insee.")


if __name__ == "__main__":
    deficit_dette()
    depenses_fonctions()
    recettes()
    charge_dette()
    prelevements_europe()
    print("ok", sorted(p.name for p in OUT.glob("*.png")))
