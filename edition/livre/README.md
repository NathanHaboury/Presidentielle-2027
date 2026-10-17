# Le livre : construction

Le document unifié est un livre [Quarto](https://quarto.org). Les fichiers Markdown des dossiers restent la source unique : le livre les lit tels quels et produit un site web et un PDF.

## Construire le livre

Il faut Quarto 1.10 ou plus récent (sur Mac : `brew install --cask quarto`). Le PDF est produit avec Typst, inclus dans Quarto : il n'y a rien d'autre à installer.

Depuis la racine du dépôt :

| Commande | Résultat |
|---|---|
| `quarto render` | Le site et le PDF, dans `_book/` (≈ 1 minute) |
| `quarto render --to typst` | Le PDF seul : `_book/presidentielle-2027.pdf` |
| `quarto render --to html` | Le site seul : ouvrir `_book/index.html` |
| `quarto preview` | Le site dans le navigateur, mis à jour à chaque modification |

Le dossier `_book/` n'est pas versionné (voir `.gitignore`).

## Les fichiers

| Fichier | Rôle |
|---|---|
| `_quarto.yml` (racine) | Plan du livre : parties, chapitres, annexes ; réglages du site et du PDF |
| `index.qmd` (racine) | Introduction : pourquoi ce livre, ce qu'il contient, comment il est fait (sources, date des chiffres, méthode), par où commencer. L'état des chapitres est dans le README racine |
| `edition/livre/enjeux.qmd` | Les grands enjeux de 2027 : huit questions qui traversent les chapitres, sans parti nommé |
| `edition/livre/livre_en_bref.qmd` | Le livre en bref : une fiche par chapitre. « À savoir » s'écrit à la main ; « En débat » est mis à jour par `edition/scripts/livre_en_bref.py` |
| `edition/livre/mode_emploi.qmd` | Mode d'emploi : plan d'un chapitre et des fiches, partis retenus et ordre, leviers, verdicts, signes, notes, unités, sigles |
| `edition/livre/filtres/livre.lua` | Filtre qui adapte les dossiers au livre (voir ci-dessous) |
| `edition/livre/filtres/notes.lua` | Filtre des notes de source : une source appelée plusieurs fois garde un seul numéro ; dans le PDF du livre, notes en fin de chapitre (aussi utilisé par `edition/scripts/build_pdfs.py`) |
| `edition/livre/typst/typst-show.typ` | Copie du gabarit PDF « orange-book » de Quarto, avec un réglage : les pages de partie ne listent que les chapitres |

## Ce que fait le filtre

Les dossiers sont écrits pour GitHub. Le filtre les adapte au moment du rendu, sans modifier les fichiers :

- **Ancres.** Chaque titre reçoit une ancre unique, `<fichier>--<ancre GitHub>`, et les liens internes sont réécrits. Sans cela, le PDF, qui réunit tous les chapitres, aurait douze sections « Sources » de même nom.
- **Liens hors du livre** (charte, audit…) : ils pointent vers le fichier sur GitHub.
- **Titres de niveau 1 en trop** (« Partie A », « Partie B ») : ils descendent d'un niveau, avec leurs sous-titres.
- **Sections retirées du livre** : « Sommaire » (le livre a sa table des matières) et « À vérifier » du glossaire. Elles restent sur GitHub.
- **Graphiques** : le titre est déjà dans l'image, il n'est pas répété en légende.
- **Tableaux** : la largeur des colonnes suit la longueur du texte.
- **Notes de source** (`notes.lua`) : sur GitHub, une source appelée plusieurs fois (`[^insee-2106]`) n'a qu'une note ; Pandoc en créerait une par appel. Sur le site, le filtre garde la première note et fait pointer les appels suivants vers elle ; la note s'ouvre au survol. Dans le PDF du livre, les notes ne sont pas en bas de page : elles sont regroupées à la fin de chaque chapitre, sous « Notes de source », avec un seul numéro par source et une numérotation qui repart de 1 à chaque chapitre.

Les réglages du PDF dans `_quarto.yml` ajoutent deux choses : seuls les chapitres sont numérotés (les dossiers numérotent eux-mêmes leurs sections), et l'en-tête de page donne le titre du chapitre.

## Ajouter un chapitre

1. Écrire le dossier selon la charte (`edition/charte.md`).
2. Dans `_quarto.yml`, ajouter son chemin **à deux endroits** : la liste `render` et la partie voulue sous `chapters`.
3. Mettre à jour le tableau des chapitres dans le `README.md` racine.
4. Ajouter sa fiche dans `edition/livre/livre_en_bref.qmd` (ligne « À savoir » et bloc `<!-- en-debat: … -->`), puis lancer `python3 edition/scripts/livre_en_bref.py`. À relancer après toute modification des questions de la section 2 ; `--check` dit si la page est à jour.

## Limites connues

- Les pages blanches placées avant une partie portent l'en-tête du chapitre précédent.
- Dans le glossaire, la colonne « Chapitres » donne le nom des dossiers (`energie`, `sante`…), pas le titre des chapitres.
- Le PDF pèse ≈ 18 Mo, surtout à cause des graphiques en haute résolution.
