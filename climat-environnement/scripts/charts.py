"""Graphiques du chapitre « Climat et environnement ».

Les données sont dans ce script, avec leur source en commentaire. Elles sont
détaillées dans le chapitre (climat-environnement/climat_environnement.md) et
dans les notes de recherche, non publiées.
Lancer : python3 climat-environnement/scripts/charts.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# --- Police & encre (même style que les autres chapitres) -------------------
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


def fr(x, d=1):
    """Nombre à la française : virgule décimale, espace fine pour les milliers."""
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s


# ===========================================================================
# Données
# ===========================================================================
# Citepa, rapport Secten 2026 (16 juin 2026), tableau « Secteurs / Mt CO2e »,
# France hexagonale + outre-mer de l'UE, tous gaz à effet de serre, hors puits
# (« brut ») et puits UTCATF. 2025 : estimation provisoire.
# https://www.citepa.org/donnees-air-climat/donnees-gaz-a-effet-de-serre/secten/
YEARS = list(range(1990, 2026))
GROSS = [546.9, 572.5, 561.5, 540.0, 531.7, 538.1, 556.4, 548.6, 562.5, 557.2,
         551.9, 557.0, 550.6, 554.7, 554.3, 555.6, 544.9, 535.2, 530.3, 509.2,
         513.1, 488.0, 490.7, 490.2, 457.4, 460.8, 463.7, 466.1, 446.5, 437.7,
         398.0, 422.4, 405.8, 378.2, 367.0, 359.4]
SINK = [-39.3, -41.1, -41.0, -43.8, -41.6, -44.5, -50.1, -51.4, -53.6, -57.2,
        -44.1, -54.6, -61.9, -65.9, -68.6, -68.6, -69.0, -68.3, -67.1, -57.8,
        -60.3, -60.6, -63.3, -67.2, -59.7, -56.6, -50.8, -45.8, -59.8, -54.9,
        -58.3, -50.9, -48.8, -50.2, -52.0, -51.3]
assert len(YEARS) == len(GROSS) == len(SINK)

# Plafonds indicatifs annuels de la SNBC-3, décret n° 2026-636 du 16 juillet 2026
# (texte reproduit par l'Ineris : https://aida.ineris.fr/node/46163), Mt CO2e, hors puits.
SNBC3 = {2025: 359, 2026: 348, 2027: 328, 2028: 308, 2029: 292, 2030: 276}

# Secteurs, 1990 et 2025 (Citepa, Secten 2026), Mt CO2e.
SECTORS = [  # (nom, 1990, 2025)
    ("Transports", 125.4, 122.9),
    ("Agriculture", 92.9, 76.6),
    ("Industrie manufacturière", 140.1, 58.4),
    ("Bâtiments (chauffage…)", 92.9, 54.9),
    ("Production d'énergie", 78.9, 31.4),
    ("Déchets", 16.7, 15.3),
]

# Émissions par habitant, hors puits, t CO2e (Eurostat, jeu sdg_13_10,
# « total hors UTCATF et items pour mémoire », mis à jour le 22 avril 2026).
PER_CAPITA = [  # (pays, 1990, 2024)
    ("Pologne", 12.5, 9.3),
    ("Allemagne", 15.8, 7.8),
    ("Italie", 9.2, 6.2),
    ("Espagne", 7.3, 5.5),
    ("France", 9.4, 5.3),
]

# Consommation d'espaces naturels, agricoles et forestiers (ENAF), ha par an
# (Cerema, synthèse 2026, fichiers fonciers ; 2024 provisoire).
ENAF = {2011: 29470, 2012: 27619, 2013: 25173, 2014: 22632, 2015: 20511, 2016: 20977,
        2017: 21172, 2018: 20877, 2019: 18754, 2020: 19549, 2021: 20130, 2022: 19336,
        2023: 18073, 2024: 15119}


# ===========================================================================
# 1. Émissions 1990-2025 et trajectoire 2030 (graphique clé)
# ===========================================================================
def emissions_trajectory():
    fig, ax = plt.subplots(figsize=(12, 5.8))
    fig.subplots_adjust(left=0.07, right=0.975, top=0.80, bottom=0.13)
    ax.plot(YEARS, GROSS, color=BLUE, linewidth=2.6, label="Émissions observées")
    ax.scatter([2025], [GROSS[-1]], color=BLUE, s=28, zorder=5)
    xs, ys = list(SNBC3.keys()), list(SNBC3.values())
    ax.plot(xs, ys, color=ORANGE, linewidth=2.2, linestyle=(0, (4, 2)),
            label="Plafonds de la stratégie nationale bas-carbone (SNBC-3)")
    ax.axhline(546.9 * 0.6, color=MUTED, linewidth=1, linestyle=":")
    ax.text(1990.3, 546.9 * 0.6 + 5, "Objectif de la loi pour 2030 : −40 % par rapport à 1990 (328 Mt)",
            fontsize=8.8, color=INK2)
    ax.text(1990.3, 276 - 16, "Objectif de la SNBC-3 pour 2030 : 276 Mt, ≈ −50 % par rapport à 1990",
            fontsize=8.8, color=ORANGE)
    ax.axhline(276, color=ORANGE, linewidth=0.8, linestyle=":")
    ax.annotate("1990 : 547 Mt", (1990, 546.9), xytext=(1991.2, 585), fontsize=9, color=INK2,
                arrowprops=dict(arrowstyle="-", color=BASE))
    ax.annotate("2025 : 359 Mt\n(provisoire)", (2025, 359.4), xytext=(2017.6, 300), fontsize=9, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BASE))
    ax.text(2009.2, 410, "2019-2025 :\n−3,2 % par an\nen moyenne", fontsize=9, color=BLUE, ha="center")
    ax.text(2030.2, 300, "2025-2030 :\n−5,1 %\npar an", fontsize=9, color=ORANGE, ha="left")
    ax.set_xlim(1989, 2033.5)
    ax.set_ylim(0, 620)
    ax.set_ylabel("Millions de tonnes d'équivalent CO₂ (Mt CO₂e)")
    hgrid(ax)
    ax.legend(loc="lower left", fontsize=9.5)
    finish(fig, "01_emissions_trajectoire.png",
           "Pour tenir l'objectif 2030, la baisse des émissions doit passer d'≈ 3 % à ≈ 5 % par an",
           "Émissions de gaz à effet de serre de la France, hors puits de carbone (Mt CO₂e). 2025 : estimation provisoire.",
           "Sources : Citepa, rapport Secten 2026 ; décret n° 2026-636 du 16 juillet 2026 (SNBC-3). Rythmes annuels : calcul.")


# ===========================================================================
# 2. Émissions par secteur, 1990 et 2025
# ===========================================================================
def sectors():
    fig, ax = plt.subplots(figsize=(12, 5.4))
    fig.subplots_adjust(left=0.20, right=0.97, top=0.80, bottom=0.12)
    names = [s[0] for s in SECTORS][::-1]
    v90 = [s[1] for s in SECTORS][::-1]
    v25 = [s[2] for s in SECTORS][::-1]
    y = range(len(names))
    ax.barh([i + 0.2 for i in y], v90, height=0.38, color=BASE, label="1990")
    ax.barh([i - 0.2 for i in y], v25, height=0.38, color=BLUE, label="2025 (provisoire)")
    for i, (a, b) in enumerate(zip(v90, v25)):
        ax.text(a + 1.5, i + 0.2, fr(a), va="center", fontsize=8.6, color=MUTED)
        ax.text(b + 1.5, i - 0.2, (f"{fr(b)}  ({(b / a - 1) * 100:+.1f} %)").replace(".", ",").replace("-", "−"),
                va="center", fontsize=8.8, color=BLUE)
    ax.set_yticks(list(y))
    ax.set_yticklabels(names)
    ax.set_xlabel("Mt CO₂e")
    ax.set_xlim(0, 165)
    vgrid(ax)
    ax.legend(loc="lower right", fontsize=9.5)
    finish(fig, "02_emissions_secteurs.png",
           "Les transports émettent presque autant qu'en 1990 ; l'industrie et l'énergie ont baissé d'≈ 60 %",
           "Émissions de gaz à effet de serre par secteur (Mt CO₂e), en 1990 et en 2025. Entre parenthèses : variation depuis 1990.",
           "Source : Citepa, rapport Secten 2026 (secteurs du Citepa). 2025 : estimation provisoire. Variations : calcul.")


# ===========================================================================
# 3. Le puits de carbone (forêts et sols)
# ===========================================================================
def carbon_sink():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    fig.subplots_adjust(left=0.08, right=0.975, top=0.79, bottom=0.13)
    absorb = [-v for v in SINK]
    ax.bar(YEARS, absorb, color=GREEN, width=0.75)
    ax.hlines(64, 2005 - 0.4, 2014 + 0.4, color=INK, linewidth=1.6)
    ax.hlines(53, 2015 - 0.4, 2024 + 0.4, color=INK, linewidth=1.6)
    ax.text(2009.5, 73, "Moyenne 2005-2014 :\n64 Mt par an", ha="center", fontsize=9, color=INK)
    ax.text(2019.5, 62, "Moyenne 2015-2024 :\n53 Mt par an (−17 %)", ha="center", fontsize=9, color=INK)
    ax.set_xlim(1989, 2026)
    ax.set_ylim(0, 85)
    ax.set_ylabel("CO₂ absorbé, en Mt CO₂e par an")
    hgrid(ax)
    finish(fig, "03_puits_carbone.png",
           "Les forêts et les sols absorbent moins de CO₂ qu'il y a dix ans",
           "Absorption nette des forêts, des sols et des autres terres, en Mt CO₂e par an. Méthode de l'édition 2026 de l'inventaire.",
           "Sources : Citepa, rapport Secten 2026 ; moyennes : Haut Conseil pour le climat, rapport 2026. Les éditions plus anciennes donnaient des niveaux plus bas (voir le texte).")


# ===========================================================================
# 4. Émissions par habitant en Europe
# ===========================================================================
def per_capita():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    fig.subplots_adjust(left=0.13, right=0.97, top=0.78, bottom=0.17)
    names = [p[0] for p in PER_CAPITA]
    y = range(len(names))
    for i, (name, a, b) in enumerate(PER_CAPITA):
        col = BLUE if name == "France" else INK2
        ax.plot([a, b], [i, i], color=GRID, linewidth=3, zorder=1)
        ax.scatter([a], [i], color=BASE, s=60, zorder=2)
        ax.scatter([b], [i], color=BLUE if name == "France" else VIOLET, s=70, zorder=3)
        ax.text(a + 0.25, i + 0.22, fr(a), fontsize=8.8, color=MUTED)
        ax.text(b - 0.25, i + 0.22, fr(b), fontsize=9.2, color=col, ha="right",
                fontweight="bold" if name == "France" else None)
    ax.set_yticks(list(y))
    ax.set_yticklabels(names)
    for lab in ax.get_yticklabels():
        if lab.get_text() == "France":
            lab.set_color(BLUE)
            lab.set_fontweight("bold")
    ax.set_xlim(0, 17)
    ax.set_xlabel("Tonnes d'équivalent CO₂ par habitant (hors puits)")
    vgrid(ax)
    ax.scatter([], [], color=BASE, s=60, label="1990")
    ax.scatter([], [], color=VIOLET, s=70, label="2024")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.13), ncol=2, fontsize=9.5)
    finish(fig, "04_emissions_par_habitant_europe.png",
           "La France émet le moins par habitant des cinq pays comparés ; l'Allemagne a le plus baissé",
           "Émissions de gaz à effet de serre par habitant, hors puits de carbone, en 1990 et en 2024 (t CO₂e).",
           "Source : Eurostat, jeu de données sdg_13_10 (avril 2026). Les émissions importées (empreinte carbone) ne sont pas comptées.")


# ===========================================================================
# 5. Consommation d'espaces et trajectoire ZAN
# ===========================================================================
def enaf():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    fig.subplots_adjust(left=0.08, right=0.975, top=0.79, bottom=0.13)
    yrs = list(ENAF.keys())
    vals = list(ENAF.values())
    cols = [BASE if y < 2021 else BLUE for y in yrs]
    ax.bar(yrs, vals, color=cols, width=0.72)
    ref = sum(ENAF[y] for y in range(2011, 2021)) / 10      # 22 673 ha (calcul)
    target = ref / 2                                         # 11 337 ha (calcul)
    ax.hlines(ref, 2010.6, 2020.4, color=INK2, linewidth=1.2, linestyle="--")
    ax.text(2015.5, ref + 900, f"Moyenne 2011-2020 : {fr(ref, 0)} ha", ha="center", fontsize=9, color=INK2)
    ax.hlines(target, 2020.6, 2030.4, color=ORANGE, linewidth=1.8)
    ax.text(2027.6, target + 900, f"Rythme moyen visé\n2021-2031 : {fr(target, 0)} ha", ha="center",
            fontsize=9, color=ORANGE)
    ax.text(2027.6, 4200, "2021-2024 : 64 % de l'enveloppe\n2021-2031 déjà consommée", ha="center",
            fontsize=9, color=BLUE)
    ax.text(2024, ENAF[2024] + 500, fr(ENAF[2024], 0), ha="center", fontsize=8.8, color=BLUE)
    ax.text(2011, ENAF[2011] + 500, fr(ENAF[2011], 0), ha="center", fontsize=8.8, color=INK2)
    ax.set_xlim(2010.3, 2030.7)
    ax.set_xticks(list(range(2011, 2031, 2)))
    ax.set_ylim(0, 33000)
    ax.set_ylabel("Hectares consommés par an")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fr(v, 0)))
    hgrid(ax)
    finish(fig, "05_consommation_espaces_zan.png",
           "La consommation d'espaces a diminué de moitié depuis 2011, mais reste au-dessus du rythme visé",
           "Espaces naturels, agricoles et forestiers transformés en terrains bâtis, routes ou parkings (hectares par an).",
           "Source : Cerema, fichiers fonciers (synthèse 2026) ; 2024 provisoire. Moyennes et part de l'enveloppe : calcul (loi Climat et résilience de 2021).")


# ===========================================================================
# 6. France, Suède, Danemark : émissions par habitant 1990-2024
# ===========================================================================
# Source : Eurostat, sdg_13_10, src_crf=TOTX4_MEMO (hors terres et forêts, hors
# transports internationaux), t CO2e par habitant, mis à jour le 22 avril 2026.
# Relevé dans les notes de recherche sur la Suède et le Danemark (non publiées), tableau (a).
NORDIC_YEARS = list(range(1990, 2025))
NORDIC = {
    "France": [9.4, 9.8, 9.6, 9.2, 9.0, 9.1, 9.3, 9.2, 9.4, 9.2, 9.1, 9.1, 8.9, 8.9, 8.9, 8.8, 8.6, 8.4,
               8.3, 7.9, 7.9, 7.5, 7.5, 7.5, 6.9, 6.9, 7.0, 7.0, 6.7, 6.5, 5.9, 6.2, 5.9, 5.5, 5.3],
    "Suède": [8.3, 8.3, 8.2, 8.2, 8.4, 8.3, 8.7, 8.2, 8.2, 7.8, 7.7, 7.7, 7.8, 7.8, 7.7, 7.3, 7.3, 7.1,
              6.8, 6.3, 6.8, 6.3, 6.0, 5.8, 5.5, 5.4, 5.4, 5.2, 5.1, 4.9, 4.4, 4.6, 4.3, 4.2, 4.5],
    "Danemark": [14.0, 16.1, 14.9, 15.3, 16.0, 15.3, 17.7, 15.8, 15.0, 14.5, 13.6, 13.9, 13.7, 14.6, 13.5,
                 12.6, 14.0, 13.1, 12.3, 11.8, 11.8, 10.8, 9.9, 10.2, 9.4, 8.9, 9.1, 8.7, 8.6, 7.9, 7.4,
                 7.6, 7.2, 6.6, 6.2],
}


def nordic():
    fig, ax = plt.subplots(figsize=(12, 5.4))
    fig.subplots_adjust(left=0.07, right=0.83, top=0.79, bottom=0.13)
    colors = {"France": BLUE, "Suède": ORANGE, "Danemark": VIOLET}
    for name, vals in NORDIC.items():
        assert len(vals) == len(NORDIC_YEARS), name
        ax.plot(NORDIC_YEARS, vals, color=colors[name], linewidth=2.6 if name == "France" else 2.0)
        ax.scatter([1990, 2024], [vals[0], vals[-1]], color=colors[name], s=26, zorder=3)
        change = (vals[-1] / vals[0] - 1) * 100
        label_y = {"Danemark": 6.9, "France": 5.3, "Suède": 3.7}[name]
        ax.text(2024.8, label_y, f"{name} : {fr(vals[-1])} t ({change:+.0f} %)".replace("-", "−"),
                va="center", fontsize=9.6, color=colors[name], fontweight="bold" if name == "France" else None)
        ax.text(1989.4, vals[0], fr(vals[0]), va="center", ha="right", fontsize=8.8, color=colors[name])
    ax.set_xlim(1988, 2024.5)
    ax.set_ylim(0, 19)
    ax.set_yticks(list(range(0, 19, 3)))
    ax.set_xticks(list(range(1990, 2025, 5)))
    ax.set_ylabel("t CO₂e par habitant")
    hgrid(ax)
    finish(fig, "06_suede_danemark_france.png",
           "Par habitant, la Suède émet moins que la France et le Danemark plus ; le Danemark a le plus baissé",
           "Émissions de gaz à effet de serre sur le territoire, hors forêts et sols, en tonnes d'équivalent CO₂ par habitant, 1990-2024.",
           "Source : Eurostat, jeu de données sdg_13_10 (avril 2026). Variations 1990-2024 par habitant : calcul. Les émissions importées (empreinte carbone) ne sont pas comptées.")


if __name__ == "__main__":
    emissions_trajectory()
    sectors()
    carbon_sink()
    per_capita()
    enaf()
    nordic()
    print("ok")
