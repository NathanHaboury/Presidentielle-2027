"""Graphiques du chapitre « Immigration ».

Les données sont dans ce script, avec leur source en commentaire. Elles sont détaillées et
annotées dans le chapitre (immigration.md). Régénérer : python3 scripts/charts.py
"""
import numpy as np
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
BLUE, ORANGE, YELLOW, VIOLET = "#2a78d6", "#eb6834", "#eda100", "#4a3aa7"
LIGHTBLUE = "#9dbfe8"

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
    return f"{x:.{d}f}".replace(".", ",").replace("-", "−")


# ===========================================================================
# 1. Part des immigrés et des étrangers dans la population, 1975-2025 (graphique clé)
# Source : INSEE, « L'essentiel sur les immigrés et les étrangers », 25 juin 2026 (figures
# « Évolution de la population immigrée / étrangère en France ») ; INSEE, série 2381757, 4 juin 2026.
# Champ : France métropolitaine jusqu'en 1982 ; hors Mayotte de 1990 à 2013 ; avec Mayotte depuis 2014.
# 2024 et 2025 provisoires. Rupture de série en 2024 (note méthodologique INSEE du 4 juin 2026 :
# +242 000 immigrés et +165 000 étrangers dus au nouveau protocole de collecte).
# ===========================================================================
def population():
    yi = [1975, 1982, 1990, 1999, 2006, 2011, 2014, 2016, 2018, 2020, 2021, 2022, 2023, 2024, 2025]
    vi = [7.4, 7.4, 7.3, 7.3, 8.1, 8.6, 9.1, 9.4, 9.8, 10.2, 10.2, 10.3, 10.7, 11.3, 11.6]
    ve = [6.5, 6.8, 6.3, 5.5, 5.8, 6.0, 6.5, 6.8, 7.2, 7.6, 7.7, 7.8, 8.2, 8.8, 9.1]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.07, right=0.83, top=0.8, bottom=0.12)
    for vals, col in [(vi, BLUE), (ve, ORANGE)]:
        ax.plot(yi[:-2], vals[:-2], color=col, linewidth=2.4, marker="o", markersize=5, markeredgecolor=SURFACE)
        ax.plot(yi[-3:], vals[-3:], color=col, linewidth=2.4, linestyle=(0, (3, 2)), marker="o", markersize=5,
                markeredgecolor=SURFACE)
    ax.text(2026.0, 11.75, "Immigrés : 11,6 %\n(8,0 millions)", va="center", fontsize=10, color=BLUE,
            fontweight="semibold")
    ax.text(2026.0, 8.95, "Étrangers : 9,1 %\n(6,3 millions)", va="center", fontsize=10, color=ORANGE,
            fontweight="semibold")
    ax.annotate("2024 : changement de collecte du\nrecensement (≈ +0,35 point d'immigrés)",
                xy=(2024, 11.3), xytext=(2008.5, 12.3), fontsize=8.8, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax.text(1987, 7.75, "≈ 7,4 % de 1975 à 1999", ha="center", fontsize=9, color=BLUE)
    ax.set_xlim(1972, 2026.5)
    ax.set_ylim(0, 13.5)
    ax.set_ylabel("% de la population")
    hgrid(ax)
    finish(fig, "01_population_immigree.png",
           "La part des immigrés passe de 7,4 % en 1975 à 11,6 % en 2025",
           "Immigré : né étranger à l'étranger (on le reste après une naturalisation). Étranger : sans la nationalité "
           "française, né en France ou non.",
           "Source : INSEE, « L'essentiel sur les immigrés et les étrangers », juin 2026. 2024-2025 provisoires ; série en "
           "rupture en 2024 (pointillés). Points publiés : 1975, 1982, 1990, 1999, puis annuels\ndepuis 2006 (certaines "
           "années non reprises ici). France métropolitaine jusqu'en 1982, avec Mayotte depuis 2014. Les descendants "
           "d'immigrés ne sont pas comptés.")


# ===========================================================================
# 2. Premiers titres de séjour par motif, 2015-2025
# Source : ministère de l'Intérieur, DGEF, « Les titres de séjour en 2024 » (26 juin 2025, tableau 1.1)
# pour 2015-2020 ; « Les titres de séjour en 2025 » (Essentiels de l'immigration n° 144, 30 juin 2026,
# figure 3) pour 2021-2025. 2025 provisoire. Ressortissants de pays tiers (hors UE, EEE et Suisse).
# ===========================================================================
def titres():
    years = list(range(2015, 2026))
    d = {
        "Familial": [99320, 94380, 94285, 97770, 98463, 80740, 93581, 97038, 92719, 91030, 90959],
        "Étudiants": [70262, 73882, 80587, 84011, 90760, 73406, 90101, 103917, 110688, 110914, 116835],
        "Économique": [20496, 22878, 27522, 34529, 43008, 27337, 38031, 55247, 58762, 58603, 50848],
        "Humanitaire": [23444, 30369, 37102, 35710, 38862, 33802, 41968, 41458, 48068, 56115, 88001],
        "Divers": [15354, 17057, 17670, 26597, 38871, 21814, 119045, 32432, 29782, 28925, 30819],
    }
    cols = {"Familial": LIGHTBLUE, "Étudiants": BLUE, "Économique": YELLOW, "Humanitaire": ORANGE, "Divers": BASE}
    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    fig.subplots_adjust(left=0.07, right=0.84, top=0.8, bottom=0.12)
    bottom = np.zeros(len(years))
    for k, v in d.items():
        v = np.array(v) / 1000
        ax.bar(years, v, bottom=bottom, color=cols[k], width=0.72, label=k, edgecolor=SURFACE, linewidth=0.6)
        bottom += v
    for x, t in zip(years, bottom):
        ax.text(x, t + 5, f"{t:.0f}", ha="center", fontsize=9, color=INK)
    ax.annotate("dont ≈ 96 000 titres\nliés au Brexit", xy=(2021, 372), xytext=(2016.0, 385), fontsize=8.8,
                color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax.annotate("humanitaire :\n56 000 → 88 000", xy=(2025, 335), xytext=(2022.3, 418), fontsize=8.8,
                color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) if y < 2025 else "2025*" for y in years])
    ax.set_ylim(0, 450)
    ax.set_ylabel("Milliers de premiers titres de séjour")
    h, l = ax.get_legend_handles_labels()
    ax.legend(h[::-1], l[::-1], loc="center left", bbox_to_anchor=(1.01, 0.5))
    hgrid(ax)
    finish(fig, "02_titres_de_sejour.png",
           "En 2025, la hausse des premiers titres de séjour vient des titres humanitaires",
           "Premiers titres délivrés à des ressortissants de pays hors UE, par motif. « Humanitaire » : réfugiés, "
           "protection subsidiaire, étrangers malades.",
           "Source : ministère de l'Intérieur, DGEF (26 juin 2025 et 30 juin 2026). * 2025 provisoire : les chiffres "
           "provisoires sous-estiment en général les définitifs, surtout pour l'humanitaire.")


# ===========================================================================
# 3. Comparaison européenne : personnes nées à l'étranger et premières demandes d'asile
# Sources : Eurostat, migr_pop3ctb (nés à l'étranger, 1er janvier 2025, mise à jour du 25 septembre 2026) ;
# migr_asyappctza (premiers demandeurs, mise à jour du 3 septembre 2026) ; tps00001 (population au
# 1er janvier, mise à jour du 30 septembre 2026). Parts et taux pour 100 000 habitants : calculs du chapitre.
# Grèce 2024 par habitant non calculé.
# ===========================================================================
def europe():
    fb = [("Suisse", 31.7), ("Autriche", 22.5), ("Suède", 20.8), ("Allemagne", 20.5), ("Belgique", 20.2),
          ("Espagne", 19.3), ("Pays-Bas", 16.8), ("UE-27", 14.4), ("Danemark", 14.4), ("France", 14.0),
          ("Italie", 11.8)][::-1]
    asy = [("Grèce", 534, None), ("Espagne", 287, 340), ("Belgique", 232, 277), ("Italie", 218, 256),
           ("France", 169, 189), ("UE-27", 149, 203), ("Autriche", 136, 243), ("Allemagne", 135, 275),
           ("Pays-Bas", 134, 178), ("Suède", 48, 64), ("Danemark", 31, 37)][::-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6.0))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.8, bottom=0.18, wspace=0.38)

    def col(n):
        return BLUE if n == "France" else (INK2 if n == "UE-27" else BASE)

    ax1.barh(range(len(fb)), [v for _, v in fb], color=[col(n) for n, _ in fb], height=0.64)
    for i, (_, v) in enumerate(fb):
        ax1.text(v + 0.4, i, fr(v), va="center", fontsize=9, color=INK)
    ax1.set_yticks(range(len(fb)), [n for n, _ in fb])
    ax1.set_xlim(0, 36)
    ax1.set_xlabel("% de la population, 1er janvier 2025")
    ax1.set_title("A. Personnes nées à l'étranger", pad=8, fontsize=11.5)
    vgrid(ax1)
    ax2.barh(range(len(asy)), [v for _, v, _ in asy], color=[col(n) for n, _, _ in asy], height=0.64, label="2025")
    pts = [(i, w) for i, (_, _, w) in enumerate(asy) if w is not None]
    ax2.scatter([w for _, w in pts], [i for i, _ in pts], marker="|", s=160, color=INK, linewidth=2, zorder=3,
                label="2024")
    for i, (_, v, w) in enumerate(asy):
        ax2.text(max(v, w or 0) + 8, i, f"{v}", va="center", fontsize=9, color=INK)
    ax2.set_yticks(range(len(asy)), [n for n, _, _ in asy])
    ax2.set_xlim(0, 600)
    ax2.set_xlabel("Premières demandes d'asile pour 100 000 habitants")
    ax2.set_title("B. Premières demandes d'asile, 2025 (trait : 2024)", pad=8, fontsize=11.5)
    ax2.legend(loc="lower right", fontsize=9)
    vgrid(ax2)
    for ax in (ax1, ax2):
        for tl in ax.get_yticklabels():
            if tl.get_text() == "France":
                tl.set_fontweight("bold")
    finish(fig, "03_comparaison_europeenne.png",
           "La France est dans la moyenne de l'UE pour la population née à l'étranger, un peu au-dessus pour l'asile",
           "De 2024 à 2025, les premières demandes d'asile baissent de 10 % en France, de 26 % dans l'UE et de 51 % "
           "en Allemagne.",
           "Source : Eurostat (migr_pop3ctb, migr_asyappctza, tps00001), mises à jour de juillet à septembre 2026 ; "
           "parts et taux par habitant calculés pour ce chapitre. Les personnes nées à l'étranger\ncomprennent les "
           "nationaux nés à l'étranger (1,7 million de Français en France).")


# ===========================================================================
# 4. Estimations du solde budgétaire de l'immigration en France, en % du PIB
# Sources : OCDE, Perspectives des migrations internationales 2021, ch. 4, tableaux 4.1 et 4.2 (moyenne
# 2006-2018 ; A : dépenses individuelles ; B : + biens publics « congestibles » ; C : + défense et intérêts
# de la dette, par tête) ; CEPII, Lettre n° 394 (déc. 2018), 1979-2011 ; CAE, Focus n° 072 (nov. 2021) ;
# OID, « Le coût de l'immigration pour les finances publiques – Partie I » (modifié le 2 déc. 2024) :
# 1,4 à 40 Md€, deux scénarios du CEPII (2006 ; descendants compris, 1,64 point de PIB en 2011) ;
# Contribuables associés, étude n° 45 (août 2023), 53,9 Md€, connue par la Fondation Jean-Jaurès :
# ≈ 1,9 % du PIB de 2023 (calcul du chapitre).
# ===========================================================================
def budget():
    rows = [  # libellé, min, max, note
        ("OCDE 2021, méthode A : dépenses individuelles", 1.02, 1.02, "personnes nées à l'étranger, 2006-2018"),
        ("OCDE, méthode B : + police, routes… (« congestibles »)", 0.25, 0.25, ""),
        ("OCDE, méthode C : + défense et dette, par tête", -0.85, -0.85, "natifs, même méthode : −3,25 %"),
        ("OCDE, méthode C, enfants compris", -1.41, -1.41, "enfants de 15 ans ou moins vivant avec un parent immigré"),
        ("CEPII 2018, 1979-2011", -0.5, 0.05, "« plutôt été négative […] mais faible »"),
        ("CAE 2021, synthèse des études", -0.5, 0.5, "« généralement comprise entre ± 0,5 % du PIB »"),
        ("OID (2020, modifié en 2024) : 1,4 à 40 Md€", -1.64, -0.08, "deux scénarios du CEPII, descendants compris pour le second"),
        ("Contribuables associés 2023 : 53,9 Md€", -1.9, -1.9, "périmètre le plus large (descendants, irréguliers)"),
    ][::-1]
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    fig.subplots_adjust(left=0.36, right=0.97, top=0.8, bottom=0.17)
    for i, (lab, lo, hi, note) in enumerate(rows):
        ax.axhline(i, color=GRID, linewidth=0.8, zorder=0)
        if hi > lo:
            ax.plot([lo, hi], [i, i], color=BLUE, linewidth=7, solid_capstyle="round", alpha=0.85)
        else:
            ax.scatter([lo], [i], s=90, color=BLUE, zorder=3)
        def sg(v):
            return ("+" if v > 0 else "") + fr(v, 2)
        txt = sg(lo) if hi == lo else f"{sg(lo)} à {sg(hi)}"
        x0 = max(lo, hi, 0) + 0.1  # libellés à droite du trait du zéro
        ax.text(x0, i + 0.18, txt, fontsize=9.3, color=INK, va="bottom")
        if note:
            ax.text(x0, i - 0.12, note, fontsize=8.4, color=INK2, va="top")
    ax.axvline(0, color=INK2, linewidth=1)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=9.4)
    ax.set_xlim(-2.3, 2.6)
    ax.set_ylim(-0.6, len(rows) - 0.3)
    ax.set_xlabel("Solde pour les finances publiques, % du PIB (négatif : les dépenses imputées dépassent les recettes)")
    finish(fig, "04_cout_estimations.png",
           "Selon la méthode, le solde budgétaire de l'immigration va de +1,0 % à −1,9 % du PIB",
           "Le résultat dépend du périmètre (immigrés seuls ou avec leurs enfants) et de la part des dépenses communes "
           "(défense, dette) qu'on leur impute.",
           "Sources : OCDE (2021, tableaux 4.1 et 4.2) ; CEPII (Lettre n° 394, 2018) ; CAE (Focus n° 072, 2021) ; "
           "OID (association favorable à une baisse de l'immigration) ; Contribuables associés (association\nqui milite "
           "pour la baisse des impôts et des dépenses publiques), via la Fondation Jean-Jaurès. Montants en Md€ convertis "
           "en % du PIB pour ce chapitre.")


# ===========================================================================
# 5. Part des étrangers : population, mis en cause selon l'infraction, chaîne pénale
# Sources : A. SSMSI, « Insécurité et délinquance en 2025 », figure 8 (9 juillet 2026), mis en cause pour
# 15 indicateurs ; étrangers résidents = 9 % de la population (Insee, estimations 2025).
# B. Vers 2019 : INSEE, « Auteurs selon la nationalité » (2021) : population 7 %, mis en cause 17,7 % ;
# INSEE, France, portrait social 2025, fiche « Justice » : condamnés 15 % (2019), 17 % (2023, provisoire) ;
# ministère de la Justice, séries statistiques 1980-2026 (tableaux 18-19) : détenus 23,1 % (1er janvier 2019),
# 24,7 % (1er janvier 2026). Population 2025 : 9 % (SSMSI).
# ===========================================================================
def delinquance():
    off = [("Vols dans les véhicules", 37), ("Cambriolages de logement", 36), ("Vols violents sans arme", 33),
           ("Vols sans violence contre des personnes", 29), ("Trafic de stupéfiants", 22),
           ("Tentatives d'homicide", 20), ("Homicides", 18), ("Vols avec armes", 18), ("Violences physiques", 16),
           ("Vols d'accessoires sur véhicules", 16), ("Violences sexuelles", 13), ("Escroqueries", 13),
           ("Destructions et dégradations", 12), ("Usage de stupéfiants", 12), ("Vols de véhicules", 9)][::-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6.6), gridspec_kw={"width_ratios": [1.45, 1]})
    fig.subplots_adjust(left=0.22, right=0.97, top=0.8, bottom=0.14, wspace=0.32)
    ax1.barh(range(len(off)), [v for _, v in off], color=BLUE, height=0.64)
    for i, (_, v) in enumerate(off):
        ax1.text(v + 0.6, i, f"{v} %", va="center", fontsize=9, color=INK)
    ax1.axvline(9, color=INK, linewidth=1.2, linestyle=(0, (3, 2)),
                label="Part des étrangers dans\nla population : 9 %")
    ax1.legend(loc="lower right", fontsize=9)
    ax1.set_yticks(range(len(off)), [n for n, _ in off], fontsize=9.4)
    ax1.set_xlim(0, 44)
    ax1.set_xlabel("% d'étrangers parmi les mis en cause, 2025")
    ax1.set_title("A. Selon l'infraction (police et gendarmerie)", pad=8, fontsize=11.5)
    vgrid(ax1)
    st = ["Population", "Mis en\ncause", "Condamnés", "Détenus"]
    old = [7.0, 17.7, 15.0, 23.1]
    new = [9.0, None, 17.0, 24.7]
    x = np.arange(len(st))
    ax2.bar(x - 0.19, old, width=0.36, color=LIGHTBLUE, label="Vers 2019")
    ax2.bar([xi + 0.19 for xi, v in zip(x, new) if v], [v for v in new if v], width=0.36, color=BLUE,
            label="Dernière donnée (2023-2026)")
    for xi, v in zip(x, old):
        ax2.text(xi - 0.19, v + 0.5, fr(v), ha="center", fontsize=9, color=INK)
    for xi, v in zip(x, new):
        if v:
            ax2.text(xi + 0.19, v + 0.5, fr(v), ha="center", fontsize=9, color=INK, fontweight="semibold")
        else:
            ax2.text(xi + 0.19, 1.0, "non\npublié", ha="center", fontsize=8, color=MUTED)
    ax2.set_xticks(x, st, fontsize=9.4)
    ax2.set_ylim(0, 28)
    ax2.set_ylabel("% d'étrangers")
    ax2.set_title("B. Population et étapes pénales", pad=8, fontsize=11.5)
    ax2.legend(loc="upper left", fontsize=8.8)
    hgrid(ax2)
    finish(fig, "05_delinquance_etrangers.png",
           "Étrangers : 9 % de la population, 9 à 37 % des mis en cause selon l'infraction, 24,7 % des détenus",
           "Un mis en cause est soupçonné, pas condamné. Les naturalisés et les descendants d'immigrés sont comptés "
           "comme Français.",
           "Sources : A. SSMSI, « Insécurité et délinquance en 2025 » (juillet 2026), hors infractions au séjour. "
           "B. INSEE (2021 ; 2025) ; ministère de la Justice (détenus au 1er janvier 2019 et 2026).\nMis en cause 2019 : "
           "toutes infractions hors routières, séjour compris ; aucune part « toutes infractions » n'est publiée pour 2025. Condamnés : "
           "2019 et 2023 (provisoire).")


# ===========================================================================
# 6. Retours rapportés aux ordres de quitter le territoire (Eurostat)
# Sources : Eurostat, migr_eiord (ordres de quitter le territoire) et migr_eirtn (retours, toutes
# destinations), API lue le 11 octobre 2026 ; migr_eiord mis à jour le 30 septembre 2026, migr_eirtn le
# 25 septembre 2026. Ratios : calculs du chapitre. Rupture de série des retours en 2021 (Eurostat).
# ===========================================================================
def retours():
    pays = [("Suède", 76.3), ("Autriche", 72.1), ("Allemagne", 65.3), ("Danemark", 42.8), ("Suisse", 33.2),
            ("UE-27", 32.1), ("Italie", 22.4), ("Belgique", 20.7), ("Pays-Bas", 15.9), ("France", 13.8),
            ("Espagne", 10.6)][::-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.8), gridspec_kw={"width_ratios": [1.25, 1]})
    fig.subplots_adjust(left=0.1, right=0.97, top=0.8, bottom=0.18, wspace=0.3)
    cols = [BLUE if n == "France" else (INK2 if n == "UE-27" else BASE) for n, _ in pays]
    ax1.barh(range(len(pays)), [v for _, v in pays], color=cols, height=0.64)
    for i, (_, v) in enumerate(pays):
        ax1.text(v + 0.8, i, f"{fr(v)} %", va="center", fontsize=9, color=INK)
    ax1.set_yticks(range(len(pays)), [n for n, _ in pays])
    for tl in ax1.get_yticklabels():
        if tl.get_text() == "France":
            tl.set_fontweight("bold")
    ax1.set_xlim(0, 88)
    ax1.set_xlabel("Retours / ordres de quitter le territoire, 2025 (%)")
    ax1.set_title("A. En Europe, 2025", pad=8, fontsize=11.5)
    vgrid(ax1)
    yrs = list(range(2015, 2026))
    # France : retours / ordres, toutes destinations (18 245 / 79 950 en 2015 … 18 930 / 137 550 en 2025)
    v = [22.8, 17.4, 18.5, 17.0, 14.3, 7.8, 6.5, 7.5, 8.9, 12.9, 13.8]
    ax2.bar(yrs, v, color=BLUE, width=0.72)
    for xx, val in zip(yrs, v):
        ax2.text(xx, val + 0.5, fr(val), ha="center", fontsize=8.2, color=INK)
    ax2.set_xticks(yrs, [str(y) for y in yrs], fontsize=8.2, rotation=45)
    ax2.set_ylim(0, 27)
    ax2.set_ylabel("%")
    ax2.set_title("B. France, de 2015 à 2025", pad=8, fontsize=11.5)
    hgrid(ax2)
    finish(fig, "06_retours_europe.png",
           "Retours rapportés aux ordres de quitter le territoire : 14 % en France, 32 % dans l'UE en 2025",
           "Indicateur approximatif : les retours d'une année ne correspondent pas aux ordres de la même année, et la "
           "France prononce un ordre pour chaque séjour irrégulier constaté.",
           "Source : Eurostat (migr_eiord, migr_eirtn), mises à jour d'août et de septembre 2026 ; ratios calculés pour "
           "ce chapitre. Retours vers toutes destinations, départs aidés compris ; rupture de série en 2021.\nVers les seuls "
           "pays hors UE, le ratio de la France est de 10,9 % en 2025.")


if __name__ == "__main__":
    population()
    titres()
    europe()
    budget()
    delinquance()
    retours()
    print("ok", sorted(p.name for p in OUT.glob("*.png")))
