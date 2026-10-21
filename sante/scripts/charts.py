"""Graphiques du chapitre « Santé et assurance maladie ».
Les données sont sourcées en commentaire, et dans le chapitre (sante_assurance_maladie.md).
Usage, depuis la racine du dépôt : python3 sante/scripts/charts.py
"""
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



def comma_axis(ax):
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:g}".replace(".", ",")))


def mark_fr(ax):
    for tl in ax.get_yticklabels():
        if tl.get_text() == "France":
            tl.set_fontweight("bold")


# ===========================================================================
# 1. Dépense de santé et reste à charge
# ===========================================================================
def depenses():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.78, bottom=0.12, wspace=0.42)
    # DREES, Les dépenses de santé en 2024 (édition 2025), comparaisons internationales :
    # dépense courante de santé au sens international, % du PIB, 2024.
    p1 = ["UE à 27", "France", "Autriche", "Allemagne", "États-Unis"]
    v1 = [10.3, 11.4, 11.8, 12.3, 17.2]
    ax1.barh(p1, v1, color=[INK2, BLUE, BASE, BASE, BASE], height=0.6)
    for i, v in enumerate(v1):
        ax1.text(v + 0.2, i, f"{v:.1f} %".replace(".", ","), va="center", fontsize=10, color=INK)
    ax1.set_xlim(0, 20)
    comma_axis(ax1)
    ax1.set_title("Dépense courante de santé, % du PIB (2024)", color=INK, fontsize=11)
    vgrid(ax1)
    mark_fr(ax1)
    # DREES, même source : part de la dépense courante payée directement par les ménages, 2023.
    p2 = ["Croatie", "Luxembourg", "France", "États-Unis", "Allemagne", "UE à 27"]
    v2 = [9.4, 9.7, 10.2, 10.9, 11.1, 14.8]
    ax2.barh(p2, v2, color=[BASE, BASE, BLUE, BASE, BASE, INK2], height=0.6)
    for i, v in enumerate(v2):
        ax2.text(v + 0.2, i, f"{v:.1f} %".replace(".", ","), va="center", fontsize=10, color=INK)
    ax2.set_xlim(0, 18)
    ax2.set_title("Part payée directement par les ménages (2023, à vérifier)", color=INK, fontsize=11)
    vgrid(ax2)
    mark_fr(ax2)
    finish(fig, "01_depenses_sante.png",
           "La France est au 3e rang de l'UE pour la dépense de santé, et parmi les pays où les ménages paient le moins directement",
           "Dépense courante de santé en % du PIB, et part payée directement par les ménages (définition internationale)",
           "Source : DREES, Les dépenses de santé en 2024 (édition 2025), d'après l'OCDE et Eurostat. Année de comparaison et valeurs "
           "des autres pays à vérifier. La mesure française du reste à charge donne 7,8 % en 2024.")


# ===========================================================================
# 2. Déficit de la Sécurité sociale
# ===========================================================================
def deficit():
    # Hauteur réduite : ce graphique figure dans « L'essentiel », qui doit tenir sur une page du PDF.
    fig, ax = plt.subplots(figsize=(12.5, 4.9))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.85, bottom=0.16)
    # Solde des régimes obligatoires de base et du fonds de solidarité vieillesse (FSV), Md€ (périmètre du
    # tableau du Sénat, avis n° 747 ; le régime général et le FSV seuls font −20,3 Md€ en 2025).
    # Correction du 21 octobre 2026 : le titre disait « régime général et FSV ». Le périmètre de 2021-2022 (IFRAP)
    # et de 2026-2027 (projet de loi) reste à vérifier.
    # 2021-2022 : IFRAP d'après les comptes officiels (source secondaire).
    # 2023-2025 : Sénat, avis n° 747 (juin 2026).
    # 2026 : prévision révisée du projet de loi de financement pour 2027 (n° 3211, 1er octobre 2026), article 1er
    #        (périmètre exact à vérifier).
    # 2027 : objectif du même projet ; sans mesures, le déficit serait de 22,6 Md€.
    yrs = ["2021", "2022", "2023", "2024", "2025", "2026\n(prévision)", "2027\n(objectif)"]
    tot = [-24.5, -19.7, -10.8, -15.3, -21.6, -21.8, -12.7]
    # Branche maladie : Sénat, avis n° 747 (2024-2025). Années antérieures non vérifiées.
    mal = [None, None, None, -13.8, -15.9, None, None]
    x = np.arange(len(yrs))
    w = 0.36
    b = ax.bar(x - w / 2, tot, w, color=ORANGE, label="Ensemble (régimes obligatoires de base et fonds de solidarité vieillesse)")
    for bar in b[-2:]:
        bar.set_hatch("///")
        bar.set_edgecolor(SURFACE)
    xm = [xi + w / 2 for xi, m in zip(x, mal) if m is not None]
    vm = [m for m in mal if m is not None]
    ax.bar(xm, vm, w, color=VIOLET, label="dont branche maladie")
    for xi, v in zip(x - w / 2, tot):
        ax.text(xi, v - 0.6, f"{v:.1f}".replace(".", ",").replace("-", "−"), ha="center", va="top", fontsize=10,
                color=INK, fontweight="semibold")
    for xi, v in zip(xm, vm):
        ax.text(xi, v - 0.6, f"{v:.1f}".replace(".", ",").replace("-", "−"), ha="center", va="top", fontsize=9.5,
                color=VIOLET)
    ax.axhline(0, color=INK2, linewidth=0.8)
    ax.text(6 - w / 2, -26.5, "sans mesures\nnouvelles :\n−22,6", ha="center", fontsize=8.8, color=INK2)
    ax.set_xticks(x)
    ax.set_xticklabels(yrs)
    ax.set_ylim(-34, 2)
    ax.set_ylabel("Md€")
    ax.legend(loc="lower left", fontsize=9.2, ncol=1)
    hgrid(ax)
    finish(fig, "02_deficit_secu.png",
           "Le déficit de la Sécurité sociale a doublé en deux ans ; le projet de budget vise 12,7 Md€ en 2027",
           "Solde des régimes obligatoires de base et du fonds de solidarité vieillesse, en milliards d'euros (hachures : prévision et objectif)",
           "Sources : Sénat, avis n° 747 (2023-2025) ; IFRAP, think tank libéral, d'après les comptes (2021-2022, à vérifier) ; "
           "projet de loi de financement pour 2027 (2026 ; 2027 via la presse).")


# ===========================================================================
# 3. Lits d'hôpital
# ===========================================================================
def lits():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.78, bottom=0.12, wspace=0.3)
    # DREES, Les établissements de santé, édition 2026 (juillet 2026) :
    # 367 100 lits d'hospitalisation complète fin 2024, « une diminution de 45 700 lits depuis fin 2013 »
    # (412 800 fin 2013, calcul) ; 91 100 places d'hospitalisation partielle fin 2024, « 23 200 places de plus
    # que fin 2013 » (67 900 fin 2013, calcul).
    for ax, vals, color, title in (
        (ax1, [412800, 367100], BLUE, "Lits d'hospitalisation complète (−11 %)"),
        (ax2, [67900, 91100], AQUA, "Places d'hospitalisation partielle, sans nuit (+34 %)"),
    ):
        ax.bar(["Fin 2013", "Fin 2024"], vals, color=color, width=0.55)
        top = max(vals) * 1.15
        for i, val in enumerate(vals):
            ax.text(i, val + top * 0.015, f"{val:,}".replace(",", " "), ha="center", fontsize=10.5, color=INK,
                    fontweight="semibold")
        ax.set_ylim(0, top)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f"{x/1000:.0f} k"))
        ax.set_title(title, color=INK, fontsize=11)
        hgrid(ax)
    finish(fig, "03_lits_hopital.png",
           "L'hôpital a 11 % de lits en moins qu'en 2013, et 34 % de places de jour en plus",
           "Capacités des établissements de santé (public et privé), en nombre de lits et de places",
           "Source : DREES, Les établissements de santé, édition 2026 (données 2024) ; valeurs de 2013 : calcul d'après la même source.")


# ===========================================================================
# 4. Pénuries de médicaments
# ===========================================================================
def penuries():
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.8, bottom=0.12)
    # ANSM, rapport d'activité 2025, annexes (juillet 2026), p. 6.
    yrs = ["2021", "2022", "2023", "2024", "2025"]
    risk = [1251, 2138, 3336, 3216, 3488]
    rup = [909, 1623, 1589, 609, 399]
    ax.bar(yrs, rup, color=ORANGE, width=0.58, label="Ruptures")
    ax.bar(yrs, risk, bottom=rup, color=YELLOW, width=0.58, label="Risques de rupture")
    for i, (a, b) in enumerate(zip(rup, risk)):
        ax.text(i, a + b + 80, f"{a+b:,}".replace(",", " "), ha="center", fontsize=10.5, color=INK,
                fontweight="semibold")
    ax.set_ylim(0, 5600)
    ax.set_ylabel("Déclarations")
    ax.legend(loc="upper left", fontsize=9.5)
    hgrid(ax)
    finish(fig, "04_penuries_medicaments.png",
           "Presque deux fois plus de signalements de pénurie qu'en 2021, mais quatre fois moins de ruptures qu'en 2022",
           "Déclarations de ruptures et de risques de rupture pour les médicaments d'intérêt thérapeutique majeur",
           "Source : Agence nationale de sécurité du médicament (ANSM), rapport d'activité 2025 (juillet 2026).")


# ===========================================================================
# 5. Espérance de vie
# ===========================================================================
def esperance():
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    fig.subplots_adjust(left=0.08, right=0.82, top=0.8, bottom=0.12)
    # Insee, espérance de vie à la naissance (2023-2025 provisoires) ; UE : Eurostat (2024).
    # Insee, tableau « Espérance de vie à divers âges » (page lue le 7 octobre 2026), France y compris Mayotte.
    yrs = [2015, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    f = [85.1, 85.6, 85.1, 85.2, 85.1, 85.6, 85.8, 85.9]
    h = [79.0, 79.7, 79.1, 79.2, 79.3, 80.0, 80.2, 80.3]
    ax.plot(yrs, f, color=MAGENTA, linewidth=2.5, marker="o", markeredgecolor=SURFACE)
    ax.plot(yrs, h, color=BLUE, linewidth=2.5, marker="o", markeredgecolor=SURFACE)
    ax.plot(2024, 84.1, "D", color=MAGENTA, markersize=7, markerfacecolor=SURFACE, markeredgewidth=2)
    ax.plot(2024, 78.9, "D", color=BLUE, markersize=7, markerfacecolor=SURFACE, markeredgewidth=2)
    ax.text(2025.3, 85.9, "Femmes, France : 85,9", va="center", fontsize=10, color=MAGENTA, fontweight="semibold")
    ax.text(2025.3, 80.3, "Hommes, France : 80,3", va="center", fontsize=10, color=BLUE, fontweight="semibold")
    ax.text(2024.1, 83.75, "UE 2024 : 84,1", fontsize=9, color=MAGENTA, va="top")
    ax.text(2024.1, 78.55, "UE 2024 : 78,9", fontsize=9, color=BLUE, va="top")
    ax.set_ylim(77, 88)
    ax.set_xlim(2014.5, 2025.2)
    ax.set_ylabel("Années")
    hgrid(ax)
    finish(fig, "05_esperance_vie.png",
           "En 2024, les Françaises vivaient 1,7 an de plus que la moyenne de l'UE, et les Français 1,3 an",
           "Espérance de vie à la naissance (losanges : moyenne de l'UE en 2024)",
           "Sources : Insee (France ; 2023-2025 provisoires) ; Eurostat (UE, 2024). Années 2016-2018 non représentées.")


if __name__ == "__main__":
    depenses()
    deficit()
    lits()
    penuries()
    esperance()
    print("ok")
