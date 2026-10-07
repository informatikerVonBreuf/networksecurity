# Architecture et d?cisions

## Contrats entre les ?tapes

1. **Ingestion** (`data_ingestion.py`) charge un CSV ou une collection MongoDB,
   retire `_id`, normalise `na` et conserve un snapshot. `StratifiedGroupKFold`
   construit un holdout sans chevauchement de groupes de caract?ristiques. La graine
   42 fixe le d?coupage. Le split est effectu? avant tout apprentissage.
2. **Validation** (`data_validation.py`) v?rifie les noms exacts des 31 colonnes,
   leurs valeurs num?riques, l'absence d'infinis et les cibles dans `{-1, 1}`.
   Une caract?ristique enti?rement manquante provoque un ?chec. Les copies valid?es
   sont les fichiers effectivement transmis ? la suite. La validation du sch?ma
   conditionne l'entra?nement ; une diff?rence KS est seulement consign?e.
3. **Pr?paration** (`data_transformation.py`) encode la cible, conserve les NaN
   et ?crit des tableaux NumPy. La derni?re colonne contient la cible. Aucun imputer
   n'est ajust? ici : le chemin de pr?traitement sera rempli ? l'?tape entra?nement.
4. **Entra?nement** (`model_trainer.py`) compare cinq familles de classifieurs,
   deux configurations par famille et trois plis de CV par groupes. Chaque candidat
   est un pipeline imputer KNN puis classifieur ; chaque pli ajuste son propre imputer.
   Le meilleur F1 moyen de CV doit atteindre 0,6. `GridSearchCV` r?ajuste le candidat
   s?lectionn? sur tout l'entra?nement ; il est ensuite ?valu? sur le holdout.
5. **Publication locale** ?crit le bundle `NetworkModel` dans les artefacts du run
   et remplace `final_model/model.pkl` ? partir d'un fichier temporaire. Le bundle
   contient le pr?traitement, le classifieur et les noms attendus. Le rapport JSON
   est ?crit s?par?ment : ce n'est pas une transaction atomique de tous les fichiers.
6. **Inf?rence** applique le m?me pr?traitement sans le r?ajuster. Les colonnes
   peuvent ?tre r?ordonn?es, mais tout champ manquant ou suppl?mentaire est rejet?.
   Les tableaux HTML ?chappent leurs cellules ; les artefacts pickle restent des
   fichiers internes de confiance et ne sont jamais accept?s comme upload.

## Artefacts

`Artifacts/<run>/` contient le snapshot, les splits bruts et valid?s, le rapport KS,
les tableaux NumPy, le pr?traitement ajust?, le bundle et le rapport de s?lection.
`final_model/` contient le bundle de service et ses m?triques. Ces fichiers g?n?r?s,
les logs et les CSV de pr?diction sont ignor?s par Git pour ?viter toute confusion
avec les donn?es sources et les preuves de r?sultats document?es.

## Choix de conception

| Choix | Raison | Compromis |
|---|---|---|
| CSV local par d?faut dans la d?mo | D?monstration sans comptes cloud | Source historique statique |
| Groupes identifi?s par hash des caract?ristiques | ?carter les doublons entre partitions | Split approximativement stratifi? ; multiplicit? conserv?e |
| F1 positif pour la s?lection | M?trique de classification coh?rente | Co?t m?tier et classe phishing encore ? confirmer |
| KNNImputer dans le pipeline CV | ?viter la fuite du pr?traitement | Pas de NaN dans le fichier fourni ; co?t accru si donn?es volumineuses |
| Grille r?duite de cinq mod?les | D?monstration courte et lisible | Recherche non exhaustive |
| Bundle unique | Coh?rence entra?nement/inf?rence | Couplage aux versions Python/scikit-learn |
| Entra?nement par CLI | ?viter de lancer un job via une route GET | Pas d'ordonnanceur de jobs |
| Options explicites MLflow/S3 | Contr?le des transferts et d?mo autonome | Int?grations non test?es sur un compte r?el |
| CI sans d?ploiement automatique | Tests r?els sans param?tres d'un autre compte | CD ? construire avec l'infrastructure de l'utilisateur |

## Ce qui reste ? construire pour la production

Authentification, quotas d'upload, suivi des erreurs/latences, ?valuation sur une source
externe ou temporelle, suivi de d?rive sur les entr?es r?elles, stockage/versionnement des
donn?es, registre de mod?les, promotion contr?l?e, rollback et d?ploiement automatis?.
Les groupes contradictoires demandent une revue des annotations. L'extraction de
caract?ristiques ? partir d'URL reste un composant distinct non pr?sent dans ce d?p?t.

## R?f?rences techniques

- [scikit-learn : validation crois?e et pipelines](https://scikit-learn.org/stable/modules/cross_validation.html)
- [MLflow : serveur de suivi](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/)
