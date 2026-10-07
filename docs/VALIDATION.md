# Vérifications et limites

Les mesures locales ont été réalisées le **7 octobre 2026**, avec Python 3.13.11,
scikit-learn 1.7.1 et pandas 2.3.3. Le rapport [results.json](results.json) contient
les métriques détaillées, l’empreinte du CSV et le contrôle des partitions.

## Vérifications réalisées

| Vérification | Résultat |
| --- | --- |
| Lint et formatage Ruff | Réussis |
| Tests automatisés | 8 tests réussis |
| Entraînement complet sur le CSV fourni | Réussi |
| Prédiction depuis un CSV | Réussie |
| API avec le modèle entraîné | Réponse HTTP 200 |
| Chevauchement des groupes entraînement/test | Aucun |
| CI et construction Docker | Réussies dans GitHub Actions |

[Workflow de référence](https://github.com/informatikerVonBreuf/networksecurity/actions/runs/37653581840),
sur le commit `9548ba8`. L’état de la version actuelle est indiqué par le badge du README.

Les tests vérifient les colonnes attendues, les cibles et les valeurs infinies, la métrique
de sélection, l’ajustement du prétraitement dans les plis, la sérialisation du modèle,
les réponses de l’API et la séparation des doublons entre partitions.

## Résultats de l’évaluation

| Mesure | Valeur |
| --- | ---: |
| F1 moyen en validation croisée | 0,9544 |
| F1 sur l’entraînement | 0,9909 |
| F1 sur le test | 0,9593 |
| Précision sur le test | 0,9584 |
| Rappel sur le test | 0,9601 |

Le test contient 2 157 lignes et l’entraînement 8 898 lignes. Aucun groupe de
caractéristiques identiques n’est présent dans les deux partitions.

Le premier score de test, 0,9774, avait été obtenu avant le regroupement des doublons.
Il a été remplacé par le résultat corrigé. L’écart entre entraînement et test mérite
une évaluation sur de nouvelles données.

## Ce que ces vérifications ne couvrent pas

MongoDB, MLflow et S3 n’ont pas été utilisés sur des services réels. Le moteur Docker
local n’était pas démarré ; la construction a été vérifiée dans GitHub Actions.

Le CSV est un jeu historique dont la provenance et les droits de redistribution restent
à préciser. Il contient 64 groupes de caractéristiques aux cibles contradictoires.
Le sens métier des classes doit être confirmé avec la source. Les métriques actuelles
ne mesurent pas la détection de campagnes de phishing récentes.

Les dépendances utilisent des plages de versions. Les versions de la mesure sont
consignées, mais l’installation n’est pas verrouillée intégralement.

## Reproduire les vérifications

```powershell
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest -q --basetemp=.pytest_tmp
python main.py --source-csv Network_Data/phisingData.csv
python scripts/export_results.py
python -m networksecurity.pipeline.batch_prediction examples/predict.csv prediction_output/results.csv
```

Le dossier temporaire `.pytest_tmp/` reste dans le projet et est ignoré par Git.
Cela évite les problèmes de droits rencontrés avec le répertoire temporaire Windows.
