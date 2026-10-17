"""Graphiques du chapitre « Pouvoir d'achat, salaires et inégalités ».
Toutes les données sont sourcées dans le chapitre (pouvoir_achat.md) et en commentaire ci-dessous.
Version du 10 octobre 2026 : six graphiques.
"""
import math
import numpy as np
import matplotlib.ticker
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
# 1. Pouvoir d'achat par unité de consommation, 2000-2025 (graphique clé)
# Sources : Insee, France, portrait social 2024 (base 2020), niveaux 2000-2013 ;
# Insee, « Données diverses sur les ménages en 2025 » (comptes de mai 2026), évolutions 2014-2025.
# Indice 2000 = 100 calculé par chaînage.
# ===========================================================================
IDX = {2000: 100.0, 2001: 102.5, 2002: 104.9, 2003: 105.3, 2004: 106.8, 2005: 107.8, 2006: 110.4, 2007: 112.9,
       2008: 112.5, 2009: 113.7, 2010: 114.5, 2011: 114.1, 2012: 113.0, 2013: 111.1, 2014: 111.9, 2015: 112.4,
       2016: 113.5, 2017: 114.9, 2018: 115.2, 2019: 117.5, 2020: 117.1, 2021: 120.4, 2022: 120.1, 2023: 120.5,
       2024: 123.2, 2025: 122.3}
G = {2001: 2.4, 2002: 2.3, 2003: 0.4, 2004: 1.4, 2005: 0.9, 2006: 2.4, 2007: 2.3, 2008: -0.4, 2009: 1.1,
     2010: 0.7, 2011: -0.4, 2012: -0.9, 2013: -1.7, 2014: 0.7, 2015: 0.4, 2016: 1.0, 2017: 1.2, 2018: 0.3,
     2019: 2.0, 2020: -0.3, 2021: 2.8, 2022: -0.3, 2023: 0.4, 2024: 2.2, 2025: -0.7}
# Phases : Insee, blog (Hauseux et Houriez, 2025) pour 2000-2021 ; 2022-2025 calculé.
PHASES = [(2000, 2007, "+1,7 % par an"), (2007, 2013, "−0,3 % par an"), (2013, 2021, "+1,0 % par an"),
          (2021, 2025, "+0,4 % par an")]


def annuel():
    years = list(range(2000, 2026))
    idx = [IDX[y] for y in years]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.5, 4.9), sharex=True,
                                   gridspec_kw={"height_ratios": [1.25, 1]})
    fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.11, hspace=0.28)
    ax1.plot(years, idx, color=BLUE, linewidth=2.6)
    ax1.fill_between(years, 100, idx, color=BLUE, alpha=0.08)
    for y in (2007, 2013, 2024, 2025):
        v = IDX[y]
        ax1.plot(y, v, "o", color=BLUE, markersize=6, markeredgecolor=SURFACE)
        dy = -2.4 if y in (2013, 2025) else 1.3
        ax1.text(y, v + dy, f"{v:.1f}".replace(".", ","), ha="center", fontsize=9.5, color=BLUE,
                 fontweight="semibold")
    # Phases
    for a, b, lab in PHASES:
        ax1.annotate("", xy=(b, 98.6), xytext=(a, 98.6),
                     arrowprops=dict(arrowstyle="<->", color=MUTED, linewidth=0.9, shrinkA=0, shrinkB=0))
        ax1.text((a + b) / 2, 99.2, lab, ha="center", va="bottom", fontsize=9, color=INK2)
    ax1.set_ylim(96, 127)
    ax1.set_ylabel("Indice (2000 = 100)")
    ax1.set_title("Niveau du pouvoir d'achat par unité de consommation, et rythme moyen par période", color=INK)
    hgrid(ax1)
    vals = [G[y] for y in years[1:]]
    cols = [BLUE if v >= 0 else ORANGE for v in vals]
    ax2.bar(years[1:], vals, color=cols, width=0.72)
    for y, v in zip(years[1:], vals):
        ax2.text(y, v + (0.12 if v >= 0 else -0.12), f"{v:+.1f}".replace(".", ","), ha="center",
                 va="bottom" if v >= 0 else "top", fontsize=8, color=INK2)
    ax2.axhline(0, color=INK2, linewidth=0.8)
    ax2.set_ylim(-2.6, 3.6)
    ax2.set_ylabel("Variation annuelle (%)")
    ax2.set_title("Variation d'une année sur l'autre", color=INK)
    hgrid(ax2)
    ax2.set_xticks(list(range(2001, 2026, 2)))
    finish(fig, "01_pouvoir_achat_annuel.png",
           "Le pouvoir d'achat moyen a augmenté de 22 % depuis 2000, avec des années de baisse",
           "Pouvoir d'achat du revenu disponible brut des ménages par unité de consommation (France) : indice 2000 = 100 et variation annuelle en %",
           "Sources : Insee, comptes nationaux base 2020 (France, portrait social 2024 jusqu'en 2013, "
           "comptes de mai 2026 ensuite). 2025 provisoire. Indice et rythme 2022-2025 calculés ; rythmes 2000-2021 : blog de l'Insee (2025).")


# ===========================================================================
# 3. Dépenses pré-engagées
# Source : Insee, France, portrait social 2025, « Consommation et épargne des ménages », figure 2 (base 2020).
# ===========================================================================
def preengagees():
    yrs = [1960, 1980, 2000, 2015, 2023, 2024]
    tot = [13.5, 22.6, 28.1, 31.0, 30.3, 30.3]
    log = [10.7, 16.8, 21.4, 24.7, 22.8, 22.8]
    fig, ax = plt.subplots(figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.07, right=0.8, top=0.8, bottom=0.12)
    ax.plot(yrs, tot, color=ORANGE, linewidth=1.6, linestyle=(0, (4, 3)), marker="o", markersize=7, markeredgecolor=SURFACE)
    ax.fill_between(yrs, 0, tot, color=ORANGE, alpha=0.1)
    for y, v in zip(yrs, tot):
        if y in (1960, 1980, 2000, 2015):
            ax.text(y, v + 1.2, f"{v:.1f} %".replace(".", ","), ha="center", fontsize=10, color=ORANGE,
                    fontweight="semibold")
    ax.plot(yrs, log, color=INK2, linewidth=1.2, linestyle=(0, (2, 3)), marker="o", markersize=5)
    ax.text(2025.5, 21.0, "dont logement :\n22,8 % en 2024\n(loyers, y compris\nloyers imputés,\nénergie, eau…)",
            fontsize=9, color=INK2, va="center")
    ax.text(2025.5, 31.5, "Total des dépenses\npré-engagées :\n30,3 % en 2024", fontsize=10, color=ORANGE,
            fontweight="semibold", va="center")
    ax.set_ylim(0, 36)
    ax.set_xlim(1957, 2025)
    ax.set_ylabel("% du revenu disponible brut")
    hgrid(ax)
    finish(fig, "03_depenses_preengagees.png",
           "Près d'un tiers du revenu part dans des dépenses difficiles à réduire à court terme",
           "Part des dépenses « pré-engagées » (logement, énergie, télécommunications, assurances, cantine…) "
           "dans le revenu disponible des ménages",
           "Source : Insee, France, portrait social 2025 (comptes nationaux, base 2020). Points publiés : 1960, 1980, "
           "2000, 2015 (maximum), 2023 et 2024, reliés par des pointillés. Les loyers imputés des propriétaires sont inclus.")


# ===========================================================================
# 2. Prix par poste et inflation perçue
# Gauche : Insee, indices des prix à la consommation en moyenne annuelle (bilans 2022, 2023 et 2025), cumul calculé.
# Droite : Banque de France, Bulletin n° 265-4 (juillet 2026), enquêtes auprès des ménages ; inflation réalisée =
# indice harmonisé (IPCH) sur 12 mois au moment de chaque enquête.
# ===========================================================================
def prix():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.6), gridspec_kw={"width_ratios": [1, 1.1]})
    fig.subplots_adjust(left=0.15, right=0.98, top=0.78, bottom=0.12, wspace=0.32)
    cats = ["Produits manufacturés", "Ensemble des prix", "Alimentation", "Tabac", "Énergie"]
    v = [6.3, 13.6, 22.5, 24.3, 25.5]
    cols = [BASE, INK2, ORANGE, BASE, ORANGE]
    ax1.barh(cats, v, color=cols, height=0.62)
    for i, val in enumerate(v):
        ax1.text(val + 0.5, i, f"+{val:.1f} %".replace(".", ","), va="center", fontsize=10, color=INK,
                 fontweight="semibold" if cats[i] in ("Alimentation", "Énergie", "Ensemble des prix") else None)
    ax1.set_xlim(0, 31)
    ax1.set_title("Hausse des prix entre 2021 et 2025", color=INK)
    vgrid(ax1)
    ax1.tick_params(axis="y", labelsize=10)
    yrs = ["2022", "2023", "2024", "2025"]
    med = [6, 10, 5, 5]
    moy = [10.3, 14.1, 9.1, 9.5]
    mes = [6.2, 6.7, 1.6, 0.8]
    x = np.arange(4)
    w = 0.26
    ax2.bar(x - w, mes, w, color=INK2, label="Mesurée (indice harmonisé, sur 12 mois)")
    ax2.bar(x, med, w, color=ORANGE, label="Perçue : médiane")
    ax2.bar(x + w, moy, w, color=YELLOW, label="Perçue : moyenne")
    for xi, a, b, c in zip(x, mes, med, moy):
        for dx, val in ((-w, a), (0, b), (w, c)):
            ax2.text(xi + dx, val + 0.25, f"{val:g}".replace(".", ","), ha="center", fontsize=8.6, color=INK2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(yrs)
    ax2.set_ylim(0, 20)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f"{x:g}".replace(".", ",")))
    ax2.set_ylabel("Inflation sur 12 mois (%)")
    ax2.set_title("Inflation mesurée et inflation perçue, à la date de l'enquête", color=INK)
    ax2.legend(loc="upper right", fontsize=9)
    hgrid(ax2)
    finish(fig, "02_prix_et_inflation_percue.png",
           "Énergie, tabac et alimentation ont augmenté plus vite que les autres prix, et l'inflation perçue dépasse l'inflation mesurée",
           "Gauche : variation des prix moyens de 2025 par rapport à 2021. Droite : inflation des 12 derniers mois, "
           "mesurée et déclarée par les ménages",
           "Sources : Insee (indice des prix à la consommation, moyennes annuelles ; cumuls calculés) ; Banque de "
           "France, Bulletin n° 265-4 (juillet 2026), enquêtes de 2022 à 2025 auprès de plus de 4 000 ménages.")


# ===========================================================================
# 4. Distribution des salaires du privé
# Source : Insee, Insee Première n° 2079 (octobre 2025), salaires nets en équivalent temps plein, 2024 ;
# évolutions 1996-2024 en euros constants.
# ===========================================================================
def salaires_distribution():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.6), gridspec_kw={"width_ratios": [1.15, 1]})
    fig.subplots_adjust(left=0.07, right=0.97, top=0.78, bottom=0.18, wspace=0.3)
    lab = ["10 % les\nmoins payés\n(D1)", "Médiane", "Moyenne", "10 % les\nmieux payés\n(D9)",
           "5 % les\nmieux payés", "1 % les\nmieux payés"]
    v = [1492, 2190, 2733, 4334, 5593, 10261]
    cols = [BLUE, BLUE, INK2, BLUE, BLUE, VIOLET]
    ax1.bar(range(6), v, color=cols, width=0.62)
    for i, val in enumerate(v):
        ax1.text(i, val + 180, f"{val:,} €".replace(",", " "), ha="center", fontsize=9.8, color=INK,
                 fontweight="semibold")
    ax1.set_xticks(range(6))
    ax1.set_xticklabels(lab, fontsize=8.8)
    ax1.set_ylim(0, 11800)
    ax1.set_title("Salaire net mensuel en équivalent temps plein, 2024\n(seuils : D1 = 10 % gagnent moins)",
                  color=INK, fontsize=11)
    ax1.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f"{x/1000:.0f} k€"))
    hgrid(ax1)
    lab2 = ["D1", "Médiane", "Moyenne", "D9"]
    g = [17.8, 12.7, 13.9, 13.3]
    ax2.bar(lab2, g, color=[ORANGE, BLUE, INK2, BLUE], width=0.6)
    for i, val in enumerate(g):
        ax2.text(i, val + 0.4, f"+{val:.1f} %".replace(".", ","), ha="center", fontsize=10.5, color=INK,
                 fontweight="semibold")
    ax2.set_ylim(0, 21)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f"{x:g}".replace(".", ",")))
    ax2.set_title("Hausse en euros constants, 1996 → 2024", color=INK, fontsize=11)
    hgrid(ax2)
    finish(fig, "04_salaires_distribution.png",
           "Les plus bas salaires ont augmenté plus vite que les autres depuis 1996",
           "Distribution des salaires nets du secteur privé (équivalent temps plein) et évolution en euros constants",
           "Sources : Insee, Insee Première n° 2079 (octobre 2025) ; hausse de la moyenne : Insee, « L'essentiel sur… les salaires » (janvier 2026). "
           "Rapport D9/D1 : 2,91 en 2024, contre 3,02 en 1996.")


# ===========================================================================
# 5. Redistribution : Gini avant et après transferts
# Source : Eurostat, EU-SILC 2025 (revenus 2024), ilc_di12 (après) et ilc_di12c (avant transferts,
# retraites comptées comme revenus), mise à jour du 5 octobre 2026.
# ===========================================================================
def redistribution():
    pays = ["Belgique", "Pays-Bas", "UE à 27", "Espagne", "Italie", "Allemagne", "France"]
    av = [30.9, 31.7, 34.1, 34.1, 35.1, 36.0, 37.4]
    ap = [23.4, 25.9, 29.2, 30.8, 31.0, 30.1, 30.4]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.8, bottom=0.13)
    y = np.arange(len(pays))
    cols = [BLUE if p == "France" else INK2 for p in pays]
    for yi, a, b, c in zip(y, av, ap, cols):
        ax.plot([b, a], [yi, yi], color=GRID, linewidth=6, solid_capstyle="round", zorder=1)
        ax.scatter([a], [yi], facecolor=SURFACE, edgecolor=c, linewidth=2, s=70, zorder=3)
        ax.scatter([b], [yi], color=c, s=70, zorder=3)
        ax.text(a + 0.5, yi, f"{a:.1f}".replace(".", ","), va="center", fontsize=9.5, color=c)
        ax.text(b - 0.5, yi, f"{b:.1f}".replace(".", ","), va="center", ha="right", fontsize=9.5, color=c)
    ax.scatter([], [], facecolor=SURFACE, edgecolor=INK2, linewidth=2, s=70,
               label="Avant impôts et prestations (retraites comptées comme des revenus)")
    ax.scatter([], [], color=INK2, s=70, label="Après impôts et prestations")
    ax.set_yticks(y)
    ax.set_yticklabels(pays, fontsize=10.5)
    for tl in ax.get_yticklabels():
        if tl.get_text() == "France":
            tl.set_fontweight("bold")
    ax.set_xlim(18, 42)
    ax.set_xlabel("Indice de Gini (0 = égalité parfaite, 100 = une personne a tout)")
    ax.set_ylim(-1.7, 6.5)
    ax.legend(loc="lower center", fontsize=9, ncol=2)
    vgrid(ax)
    finish(fig, "05_redistribution_gini.png",
           "Avant redistribution, la France est plus inégalitaire que ses voisins ; après, elle est proche de la moyenne",
           "Inégalités de revenu avant et après impôts et prestations sociales (enquête européenne de 2025, revenus de 2024)",
           "Source : Eurostat (ilc_di12 et ilc_di12c), mise à jour du 5 octobre 2026. Si les retraites sont comptées "
           "comme des prestations, l'indice avant redistribution est de 53,7 en France et de 47,8 dans l'UE.")


# ===========================================================================
# 6. Patrimoine
# Gauche : Insee, Insee Focus n° 371 (décembre 2025), patrimoine brut début 2024 ; World Inequality Database
# via Our World in Data, patrimoine net 2024. Droite : World Inequality Database, part des 10 % les plus riches, 2024.
# ===========================================================================
def patrimoine():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.6), gridspec_kw={"width_ratios": [1, 1.1]})
    fig.subplots_adjust(left=0.07, right=0.97, top=0.78, bottom=0.13, wspace=0.42)
    grp = ["50 % les\nmoins dotés", "10 % les\nmieux dotés", "dont 1 % les\nmieux dotés"]
    insee = [7, 48, 15]
    x = np.arange(3)
    w = 0.36
    ax1.bar(x - w / 2, insee, w, color=BLUE, label="Insee (enquête, patrimoine brut, 2024)")
    ax1.bar([1 + w / 2, 2 + w / 2], [59.9, 27.7], w, color=VIOLET, label="World Inequality Database (patrimoine net, 2024)")
    for xi, val in zip(x - w / 2, insee):
        ax1.text(xi, val + 1, f"{val} %", ha="center", fontsize=10, color=INK)
    for xi, val in zip([1 + w / 2, 2 + w / 2], [59.9, 27.7]):
        ax1.text(xi, val + 1, f"{val:.1f} %".replace(".", ","), ha="center", fontsize=10, color=INK)
    ax1.set_xticks(x)
    ax1.set_xticklabels(grp, fontsize=9.5)
    ax1.set_ylim(0, 80)
    ax1.set_title("Part du patrimoine total détenue, France", color=INK, fontsize=11)
    ax1.legend(loc="upper left", fontsize=8.6)
    hgrid(ax1)
    pays = ["Pays-Bas", "Belgique", "Italie", "Royaume-Uni", "Espagne", "Allemagne", "France", "États-Unis"]
    t10 = [45.53, 52.60, 56.12, 57.14, 57.35, 58.52, 59.88, 69.54]
    c2 = [BLUE if p == "France" else BASE for p in pays]
    ax2.barh(pays, t10, color=c2, height=0.6)
    for i, val in enumerate(t10):
        ax2.text(val + 0.8, i, f"{val:.1f} %".replace(".", ","), va="center", fontsize=9.5, color=INK)
    ax2.set_xlim(0, 80)
    ax2.set_title("Part des 10 % les plus riches, 2024\n(World Inequality Database)", color=INK, fontsize=11)
    for tl in ax2.get_yticklabels():
        if tl.get_text() == "France":
            tl.set_fontweight("bold")
    vgrid(ax2)
    finish(fig, "06_patrimoine.png",
           "Les 10 % les mieux dotés détiennent de 48 % à 60 % du patrimoine, selon la mesure",
           "Part du patrimoine des ménages détenue par chaque groupe ; patrimoine net médian en France : 148 100 € (début 2024)",
           "Sources : Insee Focus n° 371 (décembre 2025) ; World Inequality Database via Our World in Data (données lues "
           "le 10 octobre 2026). Le WID intègre les très grandes fortunes, mal couvertes par les enquêtes.")


if __name__ == "__main__":
    annuel()
    preengagees()
    prix()
    salaires_distribution()
    redistribution()
    patrimoine()
    print("ok")
