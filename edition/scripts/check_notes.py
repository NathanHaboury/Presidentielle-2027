"""Contrôle des notes de source d'un chapitre (charte v2).
Usage, depuis la racine du dépôt :
    python3 edition/scripts/check_notes.py */*.md      # tous les chapitres et fiches
    python3 edition/scripts/check_notes.py sante/sante_assurance_maladie.md
- chaque appel [^x] a une définition dans le fichier ; chaque définition est appelée ;
- une étiquette déjà définie dans un AUTRE fichier du dépôt doit avoir exactement la même définition
  (les définitions de tous les fichiers du dépôt sont relues à chaque lancement) ;
- signale les appels [^ch-partis] restants et les doublons de définition.
"""
import re, sys, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
alld = {}
for f in glob.glob(ROOT + "/*/*.md"):
    if "/edition/" in f:
        continue
    for m in re.finditer(r"^\[\^([^\]]+)\]:\s?(.*)$", open(f, encoding="utf-8").read(), flags=re.M):
        alld.setdefault(m.group(1), {})[os.path.relpath(f, ROOT)] = m.group(2).strip()
ok = True
for f in sys.argv[1:]:
    rel = os.path.relpath(os.path.abspath(f), ROOT)
    t = open(f, encoding="utf-8").read()
    defs = {}
    for m in re.finditer(r"^\[\^([^\]]+)\]:\s?(.*)$", t, flags=re.M):
        if m.group(1) in defs:
            print(f"{rel} : DÉFINITION EN DOUBLE {m.group(1)}"); ok = False
        defs[m.group(1)] = m.group(2).strip()
    body = re.sub(r"^\[\^[^\]]+\]:.*$", "", t, flags=re.M)
    calls = set(re.findall(r"\[\^([^\]]+)\]", body))
    for k in sorted(calls - set(defs)):
        print(f"{rel} : APPEL SANS DÉFINITION {k}"); ok = False
    for k in sorted(set(defs) - calls):
        print(f"{rel} : DÉFINITION INUTILISÉE {k}"); ok = False
    for k, v in defs.items():
        for g, w in alld.get(k, {}).items():
            if g != rel and w != v:
                print(f"{rel} : ÉTIQUETTE {k} DÉFINIE AUTREMENT DANS {g}"); ok = False
                break
    n = len(re.findall(r"\[\^ch-partis\]", body))
    if n:
        print(f"{rel} : {n} appel(s) [^ch-partis] restant(s)")
print("OK" if ok else "À CORRIGER")
