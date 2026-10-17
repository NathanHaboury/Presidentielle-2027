"""Graphiques du chapitre « Logement ».
Toutes les données sont sourcées dans le chapitre (logement.md) et en commentaire ci-dessous.
Version du 10 octobre 2026 : six graphiques. Régénérer avec : python3 logement/scripts/charts.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# --- Police & encre (mêmes réglages que les autres chapitres) --------------
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
GREY = "#b9b8b0"

plt.rcParams.update({
    "font.family": FONT, "font.size": 10.5, "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE, "xtick.color": MUTED, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlelocation": "left", "axes.titlesize": 12, "axes.titleweight": "semibold",
    "legend.frameon": False,
})


def fr(x, dec=0):
    """Nombre au format français (espace fine pour les milliers, virgule décimale)."""
    s = f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s


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
# 1. Logements mis en chantier et autorisés, 2000-2025 et 12 mois à fin août 2026 (graphique clé)
# Source : Insee, séries 001718270 (commencés) et 001718158 (autorisés), cumul sur douze mois,
# France hors Mayotte, estimations en date réelle, valeurs de décembre, mise à jour du 29 septembre 2026.
# ===========================================================================
MEC = {2000: 337_600, 2001: 337_200, 2002: 342_400, 2003: 363_900, 2004: 414_400, 2005: 464_900,
       2006: 493_800, 2007: 488_900, 2008: 398_400, 2009: 345_600, 2010: 412_200, 2011: 430_100,
       2012: 382_300, 2013: 357_900, 2014: 336_800, 2015: 340_900, 2016: 369_400, 2017: 433_900,
       2018: 400_500, 2019: 385_400, 2020: 369_600, 2021: 414_200, 2022: 389_600, 2023: 296_300,
       2024: 259_600, 2025: 263_000}
AUT = {2000: 391_000, 2001: 379_600, 2002: 376_800, 2003: 413_900, 2004: 500_400, 2005: 551_700,
       2006: 602_400, 2007: 571_500, 2008: 476_600, 2009: 381_100, 2010: 477_600, 2011: 518_700,
       2012: 483_100, 2013: 416_800, 2014: 375_000, 2015: 397_500, 2016: 459_400, 2017: 488_000,
       2018: 457_000, 2019: 446_200, 2020: 393_400, 2021: 467_200, 2022: 485_700, 2023: 373_500,
       2024: 321_200, 2025: 371_500}
MEC_AOUT26, AUT_AOUT26 = 300_500, 370_200


def construction():
    years = list(MEC)
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    fig.subplots_adjust(left=0.08, right=0.95, top=0.80, bottom=0.13)
    ax.plot(years, [AUT[y] / 1000 for y in years], color=GREY, linewidth=2.0, label="Logements autorisés (permis)")
    ax.plot(years, [MEC[y] / 1000 for y in years], color=BLUE, linewidth=2.8, label="Logements mis en chantier")
    x26 = 2025.67
    ax.plot([2025, x26], [MEC[2025] / 1000, MEC_AOUT26 / 1000], color=BLUE, linewidth=2.0, linestyle=":")
    ax.plot([2025, x26], [AUT[2025] / 1000, AUT_AOUT26 / 1000], color=GREY, linewidth=1.6, linestyle=":")
    ax.scatter([x26], [MEC_AOUT26 / 1000], color=BLUE, s=28, zorder=3)
    for y, dy in ((2006, 14), (2017, -24), (2022, 14), (2024, -30)):
        ax.annotate(fr(MEC[y]), (y, MEC[y] / 1000), xytext=(0, dy), textcoords="offset points",
                    ha="center", fontsize=9.5, color=BLUE, fontweight="semibold")
    ax.annotate("12 mois à fin\naoût 2026 :\n" + fr(MEC_AOUT26), (x26, MEC_AOUT26 / 1000), xytext=(8, -36),
                textcoords="offset points", ha="left", fontsize=8.8, color=BLUE)
    ax.set_ylim(0, 650)
    ax.set_xlim(1999.5, 2027.4)
    ax.set_ylabel("milliers de logements")
    ax.legend(loc="lower left", fontsize=9.5)
    hgrid(ax)
    finish(fig, "01_construction.png",
           "Les mises en chantier ont baissé d'un tiers de 2022 à 2024",
           "Logements mis en chantier et autorisés chaque année, France hors Mayotte, en milliers ; l'axe part de zéro",
           "Source : Insee, séries 001718270 et 001718158 (cumul sur douze mois, estimations en date réelle, "
           "mise à jour du 29 septembre 2026). Pointillés : cumul des 12 mois à fin août 2026.")


# ===========================================================================
# 2. Capacité d'emprunt pour 1 000 € par mois sur 25 ans, selon le taux moyen
# Taux : Observatoire Crédit Logement/CSA (source privée), taux moyen du 4e trimestre et d'août 2026,
# hors assurance. Capacité : calcul du chapitre, formule d'annuité, hors assurance et frais.
# ===========================================================================
TAUX = [("Fin 2019", 1.11), ("Fin 2021", 1.05), ("Fin 2023", 4.15), ("Fin 2025", 3.14), ("Août 2026", 3.31)]


def capital(taux, mensualite=1000, mois=300):
    r = taux / 100 / 12
    return mensualite * (1 - (1 + r) ** -mois) / r


def credit():
    labels = [t[0] for t in TAUX]
    caps = [capital(t[1]) for t in TAUX]
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.79, bottom=0.14)
    colors = [GREY, GREY, BLUE, GREY, BLUE]
    bars = ax.bar(labels, [c / 1000 for c in caps], color=colors, width=0.6)
    for b, c, (_, t) in zip(bars, caps, TAUX):
        ax.text(b.get_x() + b.get_width() / 2, c / 1000 + 5, "≈ " + fr(round(c, -3)) + " €",
                ha="center", fontsize=10.5, fontweight="semibold", color=INK)
        ax.text(b.get_x() + b.get_width() / 2, 12, "taux " + fr(t, 2) + " %",
                ha="center", fontsize=9.5, color="white", fontweight="semibold")
    ax.set_ylim(0, 300)
    ax.set_ylabel("milliers d'euros")
    hgrid(ax)
    finish(fig, "02_capacite_emprunt.png",
           "Avec 1 000 € par mois, on emprunte ≈ 60 000 € de moins qu'à la fin de 2021",
           "Somme empruntable sur 25 ans avec une mensualité de 1 000 €, au taux moyen du moment, hors assurance (calcul)",
           "Sources : taux moyens de l'Observatoire Crédit Logement/CSA (4e trimestre, puis août 2026) ; "
           "calcul du chapitre (formule de l'annuité constante). La Banque de France donne 3,32 % en août 2026.")


# ===========================================================================
# 3. Prix des logements anciens, en euros courants et en euros constants, base 100 au 4e trimestre 2000
# Prix : Insee, série 010567059 (France métropolitaine, CVS, base 2015), valeur du 4e trimestre.
# Prix à la consommation : Insee, série 001763852 (IPC hors tabac, base 2015), valeur de décembre.
# Euros constants : calcul du chapitre (indice des prix des logements / IPC).
# ===========================================================================
PRIX = {2000: 50.4, 2001: 54.4, 2002: 59.9, 2003: 67.5, 2004: 78.2, 2005: 89.8, 2006: 98.7, 2007: 104.1,
        2008: 100.2, 2009: 96.1, 2010: 103.4, 2011: 107.2, 2012: 105.1, 2013: 103.2, 2014: 100.6,
        2015: 100.1, 2016: 101.6, 2017: 104.9, 2018: 108.3, 2019: 112.5, 2020: 119.6, 2021: 128.0,
        2022: 134.0, 2023: 128.8, 2024: 126.1, 2025: 127.3}
IPC = {2000: 81.60, 2001: 82.63, 2002: 84.41, 2003: 85.76, 2004: 87.40, 2005: 88.82, 2006: 90.16, 2007: 92.44,
       2008: 93.37, 2009: 94.14, 2010: 95.74, 2011: 98.04, 2012: 99.23, 2013: 99.87, 2014: 99.86,
       2015: 100.04, 2016: 100.66, 2017: 101.76, 2018: 103.16, 2019: 104.39, 2020: 104.09, 2021: 107.03,
       2022: 113.42, 2023: 117.50, 2024: 118.88, 2025: 119.76}


def prix():
    years = list(PRIX)
    nom = [PRIX[y] / PRIX[2000] * 100 for y in years]
    reel = [(PRIX[y] / IPC[y]) / (PRIX[2000] / IPC[2000]) * 100 for y in years]
    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    fig.subplots_adjust(left=0.07, right=0.93, top=0.80, bottom=0.13)
    ax.plot(years, nom, color=BLUE, linewidth=2.8, label="En euros courants")
    ax.plot(years, reel, color=ORANGE, linewidth=2.2, label="En euros constants (inflation retirée)")
    ax.axhline(100, color=BASE, linewidth=1)
    for y, v, c, dy in ((2022, nom[years.index(2022)], BLUE, 10), (2025, nom[-1], BLUE, -18),
                        (2007, reel[years.index(2007)], ORANGE, -18), (2025, reel[-1], ORANGE, -18)):
        ax.annotate(fr(v), (y, v), xytext=(0, dy), textcoords="offset points", ha="center",
                    fontsize=9.5, color=c, fontweight="semibold")
    ax.set_ylim(0, 300)
    ax.set_xlim(1999.5, 2026)
    ax.set_ylabel("indice, 4e trimestre 2000 = 100")
    ax.legend(loc="upper left", fontsize=9.5)
    hgrid(ax)
    finish(fig, "03_prix_logements.png",
           "Les prix ont été multipliés par 2,5 depuis 2000 ; sans l'inflation, par 1,7",
           "Prix des logements anciens, France métropolitaine, indice 100 au 4e trimestre 2000 (valeurs du 4e trimestre)",
           "Sources : Insee, indice des prix des logements anciens (série 010567059, CVS) et indice des prix à la "
           "consommation hors tabac (série 001763852, décembre). Euros constants : calcul du chapitre.")


# ===========================================================================
# 4. Taux d'effort net pour se loger, début 2024
# Source : Insee Première n° 2128 (23 septembre 2026), enquête Logement 2023-2024, France hors Mayotte.
# Dépenses de logement, aides déduites, rapportées au revenu avant impôts directs.
# ===========================================================================
EFFORT = [("Locataires du parc privé", 25.4), ("Locataires du parc social", 24.0),
          ("Propriétaires qui remboursent un emprunt", 23.3), ("Propriétaires sans emprunt", 7.4),
          ("Ensemble des ménages", 16.8), ("Quart des ménages les plus modestes", 32.1)]


def effort():
    fig, ax = plt.subplots(figsize=(12.5, 4.6))
    fig.subplots_adjust(left=0.30, right=0.95, top=0.79, bottom=0.14)
    labels = [e[0] for e in EFFORT][::-1]
    vals = [e[1] for e in EFFORT][::-1]
    colors = [ORANGE if "modestes" in l else (BLUE if "Ensemble" in l else GREY) for l in labels]
    ax.barh(labels, vals, color=colors, height=0.62)
    for i, v in enumerate(vals):
        ax.text(v + 0.5, i, fr(v, 1) + " %", va="center", fontsize=10, fontweight="semibold")
    ax.set_xlim(0, 38)
    ax.set_xlabel("% du revenu")
    vgrid(ax)
    finish(fig, "04_taux_effort.png",
           "Le logement prend un tiers du revenu du quart des ménages les plus modestes",
           "Taux d'effort net : dépenses de logement, aides déduites, en % du revenu avant impôts, début 2024",
           "Source : Insee, Insee Première n° 2128 (septembre 2026), enquêtes Logement. France hors Mayotte, "
           "hors ménages étudiants. Mêmes chiffres que le chapitre Pouvoir d'achat, section 1.3.")


# ===========================================================================
# 5. Passoires thermiques (étiquettes F ou G) parmi les résidences principales, par statut d'occupation
# Source : SDES, Observatoire national de la rénovation énergétique (ONRE), parc au 1er janvier 2025,
# France métropolitaine (30,9 millions de résidences principales).
# ===========================================================================
PASSOIRES = [("Propriétaires occupants", 2.5, 14.0), ("Location privée", 1.1, 13.8),
             ("Logement social", 0.3, 5.8), ("Ensemble", 3.9, 12.7)]


def passoires():
    fig, ax = plt.subplots(figsize=(12.5, 4.4))
    fig.subplots_adjust(left=0.22, right=0.95, top=0.78, bottom=0.15)
    labels = [p[0] for p in PASSOIRES][::-1]
    parts = [p[2] for p in PASSOIRES][::-1]
    nombres = [p[1] for p in PASSOIRES][::-1]
    colors = [BLUE if l == "Ensemble" else GREY for l in labels]
    ax.barh(labels, parts, color=colors, height=0.6)
    for i, (v, n) in enumerate(zip(parts, nombres)):
        ax.text(v + 0.25, i, fr(v, 1) + " %  (" + fr(n, 1) + " million" + ("s" if n >= 2 else "") + ")",
                va="center", fontsize=10, fontweight="semibold")
    ax.set_xlim(0, 20)
    ax.set_xlabel("% des résidences principales de chaque statut")
    vgrid(ax)
    finish(fig, "05_passoires_statut.png",
           "Une résidence principale sur huit est une « passoire thermique »",
           "Part des résidences principales classées F ou G au diagnostic de performance énergétique, au 1er janvier 2025",
           "Source : SDES, Observatoire national de la rénovation énergétique (octobre 2025). France métropolitaine. "
           "Avant le changement de calcul du 1er janvier 2026.")


# ===========================================================================
# 6. Comparaison européenne : hausse des prix 2015-2025 et surcharge des coûts du logement en 2025
# Source : Eurostat, prc_hpi_a (indice 2015 = 100, moyenne annuelle, mise à jour du 1er octobre 2026)
# et ilc_lvho07a (part de la population dans un ménage qui consacre plus de 40 % de son revenu disponible
# au logement, mise à jour du 17 septembre 2026).
# ===========================================================================
EUROPE = [("Pays-Bas", 115, 6.5), ("Espagne", 81, 7.2), ("UE", 62, 7.7), ("Allemagne", 53, 11.2),
          ("France", 27, 6.4), ("Italie", 16, 5.0)]


def europe():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.8))
    fig.subplots_adjust(left=0.09, right=0.97, top=0.76, bottom=0.14, wspace=0.35)
    labels = [e[0] for e in EUROPE][::-1]
    hausse = [e[1] for e in EUROPE][::-1]
    surch = [e[2] for e in EUROPE][::-1]
    colors = [BLUE if l == "France" else (INK2 if l == "UE" else GREY) for l in labels]
    ax1.barh(labels, hausse, color=colors, height=0.6)
    for i, v in enumerate(hausse):
        ax1.text(v + 2, i, "+" + fr(v) + " %", va="center", fontsize=10, fontweight="semibold")
    ax1.set_xlim(0, 135)
    ax1.set_title("Hausse des prix des logements, 2015 → 2025", fontsize=11)
    vgrid(ax1)
    ax2.barh(labels, surch, color=colors, height=0.6)
    for i, v in enumerate(surch):
        ax2.text(v + 0.2, i, fr(v, 1) + " %", va="center", fontsize=10, fontweight="semibold")
    ax2.set_xlim(0, 13.5)
    ax2.set_title("Population dont le ménage consacre plus de\n40 % de son revenu au logement, 2025", fontsize=11)
    vgrid(ax2)
    finish(fig, "06_comparaison_europeenne.png",
           "Depuis 2015, les prix des logements ont moins augmenté en France que dans l'UE",
           "Hausse de l'indice des prix des logements (moyenne annuelle) et taux de surcharge des coûts du logement",
           "Source : Eurostat, prc_hpi_a (1er octobre 2026) et ilc_lvho07a (17 septembre 2026). "
           "UE : 27 pays. Arrondis à l'unité pour les prix.")


if __name__ == "__main__":
    construction()
    credit()
    prix()
    effort()
    passoires()
    europe()
    print("Graphiques écrits dans", OUT)
