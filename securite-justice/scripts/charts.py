"""Graphiques du chapitre « Sécurité et justice ».
Les données sont sourcées en commentaire, et dans le chapitre (securite_justice.md).
Usage, depuis la racine du dépôt : python3 securite-justice/scripts/charts.py
"""
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
    """Nombre au format français (virgule décimale, espace des milliers, signe moins typographique)."""
    s = f"{v:,.{d}f}".replace(",", " ").replace(".", ",").replace("-", "−")
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


def hbars(ax, rows, highlight, fmt, pad, others=BASE, special=None):
    """Barres horizontales ; rows = [(nom, valeur)], du haut vers le bas."""
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
# 1. Délinquance enregistrée depuis 2016, indices (graphique clé de « L'essentiel »)
# ===========================================================================
def delinquance_indices():
    # SSMSI, « Insécurité et délinquance en 2025 : bilan statistique et atlas départemental », 9 juillet 2026.
    # Niveaux 2025 publiés ; niveaux 2016-2024 recalculés à partir des évolutions annuelles du bilan
    # (figure 1, p. 7), sauf violences sexuelles 2016 (51 900, publié) et 2024 (Chiffres clés 2025).
    # Homicides : niveaux publiés (réponse à la question écrite n° 12954, JO du 5/12/2023, pour 2016-2022 ;
    # bilans 2024 et 2025) ; 2023 recalculé (≈ 996). Calculs dans edition/recherche/securite-justice/
    # situation_delinquance.md, section 10.
    yrs = list(range(2016, 2026))
    series = [
        ("Violences sexuelles", [100, 110, 130, 145, 148, 185, 204, 220, 236, 254], VIOLET, "254"),
        ("Violences physiques", [100, 104, 112, 120, 119, 133, 149, 158, 160, 168], RED, "168"),
        ("Homicides", [100, 91, 91, 94, 90, 97, 105, 109, 107, 107], INK2, "107"),
        ("Cambriolages de logement", [100, 102, 96, 96, 77, 77, 85, 88, 88, 85], AQUA, "85"),
        ("Vols de véhicules", [100, 94, 86, 85, 74, 74, 80, 84, 83, 75], GREEN, "75"),
        ("Vols violents sans arme", [100, 94, 87, 85, 69, 65, 63, 57, 51, 52], YELLOW, "52"),
    ]
    fig, ax = plt.subplots(figsize=(12.5, 5.4))
    fig.subplots_adjust(left=0.06, right=0.76, top=0.83, bottom=0.15)
    offsets = {"Cambriolages de logement": 4, "Vols de véhicules": -3, "Homicides": 3, "Vols violents sans arme": -3}
    for name, v, c, lab in series:
        ax.plot(yrs, v, color=c, linewidth=2.5)
        ax.text(2025.25, v[-1] + offsets.get(name, 0), f"{name} : {lab}", va="center", ha="left",
                fontsize=10, color=c if c != INK2 else INK, fontweight="semibold")
    ax.axhline(100, color=BASE, linewidth=1.0)
    ax.annotate("2020 : confinements", xy=(2020, 70), xytext=(2017.6, 40), fontsize=9, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax.set_xlim(2015.6, 2025.2)
    ax.set_ylim(0, 270)
    ax.set_xticks(yrs)
    ax.set_ylabel("Indice, 2016 = 100")
    ax.set_clip_on(False)
    hgrid(ax)
    finish(fig, "01_delinquance_indices.png",
           "Les violences enregistrées augmentent depuis 2016, les vols diminuent",
           "Victimes ou infractions enregistrées par la police et la gendarmerie, indice 100 en 2016. Une partie de "
           "la hausse des violences vient\nde la hausse des plaintes. Les homicides de 2016 comprennent les victimes "
           "de l'attentat de Nice.",
           "Source : SSMSI, bilan 2025 (juillet 2026) ; niveaux 2016-2024 recalculés à partir des évolutions "
           "publiées (calcul) ; homicides : niveaux publiés par le ministère de l'Intérieur, 2023 recalculé.")


# ===========================================================================
# 2. La part des victimes qui portent plainte
# ===========================================================================
def plaintes():
    # SSMSI, enquête « Vécu et ressenti en matière de sécurité » (VRS), édition 2024 (atteintes subies en 2023) ;
    # Chiffres clés 2025 (27 novembre 2025), p. 11-12 ; bilan 2025, PDF, p. 8.
    # Vols : vols réussis (hors tentatives). Cambriolage : résidence principale (57 %, Chiffres clés 2025, relu).
    rows = [("Vol de voiture (vol réussi)", 57), ("Cambriolage (vol réussi)", 57),
            ("Violences physiques", 21), ("Violences conjugales", 16), ("Menaces", 13),
            ("Harcèlement moral", 7), ("Violences sexuelles physiques", 6), ("Injures", 5),
            ("Violences sexuelles non physiques", 2)]
    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    fig.subplots_adjust(left=0.25, right=0.95, top=0.83, bottom=0.15)
    hbars(ax, rows, set(), lambda v: f"{v} %", 0.8, others=BLUE)
    ax.set_xlim(0, 65)
    ax.set_xlabel("% des victimes qui ont porté plainte")
    finish(fig, "02_plaintes.png",
           "La plupart des victimes de violences ne portent pas plainte",
           "Part des victimes qui déclarent avoir porté plainte, atteintes subies en 2023, personnes de 18 ans ou plus",
           "Source : SSMSI, enquête Vécu et ressenti en matière de sécurité, édition 2024 (Chiffres clés 2025 ; "
           "bilan 2025).")


# ===========================================================================
# 3. Les homicides en Europe
# ===========================================================================
def homicides_europe():
    # Eurostat, crim_off_cat, ICCS0101 (homicide volontaire), unité P_HTHAB, mise à jour du 29 avril 2026.
    # UE à 27 : calcul pondéré (3 953 homicides / ≈ 450 millions d'habitants), Eurostat ne le publie pas.
    rows = [("Lituanie", 2.63), ("Lettonie", 2.40), ("Estonie", 1.82), ("Finlande", 1.78), ("Belgique", 1.40),
            ("France", 1.28), ("UE à 27 (calcul)", 0.88), ("Suède", 0.87), ("Allemagne", 0.83),
            ("Espagne", 0.72), ("Pologne", 0.69), ("Pays-Bas", 0.67), ("Italie", 0.57)]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    fig.subplots_adjust(left=0.17, right=0.95, top=0.85, bottom=0.15)
    hbars(ax, rows, {"France"}, lambda v: fr(v, 2), 0.03, special={"UE à 27 (calcul)": ORANGE})
    ax.set_xlim(0, 3.0)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: fr(x, 1)))
    ax.set_xlabel("Homicides volontaires pour 100 000 habitants")
    finish(fig, "03_homicides_europe.png",
           "Le taux d'homicide de la France est au-dessus de la moyenne de l'UE",
           "Homicides volontaires enregistrés par la police pour 100 000 habitants, 2024 ; la France est 6e sur 27",
           "Source : Eurostat, série crim_off_cat (avril 2026). Moyenne de l'UE calculée à partir des nombres et des "
           "taux des 27 pays (calcul).")


# ===========================================================================
# 4. Les saisies de cocaïne
# ===========================================================================
def cocaine_saisies():
    # 2021 : OFDT, « Cocaïne et crack : synthèse des connaissances » (page non datée).
    # 2022-2024 : OFDT, Salhi, L'offre de stupéfiants en France en 2024 (février 2026), tableau 3
    #   (données OCRTIS/OFAST).
    # 2025 : annonce du ministre de l'Intérieur, dépêche AFP reprise par Outremers 360 (18 mars 2026),
    #   source secondaire.
    yrs = ["2021", "2022", "2023", "2024", "2025"]
    v = [26.5, 27.73, 23.25, 53.47, 84.3]
    labels = ["26,5", "27,7", "23,3", "53,5", "84,3"]
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    fig.subplots_adjust(left=0.07, right=0.95, top=0.82, bottom=0.17)
    cols = [BLUE] * 4 + [BLUE]
    bars = ax.bar(range(len(yrs)), v, color=cols, width=0.6)
    bars[-1].set_hatch("//")
    bars[-1].set_facecolor(SURFACE)
    bars[-1].set_edgecolor(BLUE)
    for i, (val, lab) in enumerate(zip(v, labels)):
        ax.text(i, val + 1.5, f"{lab} t", ha="center", fontsize=10.5, color=INK, fontweight="semibold")
    ax.set_xticks(range(len(yrs)), ["2021", "2022", "2023", "2024", "2025\n(annonce du ministre)"])
    ax.set_ylim(0, 95)
    ax.set_ylabel("Tonnes")
    hgrid(ax)
    finish(fig, "04_cocaine_saisies.png",
           "Les saisies de cocaïne ont plus que triplé entre 2023 et 2025",
           "Cocaïne saisie en France par la police, la gendarmerie et la douane, en tonnes. Les saisies dépendent "
           "aussi de l'activité des services.",
           "Sources : OFDT (2021-2024, données OFAST) ; 2025 : chiffre du ministre de l'Intérieur, dépêche AFP "
           "(source secondaire).")


# ===========================================================================
# 5. Le budget de la justice et la loi de programmation
# ===========================================================================
def justice_budget():
    # Mission Justice, crédits de paiement hors CAS Pensions, en millions d'euros.
    # Loi de programmation 2023-2027 (loi n° 2023-1059 du 20 novembre 2023, art. 1er) et crédits votés ou
    # demandés : Assemblée nationale, rapport n° 1996, annexe 29 (J.-D. Berger, 23 octobre 2025).
    # 2027 : « près de 11 milliards » (JSS, 1er octobre 2026) ; plafond de 11 Md€ (Unité Magistrats,
    # 21 juillet 2026). Périmètre (hors pensions) à vérifier dans le projet de loi de finances pour 2027.
    yrs = ["2023", "2024", "2025", "2026", "2027"]
    prog = [9579, 10081, 10681, 10691, 10748]
    reel = [9571, 10082, 10242, 10629, 11000]
    x = range(len(yrs))
    w = 0.38
    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.82, bottom=0.2)
    ax.bar([i - w / 2 for i in x], prog, width=w, color=BASE, label="Loi de programmation")
    b = ax.bar([i + w / 2 for i in x], reel, width=w, color=BLUE, label="Loi de finances ou projet")
    b[-1].set_hatch("//")
    b[-1].set_facecolor(SURFACE)
    b[-1].set_edgecolor(BLUE)
    for i in x:
        ax.text(i - w / 2, prog[i] + 120, fr(prog[i] / 1000, 2), ha="center", fontsize=9.5, color=INK2)
        lab = "≈ 11,0" if i == 4 else fr(reel[i] / 1000, 2)
        ax.text(i + w / 2, reel[i] + 120, lab, ha="center", fontsize=9.5, color=INK, fontweight="semibold")
    ax.set_xticks(list(x), ["2023\n(loi de finances)", "2024\n(loi de finances)", "2025\n(loi de finances)",
                            "2026\n(projet)", "2027\n(projet, annoncé)"])
    ax.set_ylim(0, 12500)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: fr(y / 1000, 0)))
    ax.set_ylabel("Milliards d'euros")
    ax.legend(loc="upper left", ncol=2, fontsize=10)
    hgrid(ax)
    finish(fig, "05_justice_budget.png",
           "En 2025, le budget de la justice est resté sous la loi de programmation",
           "Mission Justice, crédits de paiement hors pensions, en milliards d'euros",
           "Sources : loi de programmation 2023-2027 ; Assemblée nationale, rapport n° 1996 (octobre 2025) ; "
           "2027 : annonces du projet de loi de finances (JSS, octobre 2026, source secondaire).")


# ===========================================================================
# 6. Les détenus et les places de prison
# ===========================================================================
def prisons():
    # Ministère de la Justice, « Séries statistiques des personnes placées sous main de justice » (mars 2026) :
    # détenus et places opérationnelles au 1er janvier. 2000-2004 : personnes écrouées (y compris non détenues).
    # Point du 1er septembre 2026 : mesure mensuelle de l'incarcération (publiée le 3 octobre 2026).
    # Baisse de 2021 : −12 959 détenus du 16 mars au 11 mai 2020 (Sénat, réponse à la question écrite n° 15081).
    yrs = list(range(2000, 2027))
    det = [51441, 47837, 48594, 55407, 59246, 58231, 58344, 58402, 61076, 62252, 60978, 60544, 64787, 66572,
           67075, 66270, 66678, 68432, 68974, 70059, 70739, 62673, 69448, 72173, 75897, 80669, 86140]
    pla = [49294, 48593, 48021, 47987, 48605, 50094, 51252, 50588, 50693, 51997, 54988, 56358, 57236, 56992,
           57516, 57841, 58561, 58681, 59765, 60151, 61037, 60583, 60749, 60670, 61767, 62385, 63411]
    assert len(yrs) == len(det) == len(pla)
    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    fig.subplots_adjust(left=0.08, right=0.84, top=0.83, bottom=0.14)
    ax.plot(yrs, det, color=BLUE, linewidth=2.6)
    ax.plot(yrs, pla, color=INK2, linewidth=2.2)
    ax.fill_between(yrs, pla, det, where=[d > p for d, p in zip(det, pla)], color=BLUE, alpha=0.10, linewidth=0)
    ax.scatter([2026.67], [90020], s=56, color=BLUE, edgecolor=SURFACE, linewidth=1.2, zorder=4)
    ax.scatter([2026.67], [63348], s=56, color=INK2, edgecolor=SURFACE, linewidth=1.2, zorder=4)
    ax.text(2027.1, 90020, "90 020 détenus\n(1er septembre 2026)", va="center", ha="left", fontsize=10,
            color=BLUE, fontweight="semibold")
    ax.text(2027.1, 63348, "63 348 places", va="center", ha="left", fontsize=10, color=INK2,
            fontweight="semibold")
    ax.annotate("2021 : baisse après\nle confinement de 2020", xy=(2021, 62673), xytext=(2014.2, 78000), fontsize=9,
                color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
    ax.set_xlim(1999.5, 2027)
    ax.set_ylim(0, 100000)
    ax.set_xticks(list(range(2000, 2027, 2)))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: fr(y, 0)))
    ax.set_clip_on(False)
    hgrid(ax)
    finish(fig, "06_prisons.png",
           "Le nombre de détenus augmente plus vite que le nombre de places",
           "Personnes détenues et places de prison au 1er janvier (2000-2004 : personnes écrouées) ; points : "
           "1er septembre 2026",
           "Sources : ministère de la Justice, séries statistiques (mars 2026) et mesure mensuelle de "
           "l'incarcération au 1er septembre 2026.")


if __name__ == "__main__":
    delinquance_indices()
    plaintes()
    homicides_europe()
    cocaine_saisies()
    justice_budget()
    prisons()
    print("6 graphiques écrits dans", OUT)
