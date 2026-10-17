"""Graphiques du chapitre « Travail et emploi ».
Les données sont sourcées en commentaire, et dans le chapitre (travail_emploi.md).
Usage, depuis la racine du dépôt : python3 travail-emploi/scripts/charts.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
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
    "hatch.color": INK2, "hatch.linewidth": 0.8,
})


def fr(v, d=1):
    """Nombre au format français (virgule décimale, signe moins typographique)."""
    return f"{v:.{d}f}".replace(".", ",").replace("-", "−")


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


def hbars(ax, rows, highlight, fmt, pad, others=BASE, special=None):
    """Barres horizontales triées ; rows = [(nom, valeur)], du plus haut au plus bas."""
    special = special or {}
    rows = rows[::-1]
    cols = []
    for n, _ in rows:
        if n in highlight:
            cols.append(BLUE)
        elif n in special:
            cols.append(special[n])
        else:
            cols.append(others)
    ax.barh(range(len(rows)), [v for _, v in rows], color=cols, height=0.66)
    for i, (n, v) in enumerate(rows):
        bold = n in highlight or n in special
        ax.text(v + pad, i, fmt(v), va="center", ha="left", fontsize=10,
                color=INK, fontweight="semibold" if bold else "normal")
    ax.set_yticks(range(len(rows)), [n for n, _ in rows])
    for lab in ax.get_yticklabels():
        if lab.get_text() in highlight or lab.get_text() in special:
            lab.set_fontweight("semibold")
            lab.set_color(INK)
    vgrid(ax)


# ===========================================================================
# 1. Le chômage depuis 1975 (graphique clé de « L'essentiel »)
# ===========================================================================
def chomage_long_terme():
    # France, taux de chômage au sens du BIT, moyenne annuelle, France hors Mayotte :
    # Insee, « L'essentiel sur… le chômage », séries longues, 7 août 2026
    # (https://www.insee.fr/fr/statistiques/4805248).
    fr_y = list(range(1975, 2026))
    fr_v = [3.6, 4.0, 4.5, 4.7, 5.3, 5.6, 6.6, 7.1, 7.4, 8.7, 9.1, 9.1, 9.2, 8.9, 8.2, 8.0, 8.2, 9.0, 10.0,
            10.6, 10.0, 10.5, 10.6, 10.2, 9.9, 8.5, 7.8, 7.9, 8.5, 8.9, 8.9, 8.9, 8.0, 7.4, 9.1, 9.3, 9.2,
            9.8, 10.3, 10.3, 10.4, 10.1, 9.4, 9.1, 8.5, 8.1, 7.9, 7.3, 7.4, 7.4, 7.7]
    assert len(fr_y) == len(fr_v)
    # 2e trimestre 2026, y compris Mayotte : Insee, Informations rapides n° 192 (7 août 2026).
    t2_2026 = 8.3
    # UE à 27, 15-74 ans, moyenne annuelle : Eurostat, série une_rt_a (mise à jour du 10 septembre 2026).
    ue_y = list(range(2015, 2026))
    ue_v = [10.2, 9.3, 8.3, 7.4, 6.8, 7.2, 7.1, 6.2, 6.1, 6.0, 6.0]

    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    fig.subplots_adjust(left=0.06, right=0.86, top=0.84, bottom=0.16)
    ax.plot(fr_y, fr_v, color=BLUE, linewidth=2.6, label="France")
    ax.plot(ue_y, ue_v, color=ORANGE, linewidth=2.2, label="Union européenne (27 pays)")
    ax.scatter([2026.4], [t2_2026], s=60, color=BLUE, edgecolor=SURFACE, linewidth=1.2, zorder=4)
    ax.text(2027.0, t2_2026 + 0.05, "8,3 %\n2e trim. 2026", va="center", ha="left", fontsize=10,
            color=BLUE, fontweight="semibold")
    ax.text(2027.0, 6.0, "UE : 6,0 %\n(2025)", va="center", ha="left", fontsize=10, color=ORANGE,
            fontweight="semibold")
    for y, v, dy in [(1994, 10.6, 0.35), (2015, 10.4, 0.35)]:
        ax.text(y, v + dy, f"{fr(v)} %", ha="center", fontsize=9.5, color=INK2)
    ax.text(1976.0, 3.4, "3,6 %", ha="left", va="center", fontsize=9.5, color=INK2)
    ax.text(2021.9, 6.8, "7,3 % (2022)", ha="left", va="center", fontsize=9.5, color=INK2)
    ax.set_xlim(1974, 2033)
    ax.set_ylim(0, 12)
    ax.set_xticks(list(range(1975, 2030, 5)))
    ax.set_ylabel("% des actifs")
    ax.legend(loc="upper left", fontsize=10)
    hgrid(ax)
    finish(fig, "01_chomage_long_terme.png",
           "Le chômage remonte depuis 2023 et reste au-dessus de la moyenne européenne",
           "Taux de chômage au sens du BIT, moyenne annuelle, en % des actifs ; point : 2e trimestre 2026 "
           "(Mayotte comprise)",
           "Sources : Insee, séries longues (août 2026) et Informations rapides n° 192 ; Eurostat, série une_rt_a "
           "(UE à 27, 15-74 ans).")


# ===========================================================================
# 2. Le taux d'emploi des 15-64 ans
# ===========================================================================
def taux_emploi():
    # Eurostat, série lfsi_emp_a, 15-64 ans, France (mise à jour du 10 septembre 2026).
    # Signe « d » (définition différente) à partir de 2021 (sens exact à vérifier dans les métadonnées).
    y = list(range(2003, 2026))
    v = [64.3, 64.2, 64.1, 64.1, 64.7, 65.2, 64.4, 64.3, 64.2, 64.3, 64.3, 64.4, 64.6, 64.9, 65.5, 66.0,
         66.2, 66.0, 67.2, 68.1, 68.4, 68.8, 69.3]
    assert len(y) == len(v)
    # 2e trimestre 2026 : Insee, Informations rapides n° 192.
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    fig.subplots_adjust(left=0.06, right=0.86, top=0.83, bottom=0.16)
    ax.plot(y[:19], v[:19], color=BLUE, linewidth=2.6)
    ax.plot(y[18:], v[18:], color=BLUE, linewidth=2.6, linestyle=(0, (4, 2)))
    ax.scatter([2026.4], [69.0], s=56, color=BLUE, edgecolor=SURFACE, linewidth=1.2, zorder=4)
    ax.text(2026.9, 69.0, "69,0 %\n2e trim. 2026", va="center", ha="left", fontsize=10, color=BLUE,
            fontweight="semibold")
    ax.text(2025, 69.75, "69,3 %", ha="center", fontsize=10, color=BLUE, fontweight="semibold")
    ax.text(2003, 64.75, "64,3 %", ha="center", fontsize=10, color=INK2)
    ax.annotate("Définition un peu différente\nselon Eurostat (depuis 2021)", xy=(2021, 67.2), xytext=(2015.4, 68.3),
                fontsize=9, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax.set_xlim(2002, 2030)
    ax.set_ylim(62, 71)
    ax.set_xticks(list(range(2003, 2027, 2)))
    ax.set_ylabel("% des 15-64 ans")
    hgrid(ax)
    finish(fig, "02_taux_emploi.png",
           "La part des 15-64 ans qui ont un emploi atteint un record en 2025",
           "Taux d'emploi des 15-64 ans en France, en % ; pointillés : définition un peu différente selon Eurostat "
           "à partir de 2021",
           "Sources : Eurostat, série lfsi_emp_a (enquête Emploi de l'Insee), mise à jour de septembre 2026 ; "
           "Insee, Informations rapides n° 192 (2e trimestre 2026).")


# ===========================================================================
# 3. Le chômage des jeunes en Europe
# ===========================================================================
def chomage_jeunes_europe():
    # Eurostat, Euro indicators du 1er octobre 2026 : taux de chômage des moins de 25 ans, août 2026,
    # données corrigées des variations saisonnières, France hors Mayotte.
    rows = [("Espagne", 22.7), ("France", 20.6), ("Italie", 20.3), ("Union européenne", 15.4),
            ("Zone euro", 15.0), ("Pays-Bas", 8.8), ("Allemagne", 7.4)]
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    fig.subplots_adjust(left=0.17, right=0.95, top=0.82, bottom=0.19)
    hbars(ax, rows, {"France"}, lambda v: f"{fr(v)} %", 0.3, special={"Union européenne": ORANGE})
    ax.set_xlim(0, 26)
    ax.set_xlabel("% des actifs de moins de 25 ans")
    finish(fig, "03_chomage_jeunes_europe.png",
           "Le chômage des jeunes actifs est plus élevé en France que dans la moyenne de l'UE",
           "Taux de chômage des moins de 25 ans en août 2026, en % des jeunes actifs (en emploi ou au chômage)",
           "Source : Eurostat, communiqué du 1er octobre 2026 (données mensuelles corrigées des variations "
           "saisonnières).")


# ===========================================================================
# 4. Les prélèvements de l'État sur l'assurance chômage
# ===========================================================================
def prelevements_unedic():
    # 2023-2026 : Unédic, Situation financière de l'Assurance chômage à horizon 2028 (17 juin 2026) :
    #   2,0 + 2,6 + 3,35 + 4,1 = 12,05 Md€ (« moindres compensations » des exonérations, arrêté du
    #   27 décembre 2023). 2027 : projet de loi de finances, non voté ; JeChange, 5 octobre 2026
    #   (source secondaire).
    yrs = ["2023", "2024", "2025", "2026\n(prévision)", "2027\n(projet de budget)"]
    v = [2.0, 2.6, 3.35, 4.1, 2.1]
    fig, ax = plt.subplots(figsize=(12.5, 4.7))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.83, bottom=0.2)
    x = np.arange(len(v))
    bars = ax.bar(x, v, 0.58, color=[BLUE] * 4 + [SURFACE], edgecolor=[BLUE] * 4 + [BLUE], linewidth=1.4)
    bars[-1].set_hatch("///")
    for r, val in zip(bars, v):
        d = 2 if val == 3.35 else 1
        ax.text(r.get_x() + r.get_width() / 2, val + 0.08, f"{fr(val, d)} Md€", ha="center", fontsize=10.5,
                color=INK, fontweight="semibold")
    ax.annotate("", xy=(3.32, 4.75), xytext=(-0.32, 4.75),
                arrowprops=dict(arrowstyle="-", color=INK2, linewidth=1))
    ax.text(1.5, 4.85, "12,05 Md€ de 2023 à 2026", ha="center", va="bottom", fontsize=10.5, color=INK2)
    ax.set_xticks(x, yrs)
    ax.set_ylim(0, 5.5)
    ax.set_ylabel("Milliards d'euros")
    hgrid(ax)
    finish(fig, "04_prelevements_unedic.png",
           "L'État a prélevé 12 Md€ sur les recettes de l'assurance chômage de 2023 à 2026",
           "Montant prélevé chaque année, en milliards d'euros ; barre hachurée : projet de budget pour 2027, "
           "non voté",
           "Sources : Unédic, situation financière à horizon 2028 (juin 2026) ; pour 2027, JeChange (octobre 2026), "
           "source secondaire.")


# ===========================================================================
# 5. La durée hebdomadaire du travail des salariés à temps plein
# ===========================================================================
def duree_hebdomadaire():
    # Eurostat, série lfsa_ewhun2, salariés à temps plein de 15 à 64 ans, durée habituelle, 2025
    # (mise à jour du 10 septembre 2026). France et Espagne : signe « d » (définition différente).
    # Valeurs de la France (38,8 h, signe « d ») et de la Suède (40,9 h) relues le 9 octobre 2026.
    # Points plutôt que barres : l'axe ne part pas de zéro (charte, section 5).
    rows = [("Suède", 40.9), ("Autriche", 40.6), ("Portugal", 40.5), ("Pologne", 40.4), ("Allemagne", 39.8),
            ("Union européenne", 39.5), ("Espagne", 39.2), ("Belgique", 38.9), ("Italie", 38.9),
            ("France", 38.8), ("Finlande", 38.3), ("Danemark", 38.0), ("Pays-Bas", 37.9)]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 5.9))
    fig.subplots_adjust(left=0.17, right=0.95, top=0.86, bottom=0.16)
    for i, (n, v) in enumerate(rows):
        col = BLUE if n == "France" else (ORANGE if n == "Union européenne" else INK2)
        big = n in ("France", "Union européenne")
        ax.hlines(i, 37.5, 41.6, color=GRID, linewidth=0.8, zorder=1)
        ax.scatter([v], [i], s=110 if big else 60, color=col, zorder=3)
        ax.text(v + 0.07, i, f"{fr(v)} h", va="center", ha="left", fontsize=10, color=INK,
                fontweight="semibold" if big else "normal")
    ax.set_yticks(range(len(rows)), [n for n, _ in rows])
    for lab in ax.get_yticklabels():
        if lab.get_text() in ("France", "Union européenne"):
            lab.set_fontweight("semibold")
            lab.set_color(INK)
    ax.set_xlim(37.5, 41.6)
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: fr(v)))
    ax.set_xlabel("Heures par semaine (l'axe commence à 37,5 heures)")
    vgrid(ax)
    finish(fig, "05_duree_hebdomadaire.png",
           "Un salarié à temps plein travaille 38,8 heures par semaine en France, un peu moins que dans l'UE",
           "Durée hebdomadaire habituelle des salariés à temps plein de 15 à 64 ans, en 2025, en heures",
           "Source : Eurostat, série lfsa_ewhun2 (enquêtes sur les forces de travail), mise à jour de septembre "
           "2026. France et Espagne : définition un peu différente.")


# ===========================================================================
# 6. Le coût horaire du travail en Europe
# ===========================================================================
def cout_horaire():
    # Gauche : Insee, « Coût horaire du travail dans l'Union européenne – données annuelles 2025 »
    #   (18 septembre 2026), d'après Eurostat ; secteur marchand non agricole hors services aux ménages,
    #   entreprises de 10 salariés ou plus. Belgique : 2024. Autriche : provisoire.
    # Droite : Eurostat, communiqué du 31 mars 2026 (ensemble de l'économie, 2025) : part des coûts non
    #   salariaux (cotisations patronales et taxes sur l'emploi, moins les subventions) dans le coût du travail.
    rows = [("Luxembourg", 56.2), ("Danemark", 53.3), ("Belgique (2024)", 48.0), ("Suède", 46.6),
            ("Autriche", 46.3), ("Pays-Bas", 46.2), ("Allemagne", 45.7), ("France", 44.7), ("Zone euro", 38.1),
            ("Union européenne", 34.7), ("Italie", 31.5), ("Espagne", 26.0), ("Pologne", 18.3),
            ("Bulgarie", 11.8)]
    share = [("France", 32.3), ("Suède", 31.7), ("Slovaquie", 28.6), ("Zone euro", 25.6),
             ("Union européenne", 24.8), ("Roumanie", 4.8)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6.0), gridspec_kw={"width_ratios": [1.35, 1]})
    fig.subplots_adjust(left=0.13, right=0.97, top=0.82, bottom=0.12, wspace=0.55)
    hbars(ax1, rows, {"France"}, lambda v: f"{fr(v)} €", 0.6, special={"Union européenne": ORANGE})
    ax1.set_xlim(0, 64)
    ax1.set_title("Coût d'une heure de travail, en euros (2025)", fontsize=11)
    hbars(ax2, share, {"France"}, lambda v: f"{fr(v)} %", 0.5, special={"Union européenne": ORANGE})
    ax2.set_xlim(0, 38)
    ax2.set_title("Part des cotisations patronales et taxes\nsur l'emploi dans ce coût, en %", fontsize=11)
    finish(fig, "06_cout_horaire.png",
           "Une heure de travail coûte plus cher en France que dans l'UE, et les cotisations y pèsent plus",
           "À gauche : entreprises de 10 salariés ou plus, hors agriculture et services aux ménages. À droite : "
           "ensemble de l'économie.",
           "Sources : Insee, d'après Eurostat (septembre 2026), à gauche ; Eurostat, communiqué du 31 mars 2026, "
           "à droite.")


if __name__ == "__main__":
    chomage_long_terme()
    taux_emploi()
    chomage_jeunes_europe()
    prelevements_unedic()
    duree_hebdomadaire()
    cout_horaire()
    print("Graphiques écrits dans", OUT)
