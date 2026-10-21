"""Graphiques du chapitre « Retraites et productivité ».
Toutes les données sont sourcées dans le chapitre (retraites_productivite.md)
et dans les notes de recherche (non publiées).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
from matplotlib.ticker import FuncFormatter

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
LIGHT = "#9dbfe8"
NEUTRAL = "#6f6e69"

plt.rcParams.update({
    "font.family": FONT, "font.size": 10.5, "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE, "xtick.color": MUTED, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlelocation": "left", "axes.titlesize": 12, "axes.titleweight": "semibold",
    "legend.frameon": False,
})


def finish(fig, name, title, subtitle, source):
    t = fig.suptitle(title, x=0.02, y=0.995, ha="left", va="top", fontsize=14.5, fontweight="bold", color=INK)
    h = fig.get_figheight()
    fig.text(0.02, 1 - 0.31 / h, subtitle, ha="left", va="top", fontsize=10.5, color=INK2)
    s = fig.text(0.02, 0.012, source, ha="left", va="bottom", fontsize=8.2, color=MUTED)
    fig.savefig(OUT / name, dpi=200)
    # Contrôle : le titre et la source tiennent dans la largeur de l'image.
    r = fig.canvas.get_renderer()
    w = fig.get_figwidth() * fig.dpi
    for lab, txt in (("titre", t), ("source", s)):
        right = txt.get_window_extent(renderer=r).x1
        marge = (w - right) * 200 / fig.dpi
        if marge < 45:
            print(f"ATTENTION {name} : {lab} trop long (marge {marge:.0f} px à 200 dpi)")
    plt.close(fig)


def hgrid(ax):
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def vgrid(ax):
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def fr(x, fmt="{:.1f}"):
    return fmt.format(x).replace(".", ",").replace("-", "−")


# ===========================================================================
# 1. Emploi des 60-64 ans (graphique de « L'essentiel »)
# ===========================================================================
def emploi_seniors():
    yrs = list(range(2015, 2026))
    series = {  # Eurostat, lfsa_ergan, 60-64 ans, mise à jour du 10 septembre 2026
        "Suède": ([66.1, 67.5, 68.2, 70.5, 69.9, 69.2, 67.3, 68.3, 68.9, 69.5, 71.1], YELLOW, 1.7),
        "Allemagne": ([53.3, 56.0, 58.4, 60.3, 61.8, 60.6, 61.2, 63.2, 65.3, 66.6, 67.6], ORANGE, 1.7),
        "UE-27": ([36.8, 39.0, 41.3, 43.1, 44.7, 45.3, 46.4, 48.5, 50.9, 53.0, 55.0], INK2, 1.9),
        "Italie": ([34.2, 36.9, 39.6, 41.1, 41.6, 40.8, 39.5, 41.2, 44.1, 47.2, 50.4], MAGENTA, 1.7),
        "Belgique": ([23.9, 25.3, 27.8, 30.0, 32.8, 34.3, 36.7, 39.1, 40.6, 43.8, 46.8], AQUA, 1.7),
        "France": ([27.7, 28.3, 29.6, 31.2, 32.7, 33.1, 35.5, 36.2, 38.9, 42.4, 44.4], BLUE, 2.8),
    }
    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    fig.subplots_adjust(left=0.06, right=0.86, top=0.8, bottom=0.13)
    ypos = {"Suède": 71.1, "Allemagne": 67.3, "UE-27": 55.0, "Italie": 50.4, "Belgique": 46.9, "France": 43.6}
    for lab, (v, c, lw) in series.items():
        ls = (0, (4, 2)) if lab == "UE-27" else "-"
        ax.plot(yrs, v, color=c, linewidth=lw, linestyle=ls, marker="o" if lab == "France" else None,
                markersize=4, markeredgecolor=SURFACE, zorder=4 if lab == "France" else 3)
        ax.text(2025.3, ypos[lab], f"{lab} : {fr(v[-1])} %", va="center", fontsize=10,
                color=c if lab != "UE-27" else INK2, fontweight="semibold" if lab == "France" else "normal")
    for yb in (2021, 2024):
        ax.annotate("rupture\nde série", xy=(yb, series["France"][0][yb - 2015]), xytext=(yb + 0.15, 22.5),
                    fontsize=8.2, color=BLUE, ha="left",
                    arrowprops=dict(arrowstyle="-", color=BLUE, linewidth=0.8, linestyle=":"))
    ax.set_xlim(2014.7, 2025.2)
    ax.set_ylim(0, 80)
    ax.set_xticks(range(2015, 2026))
    ax.set_ylabel("Taux d'emploi des 60-64 ans, en %")
    ax.set_clip_on(False)
    hgrid(ax)
    finish(fig, "01_emploi_seniors.png",
           "Entre 60 et 64 ans, l'emploi est moins fréquent en France que dans l'UE ; l'écart se réduit depuis 2022",
           "Part des personnes de 60 à 64 ans qui ont un emploi, de 2015 à 2025.",
           "Source : Eurostat, enquête sur les forces de travail (lfsa_ergan), mise à jour du 10 septembre 2026. "
           "France : ruptures de série en 2021 et en 2024 (changement de questionnaire).")


# ===========================================================================
# 2. Dépenses publiques, capitalisation, pauvreté
# ===========================================================================
def depenses_pauvrete():
    pays = ["Italie", "France", "Espagne", "Belgique", "Allemagne", "Danemark", "Suède", "Royaume-Uni",
            "Pays-Bas"]
    # OCDE, Panorama des pensions 2025, tableau 8.4 (pays de l'UE : Ageing Report 2024 ; Royaume-Uni : OBR)
    dep = [15.5, 14.1, 13.6, 12.8, 10.2, 8.7, 8.0, 7.6, 6.6]
    # OCDE, Panorama des pensions 2025, tableau 9.2 (actifs destinés à la retraite, fin 2024)
    act = [11.7, 12.9, 10.8, 30.3, 6.4, 206.4, 115.8, 78.4, 150.9]
    # OCDE, Panorama des pensions 2025, tableau 7.2 (65 ans et plus, seuil à 50 % du revenu médian, 2022)
    pov = [12.0, 6.1, 13.1, 7.7, 12.6, 5.0, 7.3, 15.0, 4.6]
    y = np.arange(len(pays))[::-1]
    fig, axs = plt.subplots(1, 3, figsize=(12.5, 5.6), sharey=True)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.78, bottom=0.12, wspace=0.12)
    specs = [(dep, "A. Dépenses publiques de retraite\n(% du PIB, 2023-2024)", 18, "{:.1f}"),
             (act, "B. Épargne retraite en capitalisation\n(actifs des fonds, % du PIB, 2024)", 245, "{:.0f}"),
             (pov, "C. Pauvreté des 65 ans et plus\n(% sous 50 % du revenu médian, 2022)", 22, "{:.1f}")]
    for ax, (vals, title, xmax, fmt) in zip(axs, specs):
        cols = [BLUE if p == "France" else LIGHT for p in pays]
        ax.barh(y, vals, color=cols, height=0.62)
        for yy, v in zip(y, vals):
            ax.text(v + xmax * 0.015, yy, fr(v, fmt), va="center", fontsize=9, color=INK)
        ax.set_xlim(0, xmax)
        ax.set_title(title, pad=8, fontsize=11)
        vgrid(ax)
    axs[0].set_yticks(y, pays)
    axs[0].axvline(9.9, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    axs[0].text(10.1, 8.45, "UE : 9,9", fontsize=8.5, color=INK2)
    axs[2].axvline(14.8, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    axs[2].text(15.0, 8.45, "OCDE : 14,8", fontsize=8.5, color=INK2)
    finish(fig, "02_depenses_pauvrete.png",
           "La France dépense plus que la plupart de ses voisins pour ses retraites ; ses 65 ans et plus sont moins pauvres",
           "Les pays qui dépensent moins en retraites publiques complètent souvent par une épargne en "
           "capitalisation obligatoire ou quasi obligatoire.",
           "Source : OCDE, Panorama des pensions 2025 (tableaux 8.4, 9.2 et 7.2 ; dépenses de l'UE d'après l'Ageing "
           "Report 2024 de la Commission européenne). UE : moyenne simple. Pauvreté : seuil à 50 % du revenu médian.")


# ===========================================================================
# 3. Productivité horaire : niveau et évolution
# ===========================================================================
def productivite():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.6), gridspec_kw={"width_ratios": [1, 1.25]})
    fig.subplots_adjust(left=0.1, right=0.9, top=0.78, bottom=0.13, wspace=0.32)
    lv = [("Danemark", 137.7), ("Belgique", 131.0), ("Pays-Bas", 126.0), ("Allemagne", 124.2), ("France", 114.7),
          ("Suède", 108.8), ("Zone euro", 107.1), ("UE-27", 100.0), ("Italie", 96.3), ("Espagne", 95.3)][::-1]
    cols = [BLUE if n == "France" else (MUTED if n in ("UE-27", "Zone euro") else LIGHT) for n, _ in lv]
    ax1.barh(range(len(lv)), [v for _, v in lv], color=cols, height=0.62)
    for i, (n, v) in enumerate(lv):
        ax1.text(v + 1.5, i, f"{v:.0f}", va="center", fontsize=9.5, color=INK)
    ax1.set_yticks(range(len(lv)), [n for n, _ in lv])
    ax1.set_xlim(0, 160)
    ax1.set_xlabel("PIB par heure travaillée, UE-27 = 100 (2025)")
    ax1.set_title("A. Niveau en 2025", pad=8)
    vgrid(ax1)

    yrs = list(range(2015, 2026))
    i15 = {  # Eurostat, nama_10_lp_ulc (RLPR_HW, 2015 = 100), 2015-2025
        "France": [100.000, 99.953, 101.909, 102.065, 102.548, 102.726, 101.330, 99.770, 100.146, 100.177, 101.678],
        "Allemagne": [100.000, 101.416, 103.499, 103.968, 104.798, 105.810, 107.553, 107.616, 106.353, 105.984, 107.107],
        "Zone euro": [100.000, 100.206, 101.745, 101.858, 102.506, 104.717, 105.004, 104.851, 103.547, 103.373, 104.398],
        "Espagne": [100.000, 100.353, 101.095, 101.023, 101.256, 101.302, 100.784, 102.036, 101.825, 103.042, 103.807],
    }
    style = {"France": (BLUE, 2.6), "Allemagne": (ORANGE, 1.8), "Zone euro": (INK2, 1.8), "Espagne": (AQUA, 1.8)}
    last = {}
    for lab, v in i15.items():
        reb = [100 * x / v[4] for x in v]
        last[lab] = reb[-1]
        c, lw = style[lab]
        ax2.plot(yrs, reb, color=c, linewidth=lw, marker="o" if lab == "France" else None, markersize=3.5,
                 markeredgecolor=SURFACE, zorder=4 if lab == "France" else 3)
    ypos = {"Espagne": 103.0, "Allemagne": 102.35, "Zone euro": 101.7, "France": 99.0}
    for lab in i15:
        ax2.text(2025.25, ypos[lab], f"{lab} : {fr(last[lab])}", va="center", fontsize=9.5,
                 color=style[lab][0], fontweight="semibold" if lab == "France" else "normal")
    tr = [100 * 1.007 ** (y - 2019) for y in range(2019, 2026)]
    ax2.plot(range(2019, 2026), tr, color=BLUE, linewidth=1.2, linestyle=(0, (3, 2)))
    ax2.text(2025.25, tr[-1], f"tendance : {fr(tr[-1])}", va="center", fontsize=9, color=BLUE)
    ax2.axvline(2019, color=GRID, linewidth=1)
    ax2.set_xlim(2014.6, 2025.2)
    ax2.set_ylim(94, 106)
    ax2.set_xticks([2015, 2017, 2019, 2021, 2023, 2025])
    ax2.set_ylabel("Productivité horaire réelle, 2019 = 100")
    ax2.set_title("B. Évolution depuis 2015", pad=8)
    ax2.set_clip_on(False)
    hgrid(ax2)
    finish(fig, "03_productivite_horaire.png",
           "La France produit plus par heure que la moyenne de l'UE, mais reste sous sa tendance d'avant 2019",
           "Productivité horaire de l'ensemble de l'économie. Pointillés : France si la productivité avait "
           "progressé de 0,7 % par an depuis 2019 (convention de l'Insee).\nEn 2025, la France est 4,9 % "
           "sous cette tendance.",
           "Source : Eurostat, tesem160 (niveau, en standards de pouvoir d'achat) et nama_10_lp_ulc (évolution, "
           "rebasée 2019 = 100), octobre 2026.")


# ===========================================================================
# 4. Décomposition de l'écart de PIB par habitant
# ===========================================================================
def decomposition():
    rows = [("Pays-Bas", -30.4, -9.4, 4.5, -25.5), ("Danemark", -28.1, -18.3, 9.8, -19.6),
            ("Allemagne", -17.7, -8.0, 11.5, -21.3), ("Belgique", -15.8, -13.3, -5.6, 3.1),
            ("Suède*", -12.9, 5.3, -4.3, -13.9), ("Zone euro", -6.1, 6.9, -3.4, -9.6),
            ("UE-27", -2.4, 13.7, -6.7, -9.4), ("Italie", 1.6, 17.5, -13.5, -2.4),
            ("Espagne", 6.5, 18.5, -8.5, -3.5)][::-1]
    comps = [("Productivité horaire", BLUE), ("Heures par personne en emploi", YELLOW),
             ("Personnes en emploi par habitant", ORANGE)]
    fig, ax = plt.subplots(figsize=(12.5, 6.6))
    fig.subplots_adjust(left=0.165, right=0.97, top=0.79, bottom=0.12)
    h = 0.24
    for j, (lab, c) in enumerate(comps):
        ax.barh(np.arange(len(rows)) + (1 - j) * h, [r[2 + j] for r in rows], h, color=c, label=lab)
    ax.scatter([r[1] for r in rows], range(len(rows)), marker="D", s=60, color=INK, zorder=4,
               label="Écart total de PIB par habitant")
    for i, r in enumerate(rows):
        ax.text(r[1] + (1.1 if r[1] >= 0 else -1.1), i, fr(r[1], "{:+.1f}"), fontsize=9.5, va="center",
                ha="left" if r[1] >= 0 else "right", color=INK, fontweight="semibold")
    ax.axvline(0, color=INK2, linewidth=1)
    ax.set_yticks(range(len(rows)), [f"France vs {r[0]}" for r in rows])
    ax.set_xlim(-36, 24)
    ax.set_xlabel("Écart de la France, en points de log (proches de % pour les petits écarts) ; négatif : "
                  "la France est en dessous")
    ax.legend(loc="lower left", bbox_to_anchor=(-0.01, 1.0), ncol=4, fontsize=9.2)
    vgrid(ax)
    finish(fig, "04_decomposition_pib_habitant.png",
           "Face à l'Allemagne, l'écart de richesse par habitant vient du nombre de personnes en emploi",
           "Les Français en emploi travaillent plus d'heures que les Allemands ou les Néerlandais, "
           "mais il y a moins de personnes en emploi par habitant.",
           "Calcul à partir d'Eurostat 2025 (tesem160, nama_10_a10_e, nama_10_pe), octobre 2026. Les trois barres "
           "s'additionnent pour donner l'écart total. * Suède : heures par emploi incertaines.")


# ===========================================================================
# 5. Âges de départ en Europe
# ===========================================================================
def ages_europe():
    # Cnav (circulaire 2026-07) ; Deutsche Rentenversicherung (66 ans et 4 mois pour la génération 1960) ;
    # Seguridad Social ; INPS (circulaire n° 28 de 2026) ; Rijksoverheid ; Pensionsmyndigheten ;
    # ministère danois de l'Emploi (22 mai 2025) ; gouvernement belge (réforme de 2015)
    rows = [  # pays, âge 2026, âge prévu, libellé
        ("France", 62.75, 64, "64 ans pour les personnes nées à partir de 1969"),
        ("Belgique", 66, 67, "67 ans en 2030"),
        ("Allemagne", 66.33, 67, "67 ans en 2031"),
        ("Espagne", 66.83, 67, "67 ans en 2027 (65 ans avec 38 ans et 6 mois)"),
        ("Italie", 67, 67.25, "lié à l'espérance de vie : 67 ans et 3 mois en 2028"),
        ("Pays-Bas", 67, 67.25, "lié à l'espérance de vie : 67 ans et 3 mois en 2028"),
        ("Suède", 67, 67, "âge de référence ; départ possible dès 64 ans"),
        ("Danemark", 67, 70, "70 ans en 2040 (loi de 2025)"),
    ][::-1]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.1, right=0.97, top=0.8, bottom=0.15)
    for i, (n, a, b, t) in enumerate(rows):
        c = BLUE if n == "France" else INK2
        ax.axhline(i, color=GRID, linewidth=0.8, zorder=0)
        if b != a:
            ax.annotate("", xy=(b, i), xytext=(a, i),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.4, shrinkA=5, shrinkB=4))
            ax.scatter([b], [i], s=70, facecolor=SURFACE, edgecolor=c, linewidth=1.6, zorder=3)
        ax.scatter([a], [i], s=80, color=c, zorder=4)
        ax.text(70.6, i, t, va="center", fontsize=9.2, color=BLUE if n == "France" else INK2)
    ax.text(62.75, len(rows) - 1 + 0.38, "62 ans et 9 mois", ha="center", fontsize=8.8, color=BLUE)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlim(62, 77.5)
    ax.set_xticks(range(62, 71))
    ax.spines["bottom"].set_bounds(62, 70)
    ax.set_ylim(-0.6, len(rows) - 0.2)
    ax.set_xlabel("Âge, en années (66,33 = 66 ans et 4 mois)")
    ax.scatter([], [], s=80, color=INK2, label="Âge légal ou de référence en 2026")
    ax.scatter([], [], s=70, facecolor=SURFACE, edgecolor=INK2, linewidth=1.6, label="Âge prévu par la loi")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, fontsize=9.2)
    finish(fig, "05_ages_depart_europe.png",
           "L'âge légal français est le plus bas des huit pays comparés, mais il s'ajoute à une condition de durée",
           "En France, c'est un âge minimal : le taux plein exige aussi 170 à 172 trimestres, ou 67 ans. "
           "Les comparaisons d'âge simplifient des règles différentes.",
           "Sources : Cnav (circulaire 2026-07) ; INPS (Italie) ; gouvernement néerlandais ; Agence suédoise des "
           "pensions ; Seguridad Social ; ministère danois de l'Emploi ; Deutsche Rentenversicherung ; gouvernement belge.")


# ===========================================================================
# 6. Effets des leviers (COR 2026, tableau 2.10)
# ===========================================================================
def leviers():
    rows = [("Reculer l'âge d'un an", (0.5, 0.7), (160, 250)),
            ("Modérer les pensions", (-0.2, -0.1), (-25, -10)),
            ("Hausser les cotisations des salariés", (-0.2, -0.1), (-70, -20)),
            ("Hausser les cotisations des employeurs", (-0.3, -0.1), (-75, -20))][::-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.6), sharey=True)
    fig.subplots_adjust(left=0.25, right=0.98, top=0.72, bottom=0.16, wspace=0.1)
    for ax, k, xl, unit, lim in [(ax1, 1, "Effet sur le PIB à dix ans, en %", "%", (-0.75, 1.0)),
                                 (ax2, 2, "Effet sur l'emploi à dix ans, en milliers", "k", (-190, 360))]:
        for i, r in enumerate(rows):
            lo, hi = r[k]
            ax.plot([lo, hi], [i, i], color=NEUTRAL, linewidth=3, solid_capstyle="butt", zorder=3)
            ax.scatter([lo, hi], [i, i], s=40, color=NEUTRAL, zorder=4)
            txt = fr(lo, "{:+.1f}") + " à " + fr(hi, "{:+.1f}") if unit == "%" else \
                fr(lo, "{:+.0f}") + " à " + fr(hi, "{:+.0f}")
            ax.text(hi + (lim[1] - lim[0]) * 0.02 if lo > 0 else lo - (lim[1] - lim[0]) * 0.02, i, txt,
                    va="center", ha="left" if lo > 0 else "right", fontsize=9.3, color=INK)
        ax.axvline(0, color=INK2, linewidth=1)
        ax.set_xlim(*lim)
        f_ = "{:.1f}" if k == 1 else "{:.0f}"
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _, f_=f_: fr(x, f_)))
        ax.set_xlabel(xl)
        ax.set_ylim(-0.6, len(rows) - 0.4)
        vgrid(ax)
    ax1.set_yticks(range(len(rows)), [r[0] for r in rows])
    finish(fig, "06_leviers_retraites.png",
           "Selon les modèles réunis par le COR, seul le recul de l'âge augmente le PIB et l'emploi",
           "Un an d'âge de départ en plus, ou une mesure qui rapporte 6 Md€ (0,2 point de PIB) avant ses effets sur l'économie.\n"
           "Chaque trait va de l'estimation la plus basse à la plus haute des trois modèles (DG Trésor, OFCE, i-MIP).",
           "Source : COR, rapport annuel 2026, partie 2, chapitre 6, tableau 2.10. Le recul de l'âge a aussi "
           "des coûts (chômage, invalidité) : voir la section 4.")


if __name__ == "__main__":
    emploi_seniors()
    depenses_pauvrete()
    productivite()
    decomposition()
    ages_europe()
    leviers()
    print("ok", sorted(p.name for p in OUT.glob("*.png")))
