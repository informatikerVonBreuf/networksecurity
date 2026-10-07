# Architecture

Le pipeline sépare les étapes d’entraînement pour que chacune puisse être relue,
testée et remplacée sans reprendre tout le projet.

## De la source au modèle

### Ingestion

`DataIngestion` lit un CSV local ou une collection MongoDB. Elle retire le champ `_id`,
remplace les valeurs `na` par des valeurs manquantes et conserve une copie des données
utilisées pour l’entraînement.

Le découpage s’appuie sur `StratifiedGroupKFold`, avec une graine fixée à 42. Les lignes
qui ont les mêmes 30 caractéristiques appartiennent au même groupe, quelle que soit leur
cible. Un des cinq plis est réservé au test, soit environ 20 % des lignes.

### Validation

`DataValidation` vérifie les noms exacts des 31 colonnes, leurs valeurs numériques,
l’absence d’infinis et la cible dans `{-1, 1}`. Une cible manquante ou une caractéristique
entièrement vide arrête le pipeline.

Un rapport de Kolmogorov-Smirnov compare les distributions des caractéristiques entre
l’entraînement et le test. Ce rapport sert au diagnostic ; il ne bloque pas l’entraînement.
Ses p-values ne sont pas corrigées pour les tests multiples et doivent être interprétées
avec prudence sur des variables discrètes.

### Préparation

`DataTransformation` transforme la cible `-1` en `0` et enregistre les données sous
forme de tableaux NumPy. La dernière colonne contient la cible. Les valeurs manquantes
restent présentes à ce stade : l’imputation sera apprise pendant l’entraînement.

### Sélection et évaluation

`ModelTrainer` compare cinq familles de modèles : Random Forest, arbre de décision,
Gradient Boosting, régression logistique et AdaBoost. La grille contient deux configurations
par famille.

Chaque candidat associe un imputer KNN et un classifieur dans un pipeline scikit-learn.
La validation croisée utilise trois plis, avec le même principe de regroupement des
caractéristiques identiques. Chaque pli ajuste son propre prétraitement.

Le candidat ayant le meilleur F1 moyen est retenu si son score atteint 0,6.
`GridSearchCV` le réentraîne sur toutes les données d’entraînement. Le jeu de test est
ensuite utilisé pour mesurer le F1, la précision et le rappel.

### Enregistrement et inférence

Le modèle de service est un objet `NetworkModel` qui contient le prétraitement ajusté,
le classifieur et les noms des caractéristiques. Cet objet est utilisé par l’API et la
prédiction CSV.

Les colonnes d’entrée peuvent être réordonnées, mais un champ absent ou supplémentaire
est rejeté. Le prétraitement est appliqué sans nouvel apprentissage.

## Où trouver les fichiers produits

| Emplacement | Contenu |
| --- | --- |
| `Artifacts/<run>/data_ingestion/` | Snapshot et fichiers entraînement/test |
| `Artifacts/<run>/data_validation/` | Copies validées et rapport de distribution |
| `Artifacts/<run>/data_transformation/` | Tableaux NumPy et prétraitement ajusté |
| `Artifacts/<run>/model_trainer/` | Modèle enregistré et rapport de sélection |
| `final_model/` | Modèle utilisé par l’API et métriques associées |
| `prediction_output/` | Exemples générés et prédictions CSV |
| `logs/` | Journaux d’exécution |

Ces répertoires sont exclus de Git. Le rapport `docs/results.json` conserve les résultats
mesurés et l’empreinte des données, sans publier les modèles générés.

Le fichier de service est remplacé à partir d’un fichier temporaire une fois l’évaluation
et le suivi MLflow éventuel terminés. Le rapport JSON est écrit séparément : l’ensemble
ne forme pas une transaction atomique.

## Choix techniques

| Choix | Intérêt | Limite |
| --- | --- | --- |
| Démonstration sur CSV | Exécution sans compte cloud | Données historiques statiques |
| Découpage par groupes | Aucun exemple identique entre partitions | Stratification approximative et doublons toujours pondérés |
| F1 de la classe positive | Comparaison adaptée à la classification | Coût métier des erreurs à définir |
| Imputation dans chaque pli | Prétraitement appris sans fuite de validation | KNN peut devenir coûteux sur de gros volumes |
| Modèle et prétraitement réunis | Même traitement en entraînement et en inférence | Versions Python et scikit-learn à conserver |
| Entraînement par commande | Lancement explicite d’un travail coûteux | Ordonnanceur de tâches à ajouter |
| Options MLflow et S3 | Transferts externes déclenchés à la demande | Tests sur les services réels à prévoir |

Les fichiers pickle sont des artefacts internes de confiance. L’API accepte uniquement
des CSV ; elle ne charge pas de modèle envoyé par un utilisateur. Les cellules du
tableau de résultats sont échappées avant leur affichage en HTML.

## Prochaines étapes

Pour un service de production, il faudrait ajouter l’authentification, les quotas
d’upload, le suivi des erreurs et des latences, un registre de modèles et une procédure
de retour à une version précédente. Une évaluation temporelle ou externe permettrait
aussi de mesurer la généralisation au-delà du fichier fourni.

Les 64 groupes aux cibles contradictoires demandent une revue des annotations. Leur
regroupement évite une fuite entre partitions, mais ne résout pas le désaccord des labels.

## Références

- [Validation croisée et pipelines scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Serveur de suivi MLflow](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/)
