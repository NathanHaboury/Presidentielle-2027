"""Audit automatique des dossiers au regard de la charte éditoriale (edition/charte.md).

Usage, depuis la racine du dépôt :
    python3 edition/scripts/audit.py            # tous les dossiers
    python3 edition/scripts/audit.py energie    # un seul dossier

Produit edition/audit/indicateurs.md (tableau de bord) et edition/audit/indicateurs.json.
Partie V : l'introduction (partis/programmes_partis_2027.md) suit le gabarit des chapitres ; les huit fiches
(partis/<parti>.md) suivent le gabarit des fiches (charte, section 7) et sont contrôlées à part.
Les résultats sont des indices, pas des verdicts : un « sigle non développé » est à vérifier à la main.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "edition" / "audit"

# Sigles expliqués une fois dans le mode d'emploi du livre (charte, section 3)
SIGLES_COMMUNS = {"UE", "PIB", "TVA", "SMIC"}
SIGLES_PARTIS = {"LFI", "PS", "LR", "RN", "PCF", "UDR", "EELV", "LO", "NPA", "DLF", "UPR", "NFP", "RPR", "UMP", "UDF", "GRS"}
ROMAINS = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI",
           "XVII", "XVIII", "XIX", "XX", "XXI"}
# Noms de médias et d'instituts de sondage : des marques, pas des sigles à développer (charte, section 3)
MARQUES = {"TF1", "BFMTV", "M6", "RTL", "LCI", "BVA"}
UNITES = {"GW", "MW", "TW", "GWh", "MWh", "TWh", "CO2", "CO", "NOx", "PDF", "A4", "OK", "USD", "EUR", "CHF", "GBP"}

PARTIS = {  # charte, section 6 (liste proposée), dans l'ordre de l'hémicycle
    "LFI": r"\bLFI\b|France insoumise|Mélenchon",
    "Écologistes": r"Écologistes|\bEELV\b|Tondelier",
    "PS-Place publique": r"\bPS\b|Parti socialiste|Place publique|Glucksmann",
    "Renaissance": r"Renaissance|\bAttal\b|Ensemble pour la République",
    "Horizons": r"Horizons|Édouard Philippe",
    "LR": r"\bLR\b|Les Républicains|Retailleau",
    "RN": r"\bRN\b|Rassemblement national|Le Pen|Bardella",
    "Reconquête": r"Reconquête|Zemmour",
}
CAMPS = {
    "gauche": r"\bLFI\b|insoumis|\bPS\b|socialiste|Place publique|Écologistes|écologiste|\bPCF\b|gauche|NFP",
    "centre": r"Renaissance|Horizons|MoDem|Ensemble|gouvernement|Macron|centre|majorité présidentielle",
    "droite": r"\bLR\b|Républicains|\bRN\b|Rassemblement national|Reconquête|droite|Zemmour|Le Pen",
}
VERDICTS = ["Vrai", "Plutôt vrai", "À nuancer", "Plutôt faux", "Faux", "Non démontré"]

# Partie V : l'introduction remplace « Ce qui fait débat » par « Qui propose quoi » et « Évaluations » par
# « Ce que deviennent les promesses » (charte, section 7)
GABARIT_INTRO_PARTIS = {"debat": r"qui propose quoi", "evaluations": r"promesses"}
INTRO_PARTIS = "programmes_partis_2027"
GABARIT_FICHE = [  # (libellé, motif sur les titres de niveau 2), dans l'ordre
    ("En bref", r"^en bref"),
    ("1. Qui", r"^1\. qui"),
    ("2. Sa vision", r"^2\. sa vision"),
    ("3. Ses propositions", r"^3\. ses propositions"),
    ("4. Comment il gouvernerait", r"^4\. comment"),
    ("5. Ce que coûte le programme", r"^5\. ce que coûte"),
    ("6. Critiques et réponses", r"^6\. critiques"),
    ("7. Expérience du pouvoir", r"^7\. expérience"),
    ("8. Ce qui reste à préciser", r"^8\. ce qui reste"),
    ("Sources", r"^sources"),
]
THEMES_FICHE = ["Institutions", "Finances publiques et impôts", "Pouvoir d'achat et salaires", "Retraites",
                "Travail et emploi", "Logement", "Éducation", "Santé", "Sécurité et justice", "Énergie",
                "Climat et environnement", "Immigration", "Défense", "Europe"]


def est_fiche(md):
    return md.parent.name == "partis" and md.stem != INTRO_PARTIS

GABARIT = [  # (clé, libellé, motif sur les titres de niveau 2)
    ("essentiel", "L'essentiel", r"essentiel"),
    ("debat", "Ce qui fait débat", r"fait débat|enjeux|options"),
    ("partis", "Ce que proposent les partis", r"propos\w* les partis|partis proposent|programmes?"),
    ("evaluations", "Évaluations", r"évaluation"),
    ("debattre", "Pour débattre", r"pour débattre|affirmations"),
    ("incertains", "Points incertains", r"incertain"),
    ("sources", "Sources", r"^sources"),
]


MOTS_JUGE = re.compile(
    r"\b(ambitieu\w*|irréalist\w*|dangereu\w*|massi\w*|bien plus|jamais|seulement|prétend\w*|avoue\w*|ironis\w*|dénonc\w*|tacl\w*)\b"
    r"|\beffets? modestes?\b"
    r"|\b(?:n'|n’|ne )(?:(?!\b(?:pas|rien|aucun\w*|point|plus)\b)[^.;:«»]){0,40}?\b(?:qu'|qu’|que )(?!ce |celui|celle)",
    re.I)


def dossiers(only=None):
    out = []
    for md in sorted(ROOT.glob("*/*.md")):
        if md.parent.name in ("edition", "scripts") or md.parent.name.startswith(".") or " " in md.parent.name:
            continue
        if only and md.parent.name not in only:
            continue
        out.append(md)
    return out


def slug(title):
    s = title.strip().lower()
    s = "".join(c for c in s if unicodedata.category(c)[0] in "LN" or c in " -_")
    return s.replace(" ", "-")


def sections(text):
    """Découpe en sections de niveau 2 : liste de (titre, contenu)."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    out = [("_intro", parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1]))
    return out


def prose(text):
    """Texte courant, hors tableaux, titres, images, code et adresses des liens."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("|", "#", "![", "---", ">")):
            continue
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"`[^`]*`", " ", s)
        s = re.sub(r"^(\d+\.|[-*])\s+", "", s)
        s = s.replace("**", "").replace("*", "")
        lines.append(s)
    return lines


def phrases(lines):
    out = []
    for line in lines:
        for p in re.split(r"(?<=[.!?…])\s+(?=[A-ZÀÂÉÈÊÎÔÛÇ«(])", line):
            n = len(re.findall(r"[\wÀ-ÿ'’≈%€-]+", p))
            if n >= 3:
                out.append((n, p))
    return out


def sigles_non_developpes(body):
    clean = re.sub(r"\]\([^)]*\)", "]", body)  # retire les adresses des liens
    clean = re.sub(r"`[^`]*`", " ", clean)
    clean = re.sub(r"https?://\S+", " ", clean)
    seen, out = set(), []
    for m in re.finditer(r"(?<![\w/-])([A-Z][A-Z0-9&]{1,}(?:-[A-Z0-9]+)?)(?![\w/])", clean):
        s = m.group(1)
        if s in seen or s in ROMAINS or s in UNITES or s in SIGLES_COMMUNS or s in SIGLES_PARTIS or s in MARQUES:
            continue
        if len(re.findall(r"\d", s)) >= 3:
            continue
        seen.add(s)
        # Développé à la première apparition : « Nom complet (SIGLE) », « (…, SIGLE) » ou « SIGLE (nom complet) »
        before = clean[max(0, m.start() - 3):m.start()]
        after = clean[m.end():m.end() + 3]
        dev = (re.search(r"\(\s*$", before) and re.match(r"\s*[);,]", after)) \
            or (re.search(r",\s*$", before) and re.match(r"\s*[);]", after)) \
            or re.match(r"\s*\(", after)
        if not dev:
            a = max(0, m.start() - 60)
            ctx = clean[a:m.end() + 60].replace("\n", " ")
            out.append((s, ctx))
    return out


def lien_ok(md, target, anchors_cache):
    path, _, anchor = target.partition("#")
    dest = (md.parent / path).resolve() if path else md
    if not dest.exists():
        return False
    if not anchor:
        return True
    if dest not in anchors_cache:
        t = dest.read_text(encoding="utf-8")
        anchors_cache[dest] = {slug(h) for h in re.findall(r"^#{1,6} (.+)$", t, flags=re.M)}
    return anchor in anchors_cache[dest]


def sans_notes(text):
    """Retire les notes de source : appels [^etiquette] et définitions [^etiquette]: … (en fin de fichier)."""
    text = re.sub(r"^\[\^[^\]]+\]:.*$\n?", "", text, flags=re.M)
    return re.sub(r"\[\^[^\]]+\]", "", text)


def audit(md, anchors_cache):
    brut = md.read_text(encoding="utf-8")
    text = sans_notes(brut)
    secs = sections(text)
    titles = [t for t, _ in secs[1:]]
    body = "\n".join(c for t, c in secs if not re.match(r"sources", t, re.I))
    nom = md.parent.name + ("/" + md.stem if md.stem.startswith("encadre") or est_fiche(md) else "")
    r = {"dossier": nom, "fichier": md.name, "fiche": est_fiche(md)}
    r["mots"] = len(text.split())
    r["notes_appels"] = len(re.findall(r"\[\^[^\]]+\](?!:)", brut))
    r["notes_sources"] = len(re.findall(r"^\[\^[^\]]+\]:", brut, flags=re.M))
    r["pages_estimees"] = round(r["mots"] / 380)
    m = re.search(r"\*(?:État des connaissances au|Données arrêtées au|Version de travail du|Fiche du) ([^,.*]+)", text)
    r["date"] = m.group(1).strip() if m else None

    # Gabarit
    motifs = {k: (GABARIT_INTRO_PARTIS.get(k, p) if md.stem == INTRO_PARTIS else p) for k, _, p in GABARIT}
    r["gabarit"] = {k: any(re.search(motifs[k], t, re.I) for t in titles) for k, _, _ in GABARIT}
    r["titres"] = titles

    # L'essentiel
    ess = next((c for t, c in secs if re.search(r"essentiel|^en bref", t, re.I)), "")
    r["essentiel_points"] = len(re.findall(r"^(?:\d+\.|-)\s", ess, flags=re.M)) if r["fiche"] else \
        len(re.findall(r"^\d+\.\s", ess, flags=re.M))
    r["essentiel_mots"] = len(ess.split())
    r["essentiel_sigles"] = [s for s, _ in sigles_non_developpes(ess)]
    pts = re.split(r"\*\*[^*]*(?:options|lignes de partage)[^*]*\*\*", ess, maxsplit=1, flags=re.I)[0]
    pts = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", pts)
    r["essentiel_mots_points"] = len(pts.split())

    # Phrases
    ph = phrases(prose(body))
    longs = sorted(ph, key=lambda x: -x[0])
    r["phrases"] = len(ph)
    r["mots_par_phrase"] = round(sum(n for n, _ in ph) / max(1, len(ph)), 1)
    r["pct_phrases_30"] = round(100 * sum(1 for n, _ in ph if n > 30) / max(1, len(ph)), 1)
    r["phrases_40"] = sum(1 for n, _ in ph if n > 40)
    r["plus_longues"] = [(n, p[:220]) for n, p in longs[:8]]

    # Mots qui jugent (charte, section 3), hors citations entre guillemets
    voix = [re.sub(r"«[^»]*»", " ", l) for l in prose(body)]
    juge = []
    for l in voix:
        for m in MOTS_JUGE.finditer(l):
            juge.append(l[max(0, m.start() - 40):m.end() + 30])
    r["mots_qui_jugent"] = juge

    # Sigles
    sg = sigles_non_developpes(body)
    r["sigles_non_developpes"] = [s for s, _ in sg]
    r["sigles_contextes"] = sg[:60]

    # Marqueurs d'incertitude
    r["a_verifier"] = len(re.findall(r"à vérifier", text))
    r["source_secondaire"] = len(re.findall(r"source secondaire", text))
    r["calcul"] = len(re.findall(r"\(calcul\)", text))

    # Partis
    psec = next((c for t, c in secs if re.search(r"propos\w* les partis|partis proposent", t, re.I)), None)
    zone = psec if psec is not None else ""
    if md.parent.name == "partis":
        zone = text
    r["partis_section"] = psec is not None
    r["partis_couverts"] = [p for p, rx in PARTIS.items() if re.search(rx, zone)]
    r["colonne_levier"] = bool(re.search(r"\|\s*Levier\s*\|", zone))

    # Pour débattre
    dsec = next((c for t, c in secs if re.search(r"pour débattre", t, re.I)), "")
    rows = [l for l in dsec.splitlines() if l.startswith("|") and not re.match(r"\|\s*-", l)][1:]
    camps = {"gauche": 0, "centre": 0, "droite": 0, "non attribué": 0}
    nonstd = []
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        claim = cells[0] if cells else ""
        verdict = cells[1] if len(cells) > 1 else ""
        hit = False
        for camp, rx in CAMPS.items():
            if re.search(rx, claim):
                camps[camp] += 1
                hit = True
        if not hit:
            camps["non attribué"] += 1
        v = re.match(r"\*\*([^*]+)\*\*", verdict) or re.match(r"\**([^:.,;]+)", verdict)
        v = v.group(1).strip().strip("*") if v else ""
        if v not in VERDICTS:
            nonstd.append(v[:40])
    r["debattre_lignes"] = len(rows)
    r["debattre_camps"] = camps
    r["verdicts_hors_echelle"] = sorted(set(nonstd))

    # Liens et figures
    bad = []
    for tgt in re.findall(r"\]\(([^)\s]+)\)", text):
        if tgt.startswith(("http", "mailto")):
            continue
        if re.search(r"\.(png|jpg|svg)$", tgt):
            if not (md.parent / tgt).exists():
                bad.append(tgt)
            continue
        if not lien_ok(md, tgt, anchors_cache):
            bad.append(tgt)
    r["liens_casses"] = bad
    r["figures"] = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", text))

    # Fiches des partis : plan, ordre des sections et des 14 thèmes, notes dans « En bref »
    if r["fiche"]:
        pos = [next((i for i, t in enumerate(titles) if re.search(p, t, re.I)), None) for _, p in GABARIT_FICHE]
        r["fiche_sections_manquantes"] = [lab for (lab, _), i in zip(GABARIT_FICHE, pos) if i is None]
        trouvees = [i for i in pos if i is not None]
        r["fiche_ordre_ok"] = trouvees == sorted(trouvees)
        s3 = next((c for t, c in secs if re.search(r"^3\. ses propositions", t, re.I)), "")
        lignes = [l for l in s3.splitlines() if l.startswith("|") and not re.match(r"\|\s*-", l)][1:]
        themes = [l.strip("|").split("|")[0].strip().strip("*") for l in lignes]
        r["fiche_themes"] = themes
        r["fiche_themes_ok"] = themes == THEMES_FICHE
        r["fiche_en_bref_notes"] = len(re.findall(r"\[\^[^\]]+\]", next(
            (c for t, c in sections(brut) if re.search(r"^en bref", t, re.I)), "")))
    return r


def tableau(results):
    def ok(b):
        return "✓" if b else "—"

    L = ["# Audit automatique des dossiers", "",
         "*Généré par `edition/scripts/audit.py`. Cibles : voir `edition/charte.md`. "
         "Les sigles « non développés » sont détectés automatiquement : à confirmer à la main.*", "",
         "## Volume, date et lisibilité", "",
         "| Dossier | Mots | Pages ≈ | Date | Mots / phrase (cible ≤ 20) | Phrases > 30 mots (cible ≤ 10 %) | Phrases > 40 mots (cible 0) | Sigles non développés |",
         "|---|---|---|---|---|---|---|---|"]
    for r in results:
        L.append(f"| {r['dossier']} | {r['mots']:,} | {r['pages_estimees']} | {r['date'] or '?'} | {r['mots_par_phrase']} | "
                 f"{r['pct_phrases_30']} % | {r['phrases_40']} | {len(r['sigles_non_developpes'])} |".replace(",", " "))
    L += ["", "## Conformité au gabarit", "",
          "| Dossier | L'essentiel (points / mots ; mots des points, cible ≤ 350) | Ce qui fait débat | Partis | Colonne « Levier » | Évaluations | Pour débattre | Points incertains | Sources |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in [x for x in results if not x["fiche"]]:
        g = r["gabarit"]
        L.append(f"| {r['dossier']} | {ok(g['essentiel'])} {r['essentiel_points']} / {r['essentiel_mots']} ; {r['essentiel_mots_points']} | {ok(g['debat'])} | "
                 f"{ok(g['partis'] or r['dossier'] == 'partis')} | {ok(r['colonne_levier'] or r['dossier'] == 'partis')} | {ok(g['evaluations'])} | "
                 f"{ok(g['debattre'])} | {ok(g['incertains'])} | {ok(g['sources'])} |")
    fiches = [x for x in results if x["fiche"]]
    if fiches:
        L += ["", "## Fiches des partis (Partie V)", "",
              "| Fiche | Sections du gabarit (sur 10) | Ordre des sections | 14 thèmes dans l'ordre | En bref : points / mots | Notes dans « En bref » (cible 0) | Colonne « Levier » |",
              "|---|---|---|---|---|---|---|"]
        for r in fiches:
            L.append(f"| {r['dossier']} | {10 - len(r['fiche_sections_manquantes'])}"
                     + (f" (manque : {', '.join(r['fiche_sections_manquantes'])})" if r['fiche_sections_manquantes'] else "")
                     + f" | {ok(r['fiche_ordre_ok'])} | {ok(r['fiche_themes_ok'])} ({len(r['fiche_themes'])}) | "
                     f"{r['essentiel_points']} / {r['essentiel_mots']} | {r['fiche_en_bref_notes']} | {ok(r['colonne_levier'])} |")
    L += ["", "## Partis et équilibre", "",
          "| Dossier | Partis retenus mentionnés dans la section « partis » (sur 8) | Jamais mentionnés | « Pour débattre » : lignes | gauche / centre / droite / non attribué | Verdicts hors échelle |",
          "|---|---|---|---|---|---|"]
    for r in [x for x in results if not x["fiche"]]:
        absents = [p for p in PARTIS if p not in r["partis_couverts"]]
        c = r["debattre_camps"]
        L.append(f"| {r['dossier']} | {len(r['partis_couverts'])} | {', '.join(absents) or '—'} | {r['debattre_lignes']} | "
                 f"{c['gauche']} / {c['centre']} / {c['droite']} / {c['non attribué']} | {', '.join(r['verdicts_hors_echelle']) or '—'} |")
    L += ["", "## Incertitude, liens et figures", "",
          "| Dossier | « à vérifier » | « source secondaire » | « (calcul) » | Figures | Liens ou images cassés |",
          "|---|---|---|---|---|---|"]
    for r in results:
        L.append(f"| {r['dossier']} | {r['a_verifier']} | {r['source_secondaire']} | {r['calcul']} | {r['figures']} | "
                 f"{', '.join(r['liens_casses']) or '—'} |")
    L += ["", "## Mots qui jugent, hors citations (charte, section 3 ; à confirmer à la main)", ""]
    for r in results:
        j = r["mots_qui_jugent"]
        L.append(f"- **{r['dossier']}** ({len(j)})" + (" : " + " · ".join("…" + x.strip() + "…" for x in j[:6]) if j else ""))
    L += ["", "## Sigles probablement non développés, par dossier", ""]
    for r in results:
        L.append(f"- **{r['dossier']}** ({len(r['sigles_non_developpes'])}) : {', '.join(r['sigles_non_developpes']) or '—'}")
    L += ["", "## Sigles non développés dans « L'essentiel »", ""]
    for r in results:
        if r["essentiel_sigles"]:
            L.append(f"- **{r['dossier']}** : {', '.join(r['essentiel_sigles'])}")
    L += ["", "## Phrases les plus longues, par dossier", ""]
    for r in results:
        L.append(f"**{r['dossier']}**")
        L.append("")
        for n, p in r["plus_longues"][:5]:
            L.append(f"- ({n} mots) {p}…")
        L.append("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    only = set(sys.argv[1:]) or None
    cache = {}
    res = [audit(md, cache) for md in dossiers(only)]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "indicateurs.md").write_text(tableau(res), encoding="utf-8")
    (OUT / "indicateurs.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in res:
        print(f"{r['dossier']:30s} {r['mots']:6d} mots  {r['mots_par_phrase']:5.1f} m/ph  {r['pct_phrases_30']:5.1f}% >30  "
              f"sigles {len(r['sigles_non_developpes']):3d}  juge {len(r['mots_qui_jugent']):3d}  partis {len(r['partis_couverts'])}/8  liens cassés {len(r['liens_casses'])}")
