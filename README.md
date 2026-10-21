# Présidentielle 2027 : Comprendre avant de choisir

Un livre factuel sur les grands sujets de l'élection présidentielle de 2027. Pour chaque thème : la situation, ce qui fait débat, ce que proposent les partis, comment ils le mettraient en place et ce qui pourrait les en empêcher, ce que montrent les évaluations, et des affirmations entendues dans le débat, vérifiées une à une.

Le livre ne recommande aucun vote et ne juge aucun programme dans son ensemble. Il applique la même exigence à tous les partis. Chaque chiffre a une unité, une année et une source.

**[Lire le livre en ligne](https://nathanhaboury.github.io/Presidentielle-2027/)** · **[Télécharger le PDF](https://nathanhaboury.github.io/Presidentielle-2027/presidentielle-2027.pdf)**

> **Version de travail du 21 octobre 2026.**
> - Les chiffres datent du 7 au 12 octobre 2026, selon les chapitres, avec des corrections du 21 octobre 2026 après une relecture externe. La première édition, avec des chiffres arrêtés à une même date, est visée pour la fin de 2026.
> - Ce qui n'est pas vérifié est signalé : *(à vérifier)* dans le texte, et la section « Points incertains » à la fin de chaque chapitre.
> - La recherche et la rédaction sont faites avec l'aide d'une intelligence artificielle (Claude, d'Anthropic), avec relecture et contrôle des sources.
> - Le livre peut contenir des erreurs : merci de les [signaler](#signaler-une-erreur).

## Par où commencer

- L'[introduction](index.qmd) : pourquoi ce livre, ce qu'il contient, comment il est fait.
- [Les grands enjeux de 2027](edition/livre/enjeux.qmd) : huit questions qui traversent les chapitres.
- [Le livre en bref](edition/livre/livre_en_bref.qmd) : une fiche par chapitre.
- Le [mode d'emploi](edition/livre/mode_emploi.qmd) : le plan des chapitres et des fiches, le choix des partis, les verdicts.

Sur le site, les notes de source s'ouvrent au survol ; dans le PDF du livre, elles sont regroupées à la fin de chaque chapitre.

## Les chapitres

Chaque chapitre se lit seul, en ligne, en Markdown ici, ou en PDF.

| Partie | Chapitre | Texte | PDF |
|---|---|---|---|
| Le cadre | Institutions : comment la France est gouvernée | [Markdown](institutions/institutions.md) | [PDF](institutions/institutions.pdf) |
| Économie et finances | Finances publiques : dépenses, recettes, déficit, dette | [Markdown](finances-publiques/finances_publiques.md) | [PDF](finances-publiques/finances_publiques.pdf) |
|  | Pouvoir d'achat, salaires et inégalités | [Markdown](pouvoir-achat/pouvoir_achat.md) | [PDF](pouvoir-achat/pouvoir_achat.pdf) |
|  | Retraites et productivité : faut-il travailler plus longtemps ? | [Markdown](retraites-productivite/retraites_productivite.md) | [PDF](retraites-productivite/retraites_productivite.pdf) |
|  | Travail et emploi | [Markdown](travail-emploi/travail_emploi.md) | [PDF](travail-emploi/travail_emploi.pdf) |
|  | Logement | [Markdown](logement/logement.md) | [PDF](logement/logement.pdf) |
| Services publics | Éducation | [Markdown](education/remuneration_enseignants.md) | [PDF](education/remuneration_enseignants.pdf) |
|  | Santé et assurance maladie | [Markdown](sante/sante_assurance_maladie.md) | [PDF](sante/sante_assurance_maladie.pdf) |
|  | Sécurité et justice | [Markdown](securite-justice/securite_justice.md) | [PDF](securite-justice/securite_justice.pdf) |
| Énergie et climat | Énergie : électricité, carburants, électrification | [Markdown](energie/energie_france_europe_allemagne.md) | [PDF](energie/energie_france_europe_allemagne.pdf) |
|  | Climat et environnement | [Markdown](climat-environnement/climat_environnement.md) | [PDF](climat-environnement/climat_environnement.pdf) |
| La France dans le monde | Immigration : chiffres, coût, délinquance, comparaisons européennes | [Markdown](immigration/immigration.md) | [PDF](immigration/immigration.pdf) |
|  | Défense et Europe | [Markdown](defense-europe/defense_europe.md) | [PDF](defense-europe/defense_europe.pdf) |
| Les partis | Présidentielle 2027 : ce que proposent les partis (introduction) | [Markdown](partis/programmes_partis_2027.md) | [PDF](partis/programmes_partis_2027.pdf) |
|  | Fiches des partis | [LFI](partis/lfi.md) · [Les Écologistes](partis/ecologistes.md) · [PS-Place publique](partis/ps_place_publique.md) · [Renaissance](partis/renaissance.md) · [Horizons](partis/horizons.md) · [LR](partis/lr.md) · [RN](partis/rn.md) · [Reconquête](partis/reconquete.md) | [LFI](partis/lfi.pdf) · [Les Écologistes](partis/ecologistes.pdf) · [PS-Place publique](partis/ps_place_publique.pdf) · [Renaissance](partis/renaissance.pdf) · [Horizons](partis/horizons.pdf) · [LR](partis/lr.pdf) · [RN](partis/rn.pdf) · [Reconquête](partis/reconquete.pdf) |
| Annexes | Étude de cas : TotalEnergies, profits et impôts | [Markdown](finances-publiques/encadre_totalenergies.md) | [PDF](finances-publiques/encadre_totalenergies.pdf) |
|  | Glossaire commun | [Markdown](edition/glossaire.md) | — |

## Signaler une erreur

Les corrections sont bienvenues, d'où qu'elles viennent. Ouvrez une [issue](https://github.com/NathanHaboury/Presidentielle-2027/issues/new/choose) avec l'un des trois formulaires :

- **Erreur factuelle ou source** : un chiffre, une date, une citation ou une source à corriger ;
- **Biais ou déséquilibre** : un passage qui penche, ou un parti traité avec une exigence différente ;
- **Remarque sur la structure** : la façon de présenter un sujet.

Ce qui aide le plus : le chapitre, la section, la phrase exacte, et une source, si possible primaire.

## Méthode

Les règles de rédaction sont dans la [charte éditoriale](edition/charte.md). Les termes et les sigles sont définis dans le [glossaire](edition/glossaire.md).

## Reconstruire le livre

| Tâche | Commande | Outils |
|---|---|---|
| Construire le site et le PDF du livre, dans `docs/` | `quarto render` | [Quarto](https://quarto.org) 1.10 ou plus récent |
| Régénérer les graphiques d'un chapitre | `python3 <thème>/scripts/charts.py` | Python 3, matplotlib |
| Régénérer les PDF des chapitres | `python3 edition/scripts/build_pdfs.py` | pandoc, Playwright |

Le site est publié par GitHub Pages à partir du dossier `docs/`.

## Licence

Textes, tableaux, graphiques et PDF : CC BY 4.0. Code : MIT. Détails dans [LICENSE.md](LICENSE.md).
