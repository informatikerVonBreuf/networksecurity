# Étapes du projet

Le dossier fourni n’avait pas d’historique Git. Les commits ci-dessous suivent les étapes
de sa mise en place et de sa préparation pour une démonstration.

| Commit | Étape | Changements |
| --- | --- | --- |
| `0a0a1bd` | Squelette | Dépendances, configuration, exclusions Git, Docker et workflow |
| `2168235` | Entraînement | Pipeline, schéma, métriques de classification et sélection par CV |
| `46d1fc5` | Inférence | API, prédiction CSV, scripts de démonstration et tests |
| `7818844` | Doublons | Découpage par groupes en entraînement/test et en validation croisée |
| `9548ba8` | Documentation | Architecture, présentation, vérifications et résultats mesurés |

Les deux premiers commits sont des étapes intermédiaires : leur CI n’était pas encore
complète. La branche `main` contient la version à utiliser pour la démonstration.

La relecture des textes corrige leur encodage UTF-8 et simplifie la documentation.
La page de résultats affiche un résumé du fichier et un tableau adapté aux petits écrans.
