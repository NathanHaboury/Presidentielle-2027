"""Graphiques de la Partie V « Ce que proposent les partis ».

Les données sont dans data/sondages_2026.csv (une ligne par candidat et par hypothèse, avec la source).
Elles sont présentées et sourcées dans l'introduction (programmes_partis_2027.md).
Régénérer : python3 scripts/charts.py
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
import csv
import re
import statistics
from collections import defaultdict

DATA = Path(__file__).resolve().parent.parent / "data" / "sondages_2026.csv"
# Sondages publiés du 12 juillet au 12 octobre 2026 : 16 notices de la Commission des sondages et le rapport
# de Toluna Harris Interactive du 12 octobre 2026 (recherche : edition/recherche/partis/paysage.md).


def lire():
    rows = list(csv.DictReader(open(DATA, encoding="utf-8")))
    hyp = defaultdict(dict)
    for x in rows:
        s = x["score"].replace(",", ".").replace("<", "").strip()
        if not re.match(r"^\d", s):
            continue
        cle = (x["institut"], x["commanditaire"], x["terrain_debut"], x["hypothese"])
        hyp[cle][x["candidat"]] = float(s)
    return hyp


def premier_tour():
    hyp = {k: v for k, v in lire().items() if k[3].startswith("1er")}
    lignes = [  # libellé, candidat, filtre sur l'hypothèse
        ("Jean-Luc Mélenchon (LFI)", "Mélenchon", None),
        ("Marine Tondelier (Les Écologistes)", "Tondelier", None),
        ("Raphaël Glucksmann (PS-Place publique)", "Glucksmann", None),
        ("Gabriel Attal (Renaissance), avec É. Philippe", "Attal", lambda h: "Philippe" in h),
        ("Gabriel Attal, sans É. Philippe", "Attal", lambda h: "Philippe" not in h),
        ("Édouard Philippe (Horizons), avec G. Attal", "Philippe", lambda h: "Attal" in h),
        ("Édouard Philippe, sans G. Attal", "Philippe", lambda h: "Attal" not in h),
        ("Bruno Retailleau (LR)", "Retailleau", None),
        ("Marine Le Pen (RN)", "Le Pen", None),
        ("Éric Zemmour (Reconquête)", "Zemmour", None),
    ]
    stats = []
    for lab, c, filt in lignes:
        v = [h[c] for h in hyp.values() if c in h and (filt is None or filt(h))]
        stats.append((lab, min(v), max(v), statistics.median(v), len(v)))
    stats = stats[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 5.9))
    fig.subplots_adjust(left=0.33, right=0.97, top=0.82, bottom=0.15)
    for i, (lab, lo, hi, med, n) in enumerate(stats):
        ax.axhline(i, color=GRID, linewidth=0.8, zorder=0)
        ax.plot([lo, hi], [i, i], color=LIGHTBLUE, linewidth=8, solid_capstyle="round", zorder=2)
        ax.scatter([med], [i], s=55, color=BLUE, zorder=3)
        ax.text(hi + 0.7, i, f"{fr(lo)} à {fr(hi)}  (médiane {fr(med)} ; {n} hypothèses)", va="center",
                fontsize=8.8, color=INK2)
    ax.set_yticks(range(len(stats)), [s[0] for s in stats], fontsize=9.6)
    ax.set_xlim(0, 60)
    ax.set_xticks(range(0, 51, 10))
    ax.set_ylim(-0.6, len(stats) - 0.4)
    ax.set_xlabel("Intentions de vote au premier tour (%), selon l'hypothèse testée")
    vgrid(ax)
    finish(fig, "01_intentions_premier_tour.png",
           "Marine Le Pen est en tête dans les 79 hypothèses de premier tour testées en trois mois",
           "Plus bas et plus haut score de chaque candidat, et médiane (point), dans 17 sondages publiés du 12 juillet "
           "au 12 octobre 2026,\ntous réalisés avant la désignation de Raphaël Glucksmann le 11 octobre.",
           "Sources : notices de la Commission des sondages ; Toluna Harris Interactive (rapport du 12 octobre 2026). "
           "Calculs pour ce livre à partir de 79 hypothèses ; marge d'erreur de ± 1,4 à ± 3,1 points\npour 1 000 "
           "personnes selon les instituts. Données : partis/data/sondages_2026.csv.")


def second_tour():
    hyp = {k: v for k, v in lire().items() if k[3].startswith("2nd") and "Le Pen" in v}
    adv = [("Jean-Luc Mélenchon", "Mélenchon"), ("Raphaël Glucksmann", "Glucksmann"), ("François Hollande", "Hollande"),
           ("Gabriel Attal", "Attal"), ("Édouard Philippe", "Philippe"), ("Bruno Retailleau", "Retailleau")]
    stats = []
    for lab, c in adv:
        v = [h["Le Pen"] for h in hyp.values() if c in h]
        stats.append((lab, min(v), max(v), len(v)))
    stats = stats[::-1]
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    fig.subplots_adjust(left=0.2, right=0.97, top=0.84, bottom=0.17)
    for i, (lab, lo, hi, n) in enumerate(stats):
        ax.barh(i, hi - lo, left=lo, height=0.5, color=BLUE)
        ax.text(hi + 0.4, i, f"{fr(lo)} à {fr(hi)} %  ({n} duel{'s' if n > 1 else ''})", va="center", fontsize=9,
                color=INK2)
    ax.axvline(50, color=INK2, linewidth=1)
    ax.text(50.2, len(stats) - 0.45, "50 %", fontsize=8.5, color=INK2, va="bottom")
    ax.set_yticks(range(len(stats)), [f"face à {s[0]}" for s in stats], fontsize=9.6)
    ax.set_xlim(45, 75)
    ax.set_ylim(-0.6, len(stats) - 0.2)
    ax.set_xlabel("Score de Marine Le Pen au second tour (%), selon l'adversaire testé")
    vgrid(ax)
    finish(fig, "02_duels_second_tour.png",
           "Marine Le Pen l'emporte dans chacun des 35 duels de second tour où elle a été testée",
           "Plus bas et plus haut score de Marine Le Pen selon l'adversaire, dans 17 sondages publiés du 12 juillet au "
           "12 octobre 2026.",
           "Sources : notices de la Commission des sondages ; Toluna Harris Interactive (rapport du 12 octobre 2026). "
           "Calculs pour ce livre. L'axe commence à 45 % pour lire l'écart à 50 %.\nDonnées : partis/data/sondages_2026.csv.")


if __name__ == "__main__":
    premier_tour()
    second_tour()
    print("ok", sorted(p.name for p in OUT.glob("*.png")))
