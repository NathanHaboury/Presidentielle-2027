"""Met à jour les lignes « En débat » de « Le livre en bref » (edition/livre/livre_en_bref.qmd).

Chaque fiche de la page contient un bloc délimité :
    <!-- en-debat: chemin/du/chapitre.md -->
    **En débat.** Question 1 ? Question 2 ? …
    <!-- /en-debat -->
Le script remplace le contenu du bloc par les questions de la section 2 du chapitre
(« Ce qui fait débat »), sans le préfixe « Question N. ». Les lignes « À savoir »
s'écrivent à la main et ne sont pas touchées.

Usage, depuis la racine du dépôt :
    python3 edition/scripts/livre_en_bref.py           # met la page à jour
    python3 edition/scripts/livre_en_bref.py --check   # dit si la page est à jour

À relancer après toute modification des questions de la section 2 d'un chapitre.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE = os.path.join(ROOT, "edition", "livre", "livre_en_bref.qmd")
BLOC = re.compile(r"(<!-- en-debat: (\S+) -->\n)(.*?)(<!-- /en-debat -->)", re.S)


def questions(chemin):
    texte = open(os.path.join(ROOT, chemin), encoding="utf-8").read()
    m = re.search(r"^## 2\.[^\n]*\n(.*?)(?=^## )", texte, flags=re.M | re.S)
    if not m:
        sys.exit(f"Section 2 introuvable dans {chemin}")
    qs = re.findall(r"^### (?:Question \d+\.\s*)?(.+?)\s*$", m.group(1), flags=re.M)
    if not qs:
        sys.exit(f"Aucune question en section 2 dans {chemin}")
    return qs


# Sigles des questions, développés à leur première apparition dans la page (charte, section 3)
DEVELOPPER = [
    ("Le RSA ", "Le revenu de solidarité active (RSA) "),
    ("la loi SRU", "la loi relative à la solidarité et au renouvellement urbains (SRU)"),
    ("L'OTAN", "L'Alliance atlantique (OTAN)"),
]


def mettre_a_jour(texte):
    vus = set()

    def remplace(m):
        ligne = " ".join(questions(m.group(2)))
        for court, long in DEVELOPPER:
            if court in ligne and court not in vus:
                ligne = ligne.replace(court, long, 1)
                vus.add(court)
        return f"{m.group(1)}\n**En débat.** {ligne}\n\n{m.group(4)}"

    nouveau, n = BLOC.subn(remplace, texte)
    if n == 0:
        sys.exit("Aucun bloc « en-debat » trouvé dans la page.")
    return nouveau


if __name__ == "__main__":
    actuel = open(PAGE, encoding="utf-8").read()
    nouveau = mettre_a_jour(actuel)
    if "--check" in sys.argv:
        if nouveau == actuel:
            print("À jour.")
        else:
            print("À mettre à jour : python3 edition/scripts/livre_en_bref.py")
            sys.exit(1)
    else:
        open(PAGE, "w", encoding="utf-8").write(nouveau)
        print(f"Mis à jour : {os.path.relpath(PAGE, ROOT)}")
