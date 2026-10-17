"""Génère une version PDF de chaque dossier (Markdown -> HTML -> PDF).

Prérequis : pandoc et Playwright (Chromium).
    pip install playwright && playwright install chromium
Usage, depuis la racine du dépôt :
    python3 edition/scripts/build_pdfs.py            # tous les dossiers
    python3 edition/scripts/build_pdfs.py partis     # un ou plusieurs dossiers
"""
import html
import re
import sys
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]  # racine du dépôt (edition/scripts/ -> racine)
REPO_URL = "https://github.com/NathanHaboury/Presidentielle-2027/blob/main"

DOCS = [
    ("institutions", "institutions.md", "Institutions : comment la France est gouvernée"),
    ("energie", "energie_france_europe_allemagne.md", "Énergie : électricité, carburants, électrification"),
    ("climat-environnement", "climat_environnement.md", "Climat et environnement"),
    ("finances-publiques", "finances_publiques.md", "Finances publiques"),
    ("finances-publiques", "encadre_totalenergies.md", "Étude de cas : TotalEnergies, profits et impôts"),
    ("education", "remuneration_enseignants.md", "Éducation"),
    ("partis", "programmes_partis_2027.md", "Présidentielle 2027 : ce que proposent les partis"),
    ("partis", "lfi.md", "Fiche : La France insoumise (LFI)"),
    ("partis", "ecologistes.md", "Fiche : Les Écologistes"),
    ("partis", "ps_place_publique.md", "Fiche : PS-Place publique"),
    ("partis", "renaissance.md", "Fiche : Renaissance"),
    ("partis", "horizons.md", "Fiche : Horizons"),
    ("partis", "lr.md", "Fiche : Les Républicains (LR)"),
    ("partis", "rn.md", "Fiche : Rassemblement national (RN)"),
    ("partis", "reconquete.md", "Fiche : Reconquête"),
    ("retraites-productivite", "retraites_productivite.md", "Retraites et productivité"),
    ("travail-emploi", "travail_emploi.md", "Travail et emploi"),
    ("immigration", "immigration.md", "Immigration : chiffres, coût, délinquance, comparaisons"),
    ("pouvoir-achat", "pouvoir_achat.md", "Pouvoir d'achat, salaires et inégalités"),
    ("comparaisons-internationales", "comparaisons_internationales.md", "Comparaisons internationales : LFI et Mamdani, RN et Meloni"),
    ("securite-justice", "securite_justice.md", "Sécurité et justice"),
    ("sante", "sante_assurance_maladie.md", "Santé et assurance maladie"),
    ("logement", "logement.md", "Logement"),
    ("defense-europe", "defense_europe.md", "Défense et Europe"),
]

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
:root { --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --rule:#e1e0d9; --accent:#2a78d6; --soft:#f4f3ef; }
html { font-family: Inter, "Helvetica Neue", Arial, sans-serif; font-size: 10pt; color: var(--ink); }
body { line-height: 1.45; margin: 0; }
h1 { font-size: 22pt; line-height: 1.15; margin: 0 0 4mm; letter-spacing: -0.01em; }
h1 + p em { color: var(--ink2); }
h2 { font-size: 15pt; margin: 0 0 3mm; padding-top: 1mm; break-before: page; break-after: avoid; }
h2#sommaire, h2[id^="lessentiel"] { break-before: auto; margin-top: 7mm; }
h3 { font-size: 12pt; margin: 6mm 0 2mm; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 5mm 0 2mm; break-after: avoid; }
p { margin: 0 0 2.4mm; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 2.6mm; padding-left: 6mm; }
li { margin: 0.6mm 0; }
li > ul, li > ol { margin: 0.8mm 0 0.8mm; }
a { color: var(--accent); text-decoration: none; word-break: break-word; }
strong { font-weight: 650; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.5pt; background: var(--soft); padding: 0 1mm; border-radius: 2px; }
hr { display: none; }
img { display: block; max-width: 100%; margin: 3mm auto 4mm; break-inside: avoid; }
p:has(> img) { break-inside: avoid; }
table { width: 100%; border-collapse: collapse; margin: 2mm 0 4mm; font-size: 8.3pt; line-height: 1.35; break-inside: auto; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { text-align: left; font-weight: 650; background: var(--soft); border-bottom: 1.2px solid #c3c2b7; }
th, td { padding: 1.4mm 1.8mm; vertical-align: top; border-bottom: 0.6px solid var(--rule); }
.cover-meta { color: var(--ink2); font-size: 9pt; margin-bottom: 5mm; }
.footnote-ref { text-decoration: none; }
.footnote-ref sup { font-size: 6.5pt; line-height: 0; color: var(--ink2); }
.footnotes { break-before: page; font-size: 8pt; line-height: 1.35; color: var(--ink2); }
.footnotes::before { content: "Notes de source"; display: block; font-size: 15pt; font-weight: 600; color: var(--ink); margin-bottom: 3mm; }
.footnotes hr { display: none; }
.footnotes ol { padding-left: 8mm; }
.footnotes li { margin-bottom: 0.6mm; }
.footnote-back { text-decoration: none; }
"""

TEMPLATE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>{title}</title>
<style>{css}</style></head>
<body>{body}</body></html>"""

FOOTER = """<div style="width:100%;font-family:Inter,Arial,sans-serif;font-size:7.5pt;color:#898781;
padding:0 16mm;display:flex;justify-content:space-between;">
<span>{title} · github.com/NathanHaboury/Presidentielle-2027</span>
<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>"""


def md_to_html(md_path: Path) -> str:
    # notes.lua regroupe les notes de source répétées (même source = même numéro).
    out = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5",
                          "--lua-filter", str(ROOT / "edition/livre/filtres/notes.lua"), str(md_path)],
                         check=True, capture_output=True, text=True).stdout
    # Les liens vers les autres dossiers, ou vers un autre fichier du même dossier (fiches des partis),
    # pointent vers GitHub (un lien relatif ne marche pas dans un PDF).
    def fix(m):
        href = m.group(1)
        cible = href.split("#")[0]
        if href.startswith("../") and cible.endswith(".md"):
            return f'href="{REPO_URL}/{href[3:]}"'
        if cible.endswith(".md") and not href.startswith(("http", "/")):
            return f'href="{REPO_URL}/{md_path.parent.name}/{href}"'
        return m.group(0)
    return re.sub(r'href="([^"]+)"', fix, out)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        only = set(sys.argv[1:])
        for folder, md_name, title in DOCS:
            if only and folder not in only:
                continue
            d = ROOT / folder
            md = d / md_name
            if not md.exists():  # dossier absent (par exemple dans le dépôt public)
                continue
            body = md_to_html(md)
            html_path = d / "_print.html"
            css = CSS
            if folder == "partis" and md_name != "programmes_partis_2027.md":
                # Fiches des partis : sections courtes, pas de saut de page avant chaque section
                css += "\nh2 { break-before: auto; margin-top: 7mm; }\n"
            elif md_name == "programmes_partis_2027.md":
                # En-tête long (liste des fiches, mode de lecture) : « L'essentiel » commence sur une nouvelle page
                css += '\nh2[id^="lessentiel"] { break-before: page; margin-top: 0; }\n'
            html_path.write_text(TEMPLATE.format(title=html.escape(title), css=css, body=body), encoding="utf-8")
            page.goto(html_path.as_uri(), wait_until="networkidle")
            pdf_path = d / md_name.replace(".md", ".pdf")
            page.pdf(path=str(pdf_path), format="A4", print_background=True,
                     margin={"top": "16mm", "bottom": "18mm", "left": "16mm", "right": "16mm"},
                     display_header_footer=True, header_template="<span></span>",
                     footer_template=FOOTER.format(title=html.escape(title)))
            html_path.unlink()
            print("ok", pdf_path.relative_to(ROOT))
        browser.close()


if __name__ == "__main__":
    main()
