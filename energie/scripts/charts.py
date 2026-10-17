"""Graphiques du chapitre « Énergie ».
Toutes les données sont sourcées dans le chapitre (energie_france_europe_allemagne.md). Valeurs « ≈ » = approximatives.
Les graphiques sur TotalEnergies sont dans finances-publiques/scripts/charts_totalenergies.py.
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
# 1. Ordre de mérite (illustratif)
# ===========================================================================
def merit_order():
    blocks = [  # (nom, capacité GW, coût marginal €/MWh, couleur)
        ("Éolien\n+ solaire", 45, 2, AQUA),
        ("Nucléaire", 55, 12, BLUE),
        ("Charbon", 15, 80, YELLOW),
        ("Gaz\n(cycle\ncombiné)", 20, 95, VIOLET),
        ("Pointe\ngaz/fioul", 12, 180, ORANGE),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6), sharey=True)
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.14, wspace=0.08)

    def draw(ax, extra_ren, demand, title):
        x = 0
        for i, (name, cap, cost, col) in enumerate(blocks):
            w = cap + (extra_ren if i == 0 else 0)
            ax.bar(x, max(cost, 2.5), width=w - 0.8, align="edge", color=col, edgecolor=SURFACE, linewidth=1.5)
            ax.text(x + w / 2, max(cost, 2.5) + 6, name, ha="center", va="bottom", fontsize=8.8, color=INK2,
                    linespacing=0.95)
            x += w
        # prix = coût du dernier bloc nécessaire
        cum, price = 0, None
        for i, (name, cap, cost, col) in enumerate(blocks):
            w = cap + (extra_ren if i == 0 else 0)
            if demand <= cum + w:
                price, setter = cost, name.replace("\n", " ")
                break
            cum += w
        ax.axvline(demand, color=INK, linewidth=1.6, linestyle=(0, (4, 3)))
        ax.text(demand - 1.5, 205, f"Demande\n{demand} GW", fontsize=9, color=INK, va="top", ha="right")
        ax.axhline(price, color=RED, linewidth=1.4)
        ax.text(2, price + (3 if price > 30 else 24), f"Prix pour TOUS : {price} €/MWh\n(fixé par : {setter})", color=RED,
                fontsize=9.5, fontweight="semibold", va="bottom")
        ax.set_xlim(0, 190)
        ax.set_ylim(0, 215)
        ax.set_title(title, pad=8)
        ax.set_xlabel("Capacité disponible, empilée de la moins chère à la plus chère (GW)")
        hgrid(ax)

    draw(axes[0], 0, 125, "A. Le prix est celui de la dernière centrale appelée")
    draw(axes[1], 30, 125, "B. Même demande, +30 GW d'éolien/solaire : le prix baisse")
    axes[0].set_ylabel("Coût marginal de production (€/MWh)")
    finish(fig, "01_ordre_de_merite.png",
           "Le prix de gros est fixé par la dernière centrale appelée (« ordre de mérite »)",
           "Illustration : chiffres indicatifs, pas un pays réel. Les renouvelables, à coût marginal ≈ 0, "
           "repoussent les centrales chères hors du marché.",
           "Coûts marginaux indicatifs (combustible + CO₂ à ~75 €/t). Mécanisme : règlement (UE) 2019/943 et "
           "algorithme de couplage européen (prix marginal uniforme).")


# ===========================================================================
# 2. Mix électrique 2025 France vs Allemagne
# ===========================================================================
def mix_electrique():
    cats = ["Nucléaire", "Hydraulique", "Éolien", "Solaire", "Bioénergies\n& déchets",
            "Gaz", "Charbon\n& lignite", "Fioul\n& autres"]
    fr = [373.0, 62.4, 49.6, 32.9, 10.9, 16.4, 0.7, 1.7]
    de = [0.0, 16.2, 133.0, 91.0, 48.3, 84.9, 104.8, 20.4]
    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.17)
    import numpy as np
    x = np.arange(len(cats))
    w = 0.38
    b1 = ax.bar(x - w / 2 - 0.01, fr, w, color=BLUE, label="France (547 TWh produits)")
    b2 = ax.bar(x + w / 2 + 0.01, de, w, color=ORANGE, label="Allemagne (499 TWh produits)")
    for bars, vals in ((b1, fr), (b2, de)):
        for r, v in zip(bars, vals):
            ax.text(r.get_x() + r.get_width() / 2, v + 4, f"{v:.0f}" if v >= 1 else ("<1" if v > 0 else "0"),
                    ha="center", va="bottom", fontsize=8.8, color=INK2)
    ax.set_xticks(x, cats)
    ax.set_ylabel("Production d'électricité 2025 (TWh)")
    ax.set_ylim(0, 410)
    # séparation bas-carbone / fossile
    ax.axvline(4.5, color=BASE, linewidth=1, linestyle=(0, (2, 2)))
    ax.text(2.0, 395, "BAS-CARBONE", ha="center", fontsize=9.5, color=MUTED, fontweight="semibold")
    ax.text(6.0, 395, "FOSSILE", ha="center", fontsize=9.5, color=MUTED, fontweight="semibold")
    ax.text(6.0, 250, "Part fossile de l'électricité\nFrance : ≈ 3 %\nAllemagne : ≈ 39 %",
            ha="center", va="center", fontsize=10.5, color=INK, fontweight="semibold")
    ax.legend(loc="upper left", bbox_to_anchor=(0.17, 0.9))
    hgrid(ax)
    finish(fig, "02_mix_electrique_FR_DE_2025.png",
           "La France produit surtout du nucléaire, l'Allemagne de l'éolien, du solaire et des énergies fossiles",
           "Production d'électricité en 2025, en TWh.",
           "Sources : RTE, Bilan électrique 2025 (France) ; BDEW, Die Energieversorgung 2025, production brute "
           "provisoire (Allemagne). Allemagne : importatrice nette ≈ 18–22 TWh ; France : exportatrice nette 92 TWh.")


# ===========================================================================
# 3. Part des fossiles : électricité vs énergie totale
# ===========================================================================
def fossiles():
    import numpy as np
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.4), gridspec_kw={"width_ratios": [1.1, 1]})
    fig.subplots_adjust(left=0.17, right=0.985, top=0.80, bottom=0.15, wspace=0.32)

    # A. France : consommation finale d'énergie 2025 par vecteur
    lab = ["Pétrole", "Électricité", "Gaz naturel", "Chaleur renouvelable\n(bois, PAC…) & déchets",
           "Chaleur vendue\n(réseaux)", "Charbon"]
    val = [38, 27, 18, 14, 3, 0.5]
    fossil = [True, False, True, False, False, True]
    y = np.arange(len(lab))[::-1]
    cols = [ORANGE if f else BLUE for f in fossil]
    ax1.barh(y, val, color=cols, height=0.62)
    for yy, v in zip(y, val):
        ax1.text(v + 0.8, yy, "< 1 %" if v < 1 else f"{v:.0f} %", va="center", fontsize=9.5, color=INK2)
    ax1.set_yticks(y, lab)
    ax1.set_xlim(0, 46)
    ax1.set_xlabel("Part de la consommation finale d'énergie (%)")
    ax1.set_title("A. France 2025 : d'où vient l'énergie consommée ?", pad=8)
    from matplotlib.patches import Patch
    ax1.legend(handles=[Patch(color=ORANGE, label="Fossile (≈ 57 % au total)"),
                        Patch(color=BLUE, label="Non fossile")], loc="lower right")
    vgrid(ax1)

    # B. Part des énergies fossiles en France : électricité produite vs énergie finale consommée
    groups = ["Électricité\nproduite", "Énergie finale\nconsommée"]
    frv = [3.4, 57]
    x = np.arange(2)
    bars = ax2.bar(x, frv, 0.5, color=[BLUE, ORANGE])
    for r, v in zip(bars, frv):
        ax2.text(r.get_x() + r.get_width() / 2, v + 1.5, f"≈ {v:.0f} %", ha="center", fontsize=10, color=INK2)
    ax2.set_xticks(x, groups)
    ax2.set_ylim(0, 70)
    ax2.set_ylabel("Part des énergies fossiles (%)")
    ax2.set_title("B. Part des énergies fossiles en France", pad=8)
    hgrid(ax2)
    finish(fig, "03_part_fossile.png",
           "L'électricité française est presque sans énergies fossiles, mais pas l'énergie que la France consomme",
           "France, 2025. Le pétrole (transports) et le gaz (chauffage, industrie) font ≈ 57 % de l'énergie finale "
           "consommée.",
           "Sources : SDES, Chiffres clés de l'énergie 2026 et Bilan énergétique 2025 (provisoire) ; RTE, Bilan "
           "électrique 2025.")


# ===========================================================================
# 4. Prix de l'électricité des ménages
# ===========================================================================
def prix_menages():
    years = list(range(2019, 2026))
    fr = [0.185, 0.193, 0.198, 0.215, 0.245, 0.289, 0.262]
    de = [0.298, 0.302, 0.321, 0.332, 0.407, 0.395, 0.385]
    eu = [0.217, 0.215, 0.231, 0.263, 0.287, 0.290, 0.289]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.07, right=0.88, top=0.80, bottom=0.14)
    for s, col, name in ((de, ORANGE, "Allemagne"), (eu, AQUA, "Moyenne UE"), (fr, BLUE, "France")):
        ax.plot(years, [v * 100 for v in s], color=col, linewidth=2.2, marker="o", markersize=6,
                markeredgecolor=SURFACE, markeredgewidth=1.5, label=name)
        ax.text(2025.15, s[-1] * 100, f"{name}  {s[-1]*100:.1f}".replace(".", ","), va="center", fontsize=10, color=INK)
    ax.annotate("Bouclier tarifaire :\nhausse plafonnée à +4 % (2022)\npuis +15 % (2023)", xy=(2022, 21.5),
                xytext=(2022.25, 16.2), fontsize=9, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax.set_xticks(years)
    ax.set_ylabel("c€/kWh, toutes taxes comprises")
    ax.set_ylim(15, 44)
    ax.set_xlim(2018.7, 2025.1)
    hgrid(ax)
    ax.legend(loc="upper left")
    finish(fig, "04_prix_menages_FR_DE_UE.png",
           "Les ménages français paient leur électricité moins cher que la moyenne de l'UE, sauf en 2024",
           "Prix toutes taxes comprises, en centimes d'euro par kWh. L'Allemagne est parmi les pays les plus chers.",
           "Source : Eurostat nrg_pc_204, ménages consommant 2 500 à 5 000 kWh/an, toutes taxes, "
           "moyenne des deux semestres de chaque année.")


# ===========================================================================
# 5. Gaz allemand : d'où vient-il ?
# ===========================================================================
def gaz_allemand():
    import numpy as np
    cats = ["Russie", "Norvège", "Pays-Bas", "Belgique", "GNL via terminaux\nallemands", "Autres"]
    y21 = [52, 31, 13, 0, 0, 4]
    y25 = [0, 44, 24, 21, 10.3, 0.7]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.80, bottom=0.17)
    x = np.arange(len(cats))
    w = 0.38
    r1 = ax.bar(x - w / 2 - 0.01, y21, w, color=BLUE, label="2021 (avant la guerre)")
    r2 = ax.bar(x + w / 2 + 0.01, y25, w, color=ORANGE, label="2025")
    lab21 = ["52 %", "≈ 31 %", "≈ 13 %", "n.d.", "0", "≈ 4 %"]
    lab25 = ["0", "44 %", "24 %", "21 %", "10 %", "< 1 %"]
    for bars, labs, vals in ((r1, lab21, y21), (r2, lab25, y25)):
        for r, l, v in zip(bars, labs, vals):
            ax.text(r.get_x() + r.get_width() / 2, v + 1.2, l, ha="center", va="bottom", fontsize=8.8,
                    color=INK2, linespacing=0.95)
    ax.set_xticks(x, cats)
    ax.set_ylim(0, 62)
    ax.set_ylabel("Part des importations de gaz (%)")
    ax.text(4.3, 52, "GNL des terminaux allemands :\n94 % en provenance des États-Unis.\n"
                     "Les flux néerlandais et belges incluent\naussi du GNL (dont américain) et du gaz norvégien.",
            fontsize=9.2, color=INK2, ha="center", va="top")
    ax.legend(loc="upper left", bbox_to_anchor=(0.12, 1.0))
    hgrid(ax)
    finish(fig, "05_gaz_allemand_origines.png",
           "L'Allemagne a remplacé le gaz russe par la Norvège, ses voisins et le gaz naturel liquéfié",
           "La Norvège devient le 1er fournisseur, le reste arrive par les voisins et le GNL (surtout américain), "
           "et la consommation de 2025 est ≈ 13,5 % sous la moyenne 2018-2021.",
           "Sources : Bundesnetzagentur (2021 Russie, 2025 points d'entrée physiques) ; BAFA/IW (Norvège et "
           "Pays-Bas ≈, données 2020) ; AGEB/BDEW (origine du GNL). Consommation : Bundesnetzagentur.")


# ===========================================================================
# 6. France : consommation qui stagne, exportations record
# ===========================================================================
def conso_exports():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.6), gridspec_kw={"width_ratios": [1.35, 1]})
    fig.subplots_adjust(left=0.07, right=0.985, top=0.80, bottom=0.14, wspace=0.22)

    hy = [2015, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    hv = [476.3, 474, 473, 460, 468, 460.2, 445.4, 449.2, 451.2]
    ax1.plot(hy, hv, color=BLUE, linewidth=2.2, marker="o", markersize=5.5, markeredgecolor=SURFACE,
             markeredgewidth=1.5, label="Consommation réelle (corrigée du climat)")
    ax1.plot([2025, 2030, 2035], [451.2, 510, 580], color=ORANGE, linewidth=2, linestyle=(0, (5, 3)),
             marker="o", markersize=5, label="RTE 2025 : décarbonation rapide")
    ax1.plot([2025, 2030, 2035], [451.2, 470, 505], color=AQUA, linewidth=2, linestyle=(0, (5, 3)),
             marker="o", markersize=5, label="RTE 2025 : décarbonation lente")
    ax1.errorbar([2035.4], [615], yerr=[[35], [25]], fmt="s", color=VIOLET, markersize=6, capsize=4,
                 linewidth=1.5, label="RTE 2023 : référence 2035 (580–640)")
    ax1.axhline(547.5, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    ax1.text(2015.2, 551, "Production 2025 : 547 TWh", fontsize=9, color=INK2)
    ax1.annotate("", xy=(2025, 547.5), xytext=(2025, 451.2),
                 arrowprops=dict(arrowstyle="<->", color=INK2, linewidth=1))
    ax1.text(2024.6, 500, "écart ≈ 96 TWh\n= surtout des\nexportations", ha="right", va="center",
             fontsize=9, color=INK2)
    ax1.set_xlim(2014.5, 2036.3)
    ax1.set_xticks([2015, 2020, 2025, 2030, 2035])
    ax1.set_ylim(420, 660)
    ax1.set_ylabel("TWh par an")
    ax1.set_title("A. Consommation d'électricité : stagnation, puis trajectoires", pad=8)
    ax1.legend(loc="upper left", fontsize=8.8)
    hgrid(ax1)

    ey = list(range(2015, 2026))
    ev = [61.7, 39.1, 38.0, 60.2, 55.7, 43.2, 43.1, -16.5, 50.1, 89.0, 92.3]
    cols = [RED if v < 0 else BLUE for v in ev]
    bars = ax2.bar(ey, ev, color=cols, width=0.7)
    for r, v in zip(bars, ev):
        ax2.text(r.get_x() + r.get_width() / 2, v + (2 if v >= 0 else -2), f"{v:.0f}", ha="center",
                 va="bottom" if v >= 0 else "top", fontsize=8.6, color=INK2)
    ax2.axhline(0, color=BASE, linewidth=1)
    ax2.set_xticks(ey, [str(y)[2:] if y not in (2015, 2025) else str(y) for y in ey])
    ax2.set_ylim(-28, 105)
    ax2.set_ylabel("Solde exportateur net (TWh)")
    ax2.set_title("B. Solde des échanges : du déficit de 2022 aux records", pad=8)
    ax2.text(2019.6, -13, "2022 : importatrice\n(corrosion, maintenance)", ha="center", va="center", fontsize=8.6, color=RED)
    hgrid(ax2)
    finish(fig, "06_conso_exports_FR.png",
           "Des exportations record, avec une consommation d'électricité encore basse",
           "En TWh. Les records viennent en partie du retour du nucléaire après 2022, et en partie d'une consommation "
           "≈ 6 % sous la moyenne 2014-2019.",
           "Sources : RTE, Bilans électriques 2015-2025 (consommation corrigée ; 2016-2017 non repris) ; "
           "RTE, Bilan prévisionnel 2023 et 2025. 2015 : solde recalculé (91,3 exportés − 29,6 importés).")


# ===========================================================================
# 7. Coûts par MWh
# ===========================================================================
def couts_mwh():
    rows = [  # (label, min, max, point, famille, note)
        ("Nucléaire existant (CRE, 2026-28)", 60.3, 60.3, 60.3, "nuc", "60 €₂₀₂₆"),
        ("EPR2 – fourchette RTE / plafond du CfD", 60, 100, 100, "nuc", "60–100 ; plafond CfD 100 €₂₀₂₄"),
        ("Flamanville 3 (Cour des comptes)", 138, 138, 138, "nuc", "138 €₂₀₂₃ (pour 4 % de rendement)"),
        ("Éolien en mer posé (AO 2023-2025)", 44.9, 66, 66, "enr", "45–66 € (hors raccordement)"),
        ("Éolien en mer flottant (AO 2024)", 85.9, 92.7, 86.5, "enr", "86–93 €"),
        ("Éolien terrestre (AO 2025-2026)", 77.1, 86.6, 77.1, "enr", "77–87 €"),
        ("Solaire au sol (AO 2025)", 74.1, 79.5, 74.1, "enr", "74–79 €"),
        ("Solaire sur toiture (AO 2025-2026)", 83.0, 96.5, 83.0, "enr", "83–96 €"),
        ("Gaz, cycle combiné (estimation)", 90, 110, 100, "gaz", "≈ 90–110 € (gaz 35 €/MWh, CO₂ 75 €/t)"),
    ]
    colors = {"nuc": BLUE, "gaz": ORANGE, "enr": AQUA}
    names = {"nuc": "Nucléaire", "gaz": "Gaz", "enr": "Renouvelables (prix des appels d'offres)"}
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    fig.subplots_adjust(left=0.27, right=0.985, top=0.83, bottom=0.13)
    n = len(rows)
    seen = set()
    for i, (lab, lo, hi, pt, fam, note) in enumerate(rows):
        y = n - 1 - i
        c = colors[fam]
        kw = {"label": names[fam]} if fam not in seen else {}
        seen.add(fam)
        if hi > lo:
            ax.plot([lo, hi], [y, y], color=c, linewidth=7, solid_capstyle="round", alpha=0.9, **kw)
        else:
            ax.plot([pt], [y], "o", color=c, markersize=10, markeredgecolor=SURFACE, markeredgewidth=1.5, **kw)
        ax.text(max(hi, pt) + 3, y, note, va="center", fontsize=9, color=INK2)
    ax.set_yticks(range(n), [r[0] for r in rows][::-1])
    ax.set_xlim(30, 200)
    ax.set_xlabel("€/MWh (euros de différentes années : voir étiquettes)")
    vgrid(ax)
    ax.legend(loc="upper right", fontsize=9)
    finish(fig, "07_couts_par_MWh.png",
           "Le coût d'un MWh varie beaucoup selon la technologie et les hypothèses",
           "À lire avec prudence : les prix des renouvelables excluent les coûts de réseau, de stockage et de "
           "secours ;\nle coût du nucléaire neuf dépend surtout du coût du capital (taux d'intérêt).",
           "Sources : CRE (coût du nucléaire existant 2025 ; appels d'offres PPE2 2025-2026 ; AO éolien en mer) ; "
           "Élysée, CPN du 17/03/2025 ; RTE FE2050 ch. 11 ; Cour des comptes (Flamanville 3, janv. 2025). "
           "Gaz : calcul indicatif.")


# ===========================================================================
# 8. Coûts système RTE 2060
# ===========================================================================
def couts_systeme():
    sc = ["M0", "M1", "M23", "N1", "N2", "N03"]
    cost = [77, 80, 71, 66, 61, 59]
    nuc = ["0 %", "13 %", "13 %", "26 %", "36 %", "50 %"]
    fam = [AQUA, AQUA, AQUA, BLUE, BLUE, BLUE]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.08, right=0.985, top=0.80, bottom=0.18)
    bars = ax.bar(sc, cost, color=fam, width=0.6)
    for r, v, nshare in zip(bars, cost, nuc):
        ax.text(r.get_x() + r.get_width() / 2, v + 1.2, f"≈ {v}", ha="center", fontsize=10, color=INK,
                fontweight="semibold")
        ax.text(r.get_x() + r.get_width() / 2, 4, f"nucléaire\n{nshare} en 2050", ha="center", fontsize=8.6,
                color=SURFACE, fontweight="semibold", linespacing=0.95)
    ax.axhline(45, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    ax.text(5.38, 45, "Système\nactuel ≈ 45", ha="left", va="center", fontsize=9, color=INK2)
    ax.set_xlim(-0.5, 6.05)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=AQUA, label="« M » : sans nouveau nucléaire (EnR 87–100 %)"),
                       Patch(color=BLUE, label="« N » : avec nouveaux réacteurs (EnR 50–74 %)")],
              loc="upper right")
    ax.set_ylim(0, 92)
    ax.set_ylabel("Coût complet annualisé du système électrique\nen 2060 (Md€₂₀₂₀ par an)")
    hgrid(ax)
    finish(fig, "08_couts_systeme_RTE.png",
           "Selon RTE, les scénarios avec nouveaux réacteurs coûtent moins cher en 2060",
           "Les scénarios avec nouveau nucléaire coûtent ≈ 10 à 20 Md€/an de moins, mais TOUS exigent un fort "
           "développement des renouvelables.",
           "Source : RTE, Futurs énergétiques 2050 (oct. 2021), coût du capital de 4 %. Valeurs ≈ lues sur le "
           "graphique (écart M23–N2 « de l'ordre de 10 Md€/an » selon RTE).\nAvec +3 points de coût du capital "
           "pour le nucléaire, les écarts s'effacent.")


# ===========================================================================
# 9. Prix de gros 2025 par zone de prix
# ===========================================================================
def zones_de_prix():
    rows = [("Finlande", 41.0), ("Norvège (NO1)", 58.4), ("France", 61.1), ("Espagne", 65.0),
            ("Belgique", 82.6), ("Pays-Bas", 86.8), ("Allemagne-Luxembourg", 89.3),
            ("Grande-Bretagne (≈)", 93.0), ("Autriche", 98.9), ("Suisse", 101.7), ("Italie (PUN)", 116.0)]
    rows = rows[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 6.0))
    fig.subplots_adjust(left=0.2, right=0.96, top=0.82, bottom=0.12)
    y = range(len(rows))
    cols = [BLUE if "France" in n else BASE for n, _ in rows]
    ax.barh(list(y), [v for _, v in rows], color=cols, height=0.62)
    for yy, (n, v) in zip(y, rows):
        ax.text(v + 1.2, yy, f"{v:.0f}", va="center", fontsize=9.5, color=INK2)
    ax.set_yticks(list(y), [n for n, _ in rows])
    ax.axvline(85, color=MUTED, linewidth=1, linestyle=(0, (2, 2)))
    ax.text(85.8, len(rows) - 0.6, "Moyenne UE ≈ 85", fontsize=9, color=INK2, va="center")
    ax.set_xlim(0, 130)
    ax.set_xlabel("Prix moyen day-ahead 2025 (€/MWh)")
    vgrid(ax)
    finish(fig, "09_prix_par_zone_2025.png",
           "En 2025, l'électricité de gros était moins chère en France que chez la plupart de ses voisins",
           "Prix moyen du lendemain (day-ahead) en 2025, en €/MWh. Le calcul est européen, mais chaque zone a son "
           "prix quand les lignes entre pays sont saturées.",
           "Sources : EPEX SPOT, résultats annuels 2025 ; Commission européenne (Italie, Finlande, moyenne UE) ; "
           "RTE (Espagne). GB : 80,6 £/MWh converti ≈ 1,16 €/£ (approximatif).")


# ===========================================================================
# 10. Soutien public aux renouvelables électriques (CRE)
# ===========================================================================
def soutien_enr():
    years = ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026\n(prév.)", "2027\n(prév.)"]
    vals = [5.17, 5.81, 2.95, -1.85, -3.99, 2.90, 6.18, 7.29, 8.38]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.80, bottom=0.16)
    cols = [RED if v < 0 else (AQUA if "prév" not in y else "#8fd6bc") for y, v in zip(years, vals)]
    bars = ax.bar(years, vals, color=cols, width=0.62)
    for r, v, yv in zip(bars, vals, years):
        lab = (f"{v:+.1f}" if v < 0 else f"{v:.1f}").replace(".", ",")
        if yv == "2020":
            lab = "≈ " + lab
        ax.text(r.get_x() + r.get_width() / 2, v + (0.2 if v >= 0 else -0.25), lab, ha="center",
                va="bottom" if v >= 0 else "top", fontsize=9.5, color=INK2)
    ax.axhline(0, color=BASE, linewidth=1)
    ax.set_ylim(-5.5, 9.8)
    ax.set_ylabel("Md€ par an (« charges constatées »)")
    ax.text(6.4, -2.6, "2022-2023 : prix de marché > prix garantis →\nles producteurs RENDENT de l'argent (5,5 Md€ de recettes selon la CRE)",
            ha="center", fontsize=9.5, color=RED, fontweight="semibold")
    ax.text(6.0, 9.2, "Prix de marché bas + « cannibalisation » →\nle complément versé remonte", ha="center",
            fontsize=9.5, color=INK2)
    hgrid(ax)
    finish(fig, "10_soutien_public_EnR.png",
           "Le soutien aux renouvelables coûte quand les prix de marché sont bas, et rapporte quand ils sont hauts",
           "L'État paie la différence quand le marché est sous le prix garanti, et encaisse quand il est "
           "au-dessus.",
           "Source : CRE, délibérations CSPE 2020-177, 2023-200, 2025-180, 2026-149 (électricité renouvelable, "
           "métropole continentale). 2020 recalculé (≈).")


# ===========================================================================
# 11. Composition du tarif réglementé (août 2026)
# ===========================================================================
def composition_trve():
    parts = [("Énergie + capacité\n(marchés lissés 24 mois)", 72.6, BLUE),
             ("Coûts commerciaux,\nCEE, marge", 20.7, VIOLET),
             ("Réseau (TURPE)", 74.6, AQUA),
             ("Accise + CTA", 35.6, YELLOW),
             ("TVA 20 %", 40.7, ORANGE)]
    total = sum(p[1] for p in parts)
    fig, ax = plt.subplots(figsize=(12.5, 4.4))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.84, bottom=0.1)
    left = 0
    for name, v, c in parts:
        ax.barh([0], [v], left=left, color=c, edgecolor=SURFACE, linewidth=2, height=0.55)
        ax.text(left + v / 2, 0.42, f"{name}", ha="center", va="bottom", fontsize=9.2, color=INK2,
                linespacing=0.95)
        ax.text(left + v / 2, 0, f"≈ {v:.0f} €\n{v / total * 100:.0f} %", ha="center", va="center",
                fontsize=9.5, color=SURFACE if c not in (YELLOW, AQUA) else INK, fontweight="semibold")
        left += v
    ax.set_xlim(0, total)
    ax.set_ylim(-0.32, 0.75)
    ax.axis("off")
    finish(fig, "11_composition_tarif_reglemente.png",
           "Le marché de gros pèse ≈ 30 % de la facture d'électricité",
           f"Tarif réglementé d'un ménage, ≈ {total:.0f} €/MWh toutes taxes comprises en août 2026. Seul le premier "
           "bloc dépend du marché de gros, et il est lissé sur deux ans.",
           "Reconstitution indicative à partir des délibérations CRE 2025-234, 2026-06 et 2026-147 "
           "(la CRE ne publie pas cette décomposition en €/MWh). Facture type 4,5 MWh/an : 1 072 € TTC.")


# ===========================================================================
# 14. Prix à la pompe : qui touche quoi ?
# ===========================================================================
def prix_pompe():
    rows = [("Gazole 2025", [0.39 + 0.13, 0.22, 0.61, 0.27]),
            ("SP95-E10 2025", [0.39 + 0.10, 0.25, 0.67, 0.28]),
            ("Gazole mi-sept. 2026\n(choc d'Ormuz, ≈)", [1.16, 0.22, 0.61, 0.40])]
    parts = [("Produit raffiné\n(brut + raffinage)", BLUE), ("Transport-distribution", AQUA),
             ("Accise", YELLOW), ("TVA", ORANGE)]
    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    fig.subplots_adjust(left=0.17, right=0.97, top=0.76, bottom=0.14)
    for i, (lab, vals) in enumerate(rows[::-1]):
        left = 0
        for (pname, col), v in zip(parts, vals):
            ax.barh(i, v, left=left, color=col, edgecolor=SURFACE, linewidth=2, height=0.6)
            ax.text(left + v / 2, i, f"{v:.2f}".replace(".", ","), ha="center", va="center", fontsize=9.5,
                    color=SURFACE if col in (BLUE,) else INK, fontweight="semibold")
            left += v
        tax_share = (vals[2] + vals[3]) / left * 100
        ax.text(left + 0.03, i, f"{left:.2f} €/l".replace(".", ",") + f"\ntaxes {tax_share:.0f} %",
                va="center", fontsize=9.5, color=INK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=n.replace("\n", " ")) for n, c in parts], loc="lower center",
              bbox_to_anchor=(0.5, 1.0), ncol=4, fontsize=9.5)
    ax.set_xlim(0, 2.75)
    ax.set_xlabel("€ par litre")
    vgrid(ax)
    finish(fig, "14_prix_pompe_decomposition.png",
           "En temps normal, les taxes font plus de la moitié du prix à la pompe",
           "En euros par litre. En 2026, la hausse vient du pétrole brut et des marges de raffinage.",
           "Sources : SDES (prix moyens 2025) ; CLCV (marges 2025) ; Bercy/DGCCRF (marges brutes 2026) ; "
           "accise 2026 (ministère). Mi-septembre 2026 : prix ≈ 2,39 €/l (source secondaire), cotation déduite.")


if __name__ == "__main__":
    prix_pompe()
    zones_de_prix()
    soutien_enr()
    composition_trve()
    merit_order()
    mix_electrique()
    fossiles()
    prix_menages()
    gaz_allemand()
    conso_exports()
    couts_mwh()
    couts_systeme()
    print("ok", sorted(p.name for p in OUT.glob("*.png")))
