# V?rifications de la pr?paration

V?rification locale effectu?e le 7 octobre 2026. Environnement : Python 3.13.11,
scikit-learn 1.7.1 et pandas 2.3.3. Les m?triques et le hash du CSV sont conserv?s dans
`results.json` ; les versions du rapport correspondent ? cette mesure, pas n?cessairement
aux prochaines installations utilisant les plages de d?pendances.

## V?rifications pass?es

- `ruff check .` et `ruff format --check .`.
- Huit tests automatis?s : noms de colonnes, cibles et infinis, F1 de s?lection,
  ajustement du pr?traitement ? l'int?rieur des plis, bundle s?rialis?, r?ponses API,
  s?paration des doublons entre train/test et entre les plis de CV.
- Entra?nement complet local, depuis le CSV source jusqu'au bundle d'inf?rence.
- Pr?diction batch sur un CSV de d?monstration et sur l'exemple fourni initialement.
- Pr?diction API avec le mod?le r?ellement entra?n? via le client de test FastAPI.
- V?rification du d?p?t distant par Git et par l'API GitHub.
- CI de l'?tape API r?ussie sur GitHub, incluant la construction Docker ; la CI du
  dernier commit doit aussi ?tre v?rifi?e dans l'onglet Actions.

Les deux premiers commits sont des ?tapes incompl?tes : leurs workflows peuvent ?chouer
par absence de tests ou de composants complets. La branche finale est la r?f?rence.

## R?sultats corrig?s

Random Forest : F1 test 0,9593 ; pr?cision 0,9584 ; rappel 0,9601.
Le F1 train est 0,9909 : cet ?cart appelle une ?valuation externe, plut?t qu'une promesse
de performance en production. Le score initial de 0,9774, mesur? avant le regroupement
des doublons, a ?t? remplac? par cette ?valuation corrig?e.

## Limites des v?rifications

Le moteur Docker local n'?tait pas d?marr? ; le build a ?t? v?rifi? dans GitHub Actions.
Aucune connexion r?elle ? MongoDB, aucun serveur MLflow ni synchronisation AWS/S3 n'a
?t? utilis?. Aucun d?ploiement AWS n'est annonc?. La provenance/licence du fichier source
et le sens m?tier des classes restent ? confirmer. Le mod?le n'est pas test? sur de
nouvelles campagnes de phishing et le CSV de d?mo n'est pas une ?valuation ind?pendante.

## Reproduire

```powershell
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest -q --basetemp=.pytest_tmp
python main.py --source-csv Network_Data/phisingData.csv
python scripts/export_results.py
python scripts/make_demo_csv.py
python -m networksecurity.pipeline.batch_prediction prediction_output/demo.csv prediction_output/predictions.csv
```

Le r?pertoire temporaire des tests est plac? dans le projet pour ?viter une erreur de
droits rencontr?e avec le r?pertoire temporaire global Windows. Il est ignor? par Git.
