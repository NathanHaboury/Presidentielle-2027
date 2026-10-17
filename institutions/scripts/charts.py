"""Graphiques du chapitre Institutions.
Toutes les données sont sourcées dans le chapitre (institutions.md) et en commentaire ci-dessous.
Usage : python3 institutions/scripts/charts.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
import textwrap

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# --- Police & encre (mêmes réglages que les autres chapitres) ---------------
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
    fig.text(0.02, 0.012, "\n".join(textwrap.wrap(source, 175)), ha="left", va="bottom", fontsize=8.2,
             color=MUTED, linespacing=1.3)
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


def hgrid(ax):
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def vgrid(ax):
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# ===========================================================================
# 1. Les blocs à l'Assemblée nationale, 2017-2026
# ===========================================================================
def blocs():
    # Législatives : sièges par nuance, ministère de l'Intérieur (archives des résultats, pages « France
    # entière » 2017, 2022 et 2024), regroupés par nous :
    #   2017 : gauche = FI 17 + PCF 10 + SOC 30 + PRG 3 + DVG 12 + ECO 1 = 73 ; majorité présidentielle =
    #          REM 308 + MoDem 42 = 350 ; droite = LR 112 + UDI 18 + DVD 6 + Debout la France 1 = 137 ;
    #          FN 8 + EXD 1 = 9 ; autres (régionalistes, divers) 8.
    #   2022 : gauche = NUPES 131 + DVG 22 = 153 ; Ensemble 245 + divers centre 4 = 249 ; droite = LR 61 +
    #          DVD 10 + UDI 3 + droite souverainiste 1 = 75 ; RN 89 ; autres 11.
    #   2024 : gauche = UG 178 + DVG 12 + SOC 2 + ECO 1 = 193 ; centre = Ensemble 150 + Horizons 6 + DVC 6 +
    #          UDI 3 = 165 ; droite = LR 39 + DVD 27 = 66 ; RN 125 + UXD 17 + EXD 1 = 143 ; autres 10.
    # Octobre 2026 : groupes, Assemblée nationale, « Effectif des groupes politiques » (consulté le
    #   9 octobre 2026) : gauche = LFI 70 + Socialistes 68 + Écologiste et social 38 + GDR 17 = 193 ;
    #   centre = EPR 90 + Démocrates 37 + Horizons 35 = 162 ; Droite républicaine 47 ; RN 121 + UDR 17 = 138 ;
    #   LIOT 23 + non-inscrits 11 = 34 ; 3 sièges vacants.
    # (Les groupes d'octobre 2026 sont donnés dans un tableau du chapitre, section 1.4 : pas ici.)
    cols = ["Législatives 2017", "Législatives 2022", "Législatives 2024"]
    series = [
        ("Gauche", RED, [73, 153, 193]),
        ("Centre (camp présidentiel)", YELLOW, [350, 249, 165]),
        ("Droite (LR et alliés)", BLUE, [137, 75, 66]),
        ("RN et alliés", VIOLET, [9, 89, 143]),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.19)
    w = 0.19
    for k, (lab, col, vals) in enumerate(series):
        xs = [i + (k - 1.5) * w for i in range(len(cols))]
        ax.bar(xs, vals, width=w * 0.92, color=col, label=lab, edgecolor=SURFACE, linewidth=0.8)
        for x, v in zip(xs, vals):
            ax.text(x, v + 5, str(v), ha="center", va="bottom", fontsize=8.8, color=INK)
    ax.axhline(289, color=INK, linewidth=1.2, linestyle=(0, (3, 2)))
    ax.text(2.52, 293, "Majorité absolue : 289", fontsize=9.5, color=INK, ha="right", va="bottom")
    ax.set_xticks(range(len(cols)), cols)
    ax.set_ylim(0, 385)
    ax.set_ylabel("Nombre de députés (577 au total)")
    ax.legend(loc="upper right", ncol=4, fontsize=9.3, bbox_to_anchor=(1.0, 1.08))
    hgrid(ax)
    finish(fig, "01_blocs_assemblee.png",
           "Depuis 2022, aucun bloc n'atteint la majorité absolue à l'Assemblée",
           "Sièges obtenus par bloc aux élections législatives, selon la nuance politique des élus",
           "Source : ministère de l'Intérieur, résultats des législatives 2017, 2022 et 2024 (sièges par nuance). "
           "Regroupement des nuances en blocs : calcul. Non représentés : régionalistes et divers (8 à 11 sièges).")


# ===========================================================================
# 2. Le 49.3 par Premier ministre
# ===========================================================================
def recours_49_3():
    # Assemblée nationale, « Engagements de responsabilité du Gouvernement et motions de censure depuis
    # 1958 » (bilan par Premier ministre, mise à jour du 09/09/2025) ; pour F. Bayrou, 4 engagements
    # (tableau détaillé de la même page et statistiques de la XVIIe législature : 8 engagements =
    # Barnier 1 + Bayrou 4 + Lecornu 3) ; pour S. Lecornu, 3 engagements (20, 23 et 30 janvier 2026,
    # page de la XVIIe législature et AFP). Premiers ministres sans 49.3 : Couve de Murville,
    # Chaban-Delmas, Messmer, Chirac (1974-1976), Jospin, Fillon, Ayrault, Castex, Attal.
    rows = [
        ("Debré (1959-1962)", 4), ("Pompidou (1962-1968)", 6), ("Barre (1976-1981)", 8),
        ("Mauroy (1981-1984)", 7), ("Fabius (1984-1986)", 4), ("Chirac (1986-1988)", 8),
        ("Rocard (1988-1991)", 28), ("Cresson (1991-1992)", 8), ("Bérégovoy (1992-1993)", 3),
        ("Balladur (1993-1995)", 1), ("Juppé (1995-1997)", 2), ("Raffarin (2002-2005)", 2),
        ("Villepin (2005-2007)", 1), ("Valls (2014-2016)", 6), ("Philippe (2017-2020)", 1),
        ("Borne (2022-2024)", 23), ("Barnier (2024)", 1), ("Bayrou (2024-2025)", 4),
        ("Lecornu (depuis 2025)", 3),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 6.6))
    fig.subplots_adjust(left=0.2, right=0.97, top=0.86, bottom=0.165)
    y = list(range(len(rows)))[::-1]
    for yi, (name, n) in zip(y, rows):
        recent = name.startswith(("Borne", "Barnier", "Bayrou", "Lecornu"))
        ax.barh(yi, n, color=BLUE if recent else "#bcd6f3", height=0.66)
        ax.text(n + 0.3, yi, str(n), va="center", fontsize=9.3, color=INK)
    ax.axhline(3.5, color=BASE, linewidth=1)
    ax.text(29.5, 0.6, "Depuis 2022 : 31 recours", ha="right", va="center", fontsize=9.5, color=INK)
    ax.text(29.5, 17.5, "1958-2022 : 89 recours", ha="right", va="center", fontsize=9.5, color=INK2)
    ax.set_yticks(y, [r[0] for r in rows])
    ax.set_xlim(0, 30)
    ax.set_xlabel("Nombre d'engagements de responsabilité (49.3)")
    vgrid(ax)
    finish(fig, "02_recours_49_3.png",
           "Michel Rocard (28) et Élisabeth Borne (23) ont le plus utilisé le 49.3",
           "Nombre de recours au 49.3 par Premier ministre, 1958-2026 (hors Premiers ministres qui n'y ont pas eu recours)",
           "Sources : Assemblée nationale, bilan des engagements de responsabilité (septembre 2025) et page de la "
           "XVIIe législature ; Agence France-Presse (janvier 2026). Depuis 2008, le 49.3 est limité aux budgets "
           "et à un autre texte par session.")


# ===========================================================================
# 3. Participation aux élections
# ===========================================================================
def participation():
    # Présidentielle, 1er tour, % des inscrits : 1965-2007 : proposition de loi constitutionnelle
    # n° 3400 (Assemblée nationale, 2011) et ministère de l'Intérieur (2002, 2007) ; 2012, 2017 :
    # ministère de l'Intérieur ; 2022 : Conseil constitutionnel, décision n° 2022-195 PDR (calcul).
    pres = {1965: 84.75, 1969: 77.59, 1974: 84.23, 1981: 81.09, 1988: 81.35, 1995: 78.38,
            2002: 71.60, 2007: 83.77, 2012: 79.48, 2017: 77.77, 2022: 73.69}
    # Législatives, 1er tour : 2012-2024 : ministère de l'Intérieur ; 1958-2007 : série reprise par
    # Wikipédia (« Electoral abstention in France »), à vérifier sur les archives du ministère.
    leg = {1958: 77.18, 1962: 68.7, 1967: 80.89, 1968: 80.01, 1973: 80.24, 1978: 82.78, 1981: 70.65,
           1986: 78.5, 1988: 65.74, 1993: 68.95, 1997: 67.92, 2002: 64.42, 2007: 60.44, 2012: 57.22,
           2017: 48.70, 2022: 47.51, 2024: 66.71}
    # Européennes : ministère de l'Intérieur (2019 : 50,12 % ; 2024 : 51,49 %).
    eur = {2019: 50.12, 2024: 51.49}
    fig, ax = plt.subplots(figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.16)
    ax.plot(list(pres), list(pres.values()), color=BLUE, linewidth=2.2, marker="o", markersize=5,
            markeredgecolor=SURFACE, label="Présidentielle, 1er tour")
    ax.plot(list(leg), list(leg.values()), color=ORANGE, linewidth=2.2, marker="o", markersize=5,
            markeredgecolor=SURFACE, label="Législatives, 1er tour")
    ax.scatter(list(eur), list(eur.values()), color=MUTED, s=36, zorder=3, label="Européennes")
    for x, v, dy in [(2022, 73.69, 2.2), (2022, 47.51, -4.2), (2024, 66.71, 2.2), (2017, 48.70, -4.2)]:
        ax.text(x, v + dy, f"{v:.1f}".replace(".", ","), ha="center", fontsize=9, color=INK)
    ax.set_ylim(0, 100)
    ax.set_xlim(1956, 2027)
    ax.set_ylabel("Participation, % des inscrits")
    ax.legend(loc="lower left", fontsize=9.5)
    hgrid(ax)
    finish(fig, "04_participation.png",
           "La participation aux législatives a baissé jusqu'en 2022, puis remonté en 2024",
           "Participation au premier tour, en % des électeurs inscrits",
           "Sources : ministère de l'Intérieur ; Conseil constitutionnel ; Assemblée nationale (proposition de loi "
           "n° 3400, 2011). Législatives 1958-2007 : série publiée par Wikipédia, à vérifier.")


# ===========================================================================
# 4. Confiance dans les institutions (Cevipof)
# ===========================================================================
def confiance():
    # Baromètre de la confiance politique, Cevipof (Sciences Po) - OpinionWay, vagues 1 (déc. 2009),
    # 9 à 12 et 14 à 17 (janvier 2026). France, inscrits sur les listes électorales. Vague 13 (2022)
    # non lue pour la confiance ; « démocratie fonctionne mal » 2022 = 57 (graphique de la vague 15).
    yrs = [2009, 2017, 2018, 2020, 2021, 2023, 2024, 2025, 2026]
    gouv = [32, 30, 22, 27, 35, 26, 28, 23, 17]
    an = [38, 29, 23, 31, 38, 28, 29, 24, 20]
    mal_y = [2009, 2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    mal = [48, 61, 70, 64, 55, 57, 64, 68, 71, 76]
    fig, ax = plt.subplots(figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.16)
    for xs_, ys_, col, lab in [(mal_y, mal, RED, "La démocratie fonctionne mal"),
                               (yrs, an, BLUE, "Confiance dans l'Assemblée nationale"),
                               (yrs, gouv, AQUA, "Confiance dans le gouvernement")]:
        # 2009 isolé : les vagues 2010 à 2016 ne sont pas reprises, pas de ligne entre 2009 et 2017
        ax.plot(xs_[1:], ys_[1:], color=col, linewidth=2.2, marker="o", markersize=5, markeredgecolor=SURFACE,
                label=lab)
        ax.plot(xs_[:1], ys_[:1], color=col, marker="o", markersize=5, markeredgecolor=SURFACE, linestyle="none")
    for v, col, dy in [(76, RED, 2.5), (20, BLUE, 2.5), (17, AQUA, -5.5)]:
        ax.text(2026, v + dy, f"{v} %", ha="center", fontsize=9.5, color=col, fontweight="semibold")
    ax.axvspan(2009.5, 2016.5, color="#f1f0eb", zorder=0)
    ax.text(2013, 92, "Vagues 2010 à 2016\nnon reprises",
            ha="center", fontsize=8.5, color=INK2)
    ax.set_ylim(0, 100)
    ax.set_xlim(2008.5, 2026.8)
    ax.set_ylabel("% des personnes interrogées")
    ax.set_xticks(mal_y, [str(y) for y in mal_y])
    ax.legend(loc="lower left", fontsize=9.5, bbox_to_anchor=(0.07, 0.0))
    hgrid(ax)
    finish(fig, "03_confiance.png",
           "En janvier 2026, trois Français sur quatre jugent que la démocratie fonctionne mal",
           "Réponses des inscrits sur les listes électorales, en %, chaque début d'année (décembre en 2009, 2017 et 2018)",
           "Source : Cevipof (Sciences Po) - OpinionWay, Baromètre de la confiance politique, vagues 1, 9 à 12 et 14 "
           "à 17 (2022 : graphique de la vague 15). Confiance : « très » ou « plutôt » confiance.")


if __name__ == "__main__":
    blocs()
    recours_49_3()
    participation()
    confiance()
    print("Graphiques écrits dans", OUT)
