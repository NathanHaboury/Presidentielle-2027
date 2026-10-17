"""Prépare le dépôt public du livre à partir de ce dépôt de travail.

Le dépôt public (github.com/NathanHaboury/Presidentielle-2027) contient le livre et ses
outils, sans l'historique de travail ni les dossiers internes : notes de recherche,
audit, pilote, chiffres de référence, Comparaisons internationales.

Usage, depuis la racine de ce dépôt :
    python3 edition/scripts/publier.py ../Presidentielle-2027            # copie les fichiers
    python3 edition/scripts/publier.py ../Presidentielle-2027 --render   # puis construit le site dans docs/

Le script :
- copie les fichiers de la liste INCLURE et retire du dossier cible ceux qui n'y sont plus
  (le dossier .git et docs/ ne sont jamais touchés par la copie) ;
- remplace l'adresse du dépôt de travail par celle du dépôt public ;
- fait construire le livre dans docs/ (dossier publié par GitHub Pages) ;
- écrit le README et le .gitignore publics (modèles dans edition/publication/).
Il ne lance aucune commande Git : la publication (add, commit, push) reste manuelle.
"""
import datetime
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ANCIEN = "github.com/NathanHaboury/Presidentielle-2027"
NOUVEAU = "github.com/NathanHaboury/Presidentielle-2027"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]

INCLURE = [
    "LICENSE.md", "index.qmd", "_quarto.yml", ".github",
    "edition/charte.md", "edition/glossaire.md", "edition/livre", "edition/scripts",
    "institutions", "finances-publiques", "pouvoir-achat", "retraites-productivite",
    "travail-emploi", "logement", "education", "sante", "securite-justice",
    "energie", "climat-environnement", "immigration", "defense-europe", "partis",
]
IGNORER = re.compile(r"(^|/)(__pycache__|\.DS_Store|_print\.html)(/|$)")
TEXTE = (".md", ".qmd", ".yml", ".lua", ".py", ".typ", ".css")
GARDER = {".git", "docs", "README.md", ".gitignore"}  # jamais retirés du dossier cible


def fichiers_source():
    res = []
    for item in INCLURE:
        chemin = os.path.join(ROOT, item)
        if os.path.isfile(chemin):
            res.append(item)
            continue
        for d, _, fs in os.walk(chemin):
            for f in fs:
                rel = os.path.relpath(os.path.join(d, f), ROOT)
                if not IGNORER.search(rel):
                    res.append(rel)
    return sorted(res)


def copier(rel, cible):
    src, dst = os.path.join(ROOT, rel), os.path.join(cible, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if rel.endswith(TEXTE):
        t = open(src, encoding="utf-8").read().replace(ANCIEN, NOUVEAU)
        if rel == "_quarto.yml":
            t = t.replace("output-dir: _book", "output-dir: docs")
        if not os.path.exists(dst) or open(dst, encoding="utf-8").read() != t:
            open(dst, "w", encoding="utf-8").write(t)
    else:
        shutil.copy2(src, dst)


def retirer_obsoletes(cible, gardes):
    for d, dirs, fs in os.walk(cible, topdown=True):
        rel_d = os.path.relpath(d, cible)
        if rel_d == ".":
            dirs[:] = [x for x in dirs if x not in GARDER]
        for f in fs:
            rel = os.path.normpath(os.path.join(rel_d, f))
            if rel not in gardes and rel not in GARDER:
                os.remove(os.path.join(d, f))
                print("retiré :", rel)


def tableau_chapitres():
    """Reprend le tableau des chapitres du README de travail, sans les colonnes de suivi."""
    s = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    i = s.index("| Partie | Chapitre |")
    lignes = s[i:s.index("\n\n", i)].split("\n")[2:]
    out = ["| Partie | Chapitre | Texte | PDF |", "|---|---|---|---|"]
    for l in lignes:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if c[0] == "Ouverture" or "Comparaisons" in c[1]:
            continue
        out.append(f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} |")
    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cible = os.path.abspath(sys.argv[1])
    if cible == ROOT or cible.startswith(ROOT + os.sep):
        sys.exit("Le dossier cible doit être hors du dépôt de travail.")
    os.makedirs(cible, exist_ok=True)
    src = fichiers_source()
    for rel in src:
        copier(rel, cible)
    retirer_obsoletes(cible, set(src))

    today = datetime.date.today()
    jour = "1er" if today.day == 1 else str(today.day)
    version = f"{jour} {MOIS[today.month - 1]} {today.year}"
    modele = open(os.path.join(ROOT, "edition/publication/README.md"), encoding="utf-8").read()
    readme = modele.replace("{{VERSION}}", version).replace("{{TABLEAU}}", tableau_chapitres())
    open(os.path.join(cible, "README.md"), "w", encoding="utf-8").write(readme)
    shutil.copy2(os.path.join(ROOT, "edition/publication/gitignore"), os.path.join(cible, ".gitignore"))
    print(f"{len(src)} fichiers copiés dans {cible}")

    if "--render" in sys.argv:
        subprocess.run(["quarto", "render"], cwd=cible, check=True)
        open(os.path.join(cible, "docs", ".nojekyll"), "w").close()
        print("Site construit dans docs/")


if __name__ == "__main__":
    main()
