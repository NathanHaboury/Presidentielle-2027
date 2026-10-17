"""Graphiques du chapitre « Éducation ».
Les données sont sourcées en commentaire, et dans le chapitre (remuneration_enseignants.md).
Usage, depuis la racine du dépôt : python3 education/scripts/charts.py
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


# ===========================================================================
# 1. Le niveau : scores PISA de la France (graphique clé de « L'essentiel »)
# ===========================================================================
def niveau_pisa():
    # Score moyen de la France, élèves de 15 ans.
    # 2012, 2022 : DEPP, note n° 23.48 (décembre 2023) ; 2025 : DEPP, note n° 26.40 (septembre 2026).
    # Autres années : IFRAP, « Les évolutions du classement français au test PISA depuis 25 ans »
    # (10 septembre 2026), d'après l'OCDE (à vérifier dans la base de l'OCDE).
    # L'échelle de mathématiques est fixée en 2003, celle de l'écrit en 2000 (convention de l'OCDE).
    maths_y = [2003, 2006, 2009, 2012, 2015, 2018, 2022, 2025]
    maths = [511, 496, 497, 495, 493, 495, 474, 458]
    ecrit_y = [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022, 2025]
    ecrit = [505, 496, 488, 496, 505, 499, 493, 474, 456]
    # Moyenne de l'OCDE en mathématiques : 2012 (494) et 2022 (472), DEPP n° 23.48 ; 2025 (463), DEPP n° 26.40.
    oc_y = [2012, 2022, 2025]
    oc = [494, 472, 463]
    fig, ax = plt.subplots(figsize=(12.5, 4.9))
    fig.subplots_adjust(left=0.07, right=0.83, top=0.84, bottom=0.17)
    ax.plot(ecrit_y, ecrit, color=AQUA, linewidth=2.0, marker="o", markersize=5, markeredgecolor=SURFACE,
            markeredgewidth=1.2, label="France, compréhension de l'écrit")
    ax.plot(maths_y, maths, color=BLUE, linewidth=2.6, marker="o", markersize=6, markeredgecolor=SURFACE,
            markeredgewidth=1.2, label="France, mathématiques")
    ax.scatter(oc_y, oc, marker="D", s=46, color=ORANGE, zorder=3, label="Moyenne de l'OCDE, mathématiques")
    ax.text(2003, 514, "511", ha="center", va="bottom", fontsize=10, color=BLUE, fontweight="semibold")
    ax.text(2025.5, 458, "Mathématiques : 458", va="center", fontsize=10, color=BLUE, fontweight="semibold")
    ax.text(2025.5, 451, "Écrit : 456", va="center", fontsize=10, color=AQUA, fontweight="semibold")
    ax.text(2025.5, 466, "OCDE : 463", va="center", fontsize=9.5, color=ORANGE)
    ax.set_xlim(1999, 2030.5)
    ax.set_ylim(440, 525)
    ax.set_xticks([2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022, 2025])
    ax.set_ylabel("Points")
    ax.legend(loc="lower left", fontsize=9.5)
    hgrid(ax)
    finish(fig, "01_niveau_pisa.png",
           "Mathématiques à 15 ans : −53 points depuis 2003 ; la moyenne des pays développés (OCDE) baisse aussi",
           "Score moyen à l'enquête PISA, en points ; losanges : moyenne des pays de l'OCDE en mathématiques",
           "Sources : DEPP, notes n° 23.48 (2023) et 26.40 (2026) pour 2012, 2022 et 2025 ; IFRAP, think tank libéral, "
           "d'après l'OCDE, pour les autres années (à vérifier).")


# ===========================================================================
# 2. Les inégalités : écart entre élèves favorisés et défavorisés
# ===========================================================================
def inegalites_pisa():
    # Écart de score en mathématiques entre le quart d'élèves le plus favorisé et le quart le plus
    # défavorisé (indice socio-économique de PISA). 2003, 2012, 2022 : Insee, France, portrait social,
    # édition 2025, fiche « Inégalités sociales dans l'enseignement scolaire ».
    # PISA 2025 (DEPP, note n° 26.40 : 95 points contre 83) n'est pas tracé : les groupes comparés ne sont
    # peut-être pas définis de la même façon (voir le texte, section 1.3).
    yrs = ["2003", "2012", "2022"]
    fra = [104, 119, 113]
    oc = [98, 90, 94]
    x = np.arange(len(yrs))
    w = 0.36
    fig, ax = plt.subplots(figsize=(12.5, 4.9))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.84, bottom=0.17)
    b1 = ax.bar(x - w / 2, fra, w, color=BLUE, label="France")
    b2 = ax.bar(x + w / 2, oc, w, color=ORANGE, label="Moyenne de l'OCDE")
    for bars, vals, col in [(b1, fra, BLUE), (b2, oc, ORANGE)]:
        for r, v in zip(bars, vals):
            ax.text(r.get_x() + r.get_width() / 2, v + 2, str(v), ha="center", fontsize=10.5, color=INK,
                    fontweight="semibold")
    ax.set_xticks(x, yrs)
    ax.set_ylim(0, 135)
    ax.set_ylabel("Écart de score, en points")
    ax.legend(loc="upper right")
    hgrid(ax)
    finish(fig, "02_inegalites_pisa.png",
           "L'écart entre élèves favorisés et défavorisés est plus grand en France que dans l'OCDE",
           "Écart de score en mathématiques à 15 ans (PISA) entre le quart d'élèves le plus favorisé et le quart le plus "
           "défavorisé, en points",
           "Source : Insee, France, portrait social 2025, d'après l'OCDE (PISA).")


# ===========================================================================
# 3. Les salaires réels comparés
# ===========================================================================
def salaires_reels():
    # Point d'indice : 4,6303 € (juillet 2010) → 4,9228 € (2024), +6,3 % ; prix (Insee) +26,5 % de 2010 à 2024 ;
    #   inflation déduite : 1,063 / 1,265 − 1 = −16 % (calcul).
    # Enseignants : DEPP via Sénat (2002-2022 : −8 % primaire, −5 % secondaire), puis DEPP (2023 : +0,4 % ;
    #   2024 : +4,3 %) ; enchaînement indicatif de séries non homogènes (calcul).
    # À échelon égal : −15 à −25 % en vingt ans (Sénat, rapport Longuet n° 163, 2021).
    # Fonction publique d'État, 2010 → 2024 : −0,4 % ; privé, 2000 → 2024 : +9,9 % (Insee).
    rows = [
        ("Point d'indice (2010 → 2024)", -16.0, "−16 %", None),
        ("Enseignant à échelon égal,\nsur vingt ans (Sénat, 2021)", -20.0, "−15 à −25 %", (5, 5)),
        ("Salaire moyen des professeurs\ndes écoles (2002 → 2024, estimation)", -4.0, "≈ −4 %", None),
        ("Salaire moyen des enseignants\ndu 2nd degré (2002 → 2024, estimation)", -0.5, "≈ −0,5 %", None),
        ("Salaire moyen, fonction\npublique d'État (2010 → 2024)", -0.4, "−0,4 %", None),
        ("Salaire net moyen,\nsecteur privé (2000 → 2024)", 9.9, "+9,9 %", None),
    ]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.27, right=0.95, top=0.84, bottom=0.15)
    cols = [AQUA if v > 0 else (BASE if err else BLUE) for _, v, _, err in rows]
    ax.barh(range(len(rows)), [v for _, v, _, _ in rows], color=cols, height=0.6)
    for i, (_, v, lab, err) in enumerate(rows):
        if err:
            ax.errorbar(v, i, xerr=[[err[0]], [err[1]]], color=INK2, capsize=5, linewidth=1.4)
        x = v + (0.6 if v >= 0 else -0.6)
        if err:
            x = v - err[0] - 0.6
        ax.text(x, i, lab, va="center", ha="left" if v >= 0 else "right", fontsize=10, color=INK,
                fontweight="semibold")
    ax.axvline(0, color=BASE, linewidth=1)
    ax.set_yticks(range(len(rows)), [n for n, _, _, _ in rows])
    ax.set_xlim(-34, 16)
    ax.set_xlabel("Évolution, inflation déduite, en %")
    vgrid(ax)
    finish(fig, "03_salaires_reels.png",
           "Inflation déduite, le salaire moyen des enseignants a presque stagné depuis 2002, celui du privé a progressé",
           "Le point d'indice a perdu 16 % depuis 2010 ; l'ancienneté et les primes ont compensé une grande partie de "
           "cette baisse. Les périodes diffèrent.",
           "Sources : point d'indice (retraitesdeletat.gouv.fr) et prix (Insee) ; DEPP, citée par le Sénat, puis DEPP "
           "(2023-2024), séries enchaînées (calcul) ; Sénat (2021) ; Insee (fonction publique, privé).")


# ===========================================================================
# 4. Comparaison avec l'OCDE
# ===========================================================================
def ocde():
    # OCDE, Regards sur l'éducation 2025 (données 2024), lu à travers le Sénat (rapport n° 139, 2025-2026)
    # et l'amendement CF1907 (lecture directe de l'OCDE impossible) : à vérifier.
    x = np.arange(2)
    w = 0.36
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
    fig.subplots_adjust(left=0.1, right=0.985, top=0.80, bottom=0.14, wspace=0.3)
    fra = [49462, 53086]
    oc = [59673, 61563]
    for vals, col, lab, off in [(fra, BLUE, "France", -1), (oc, ORANGE, "Moyenne de l'OCDE", 1)]:
        bars = ax1.bar(x + off * (w / 2 + 0.01), vals, w, color=col, label=lab)
        for r, v in zip(bars, vals):
            ax1.text(r.get_x() + r.get_width() / 2, v + 900, f"{v:,.0f}".replace(",", " "),
                     ha="center", fontsize=9.5, color=INK2)
    ax1.set_xticks(x, ["Primaire", "Collège"])
    ax1.set_ylim(0, 80000)
    ax1.set_ylabel("Salaire brut annuel, en dollars\ncorrigés du coût de la vie (2024)")
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " ")))
    ax1.set_title("A. Salaire prévu après 15 ans de carrière", pad=8)
    ax1.legend(loc="upper left")
    hgrid(ax1)
    fra2 = [74, 80]
    oc2 = [83, 87]
    for vals, col, lab, off in [(fra2, BLUE, "France", -1), (oc2, ORANGE, "Moyenne de l'OCDE", 1)]:
        bars = ax2.bar(x + off * (w / 2 + 0.01), vals, w, color=col, label=lab)
        for r, v in zip(bars, vals):
            ax2.text(r.get_x() + r.get_width() / 2, v + 1, f"{v} %", ha="center", fontsize=9.5, color=INK2)
    ax2.axhline(100, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    ax2.text(1.45, 101.5, "= salaire d'un autre diplômé du supérieur", fontsize=8.8, color=INK2, ha="right")
    ax2.set_xticks(x, ["Primaire", "Collège"])
    ax2.set_ylim(0, 112)
    ax2.set_ylabel("Salaire réellement versé, en % de celui\ndes autres diplômés du supérieur")
    ax2.set_title("B. Comparé aux autres diplômés du supérieur", pad=8)
    hgrid(ax2)
    finish(fig, "04_comparaison_ocde.png",
           "Les enseignants français gagnent moins que la moyenne de l'OCDE, et moins que les autres diplômés du supérieur",
           "Salaires des enseignants du public ; montants en dollars corrigés des écarts de coût de la vie entre pays",
           "Sources : OCDE, Regards sur l'éducation 2025 (données 2024), lu à travers le Sénat (rapport n° 139, 2025-2026) "
           "et un amendement parlementaire (à vérifier).")


# ===========================================================================
# 5. Le nombre d'élèves
# ===========================================================================
def eleves():
    # DEPP, « Projections d'effectifs d'élèves dans les premier et second degrés à l'horizon 2035 » (7 avril 2026).
    # 2026 : prévision (6 024 100 et 5 583 500). 2025 : prévision 2026 + baisse annoncée (calcul).
    # 2035 : 2025 − 933 000 (premier degré) et − 743 800 (second degré) (calcul).
    yrs = ["Rentrée 2025", "Rentrée 2026\n(prévision)", "Rentrée 2035\n(projection)"]
    p1 = [6.1495, 6.0241, 5.2165]
    p2 = [5.6197, 5.5835, 4.8759]
    x = np.arange(3)
    fig, ax = plt.subplots(figsize=(12.5, 4.9))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.84, bottom=0.17)
    b1 = ax.bar(x, p1, 0.5, color=BLUE, label="Premier degré (maternelle et élémentaire)")
    b2 = ax.bar(x, p2, 0.5, bottom=p1, color=AQUA, label="Second degré (collège et lycée)")
    for i in range(3):
        box = dict(boxstyle="round,pad=0.25", facecolor=SURFACE, edgecolor="none") if i == 2 else None
        tc = INK if i == 2 else "white"
        ax.text(x[i], p1[i] / 2, fr(p1[i], 2) + " M", ha="center", va="center", color=tc, fontsize=10,
                fontweight="semibold", bbox=box)
        ax.text(x[i], p1[i] + p2[i] / 2, fr(p2[i], 2) + " M", ha="center", va="center", color=tc,
                fontsize=10, fontweight="semibold", bbox=box)
        ax.text(x[i], p1[i] + p2[i] + 0.2, fr(p1[i] + p2[i], 2) + " M", ha="center", fontsize=11, color=INK,
                fontweight="semibold")
    for b in (b1[-1], b2[-1]):
        b.set_hatch("///")
        b.set_edgecolor(SURFACE)
    ax.set_xticks(x, yrs)
    ax.set_ylim(0, 13.5)
    ax.set_ylabel("Millions d'élèves")
    ax.legend(loc="upper right", fontsize=9.5)
    hgrid(ax)
    finish(fig, "05_eleves_projection.png",
           "Le nombre d'élèves baisserait de 14 % entre 2025 et 2035",
           "Élèves des écoles, collèges et lycées publics et privés sous contrat, en millions (hachures : projection)",
           "Source : DEPP, projections d'effectifs à l'horizon 2035 (avril 2026) ; 2025 et 2035 calculés à partir des "
           "évolutions publiées (calcul).")


# ===========================================================================
# 6. La réussite en licence selon le bac
# ===========================================================================
def licence():
    # SIES, Note Flash n° 29, « Parcours et réussite en licence : les résultats de la session 2024 » (novembre 2025) :
    # bacheliers 2020 inscrits en première année de licence, licence obtenue en 3 ou 4 ans.
    rows = [("Bac général", 46.1), ("Ensemble", 40.3), ("Bac technologique", 14.0), ("Bac professionnel", 6.5)]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 4.4))
    fig.subplots_adjust(left=0.17, right=0.95, top=0.82, bottom=0.22)
    cols = [INK2 if n == "Ensemble" else BLUE for n, _ in rows]
    ax.barh(range(len(rows)), [v for _, v in rows], color=cols, height=0.6)
    for i, (_, v) in enumerate(rows):
        ax.text(v + 0.8, i, fr(v) + " %", va="center", fontsize=10.5, color=INK, fontweight="semibold")
    ax.set_yticks(range(len(rows)), [n for n, _ in rows])
    ax.set_xlim(0, 60)
    ax.set_xlabel("% des bacheliers 2020 inscrits en licence qui l'obtiennent en 3 ou 4 ans")
    vgrid(ax)
    finish(fig, "06_reussite_licence.png",
           "Près d'un bachelier général sur deux obtient sa licence en 3 ou 4 ans, moins d'un bachelier "
           "professionnel sur dix",
           "Bacheliers 2020 inscrits en première année de licence à l'université",
           "Source : ministère de l'Enseignement supérieur, SIES, Note Flash n° 29 (novembre 2025).")


if __name__ == "__main__":
    niveau_pisa()
    inegalites_pisa()
    salaires_reels()
    ocde()
    eleves()
    licence()
    print("ok", sorted(p.name for p in OUT.glob("*.png")))
