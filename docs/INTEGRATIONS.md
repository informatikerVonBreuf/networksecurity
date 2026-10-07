# Intégrations optionnelles

Le mode CSV fonctionne sans compte externe. Pour utiliser un service, copier
`.env.example` vers `.env` et renseigner les variables correspondantes.

## MongoDB

Configurer `MONGO_DB_URL`, `MONGO_DATABASE` et `MONGO_COLLECTION`, puis vérifier
la connexion :

```powershell
python scripts/check_mongodb.py
```

Pour charger le CSV et entraîner depuis la collection :

```powershell
python push_data.py --source-csv Network_Data/phisingData.csv
python main.py
```

L’import ajoute les documents à la collection. Le relancer ajoute à nouveau les mêmes
lignes. Le pipeline ferme la connexion après avoir lu les données.

## MLflow

Installer les dépendances de suivi :

```powershell
python -m pip install -r requirements-tracking.txt
```

Renseigner `MLFLOW_TRACKING_URI` et, si nécessaire, les variables d’authentification,
puis lancer :

```powershell
python main.py --source-csv Network_Data/phisingData.csv --track-mlflow
```

Le run enregistre le modèle, les métriques et les scores de comparaison. Sans cette
option, aucun résultat n’est envoyé à MLflow, même si une URI est définie.

Une erreur de suivi empêche la publication du nouveau modèle de service. Le registre
de modèles et la promotion automatique restent à développer.

## S3

Installer AWS CLI, configurer son authentification et renseigner
`TRAINING_BUCKET_NAME`, puis lancer :

```powershell
python main.py --source-csv Network_Data/phisingData.csv --sync-s3
```

Les fichiers sont archivés sous un identifiant de run. Un transfert échoué arrête la
commande avec une erreur ; le modèle local peut déjà avoir été enregistré.

## Configuration et secrets

Les fichiers `.env`, les logs et les modèles générés sont exclus de Git et de l’image
Docker. Un ancien jeton présent dans la base du projet a été retiré avant les premiers
commits. Il doit être révoqué auprès du service concerné.

Ces intégrations demandent des vérifications sur les comptes utilisés avant un
déploiement. Le workflow actuel teste le projet et construit l’image ; il ne déploie
pas automatiquement de service AWS.
