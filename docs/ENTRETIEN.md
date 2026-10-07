# Présenter le projet en entretien

L’objectif est de montrer le parcours des données jusqu’à la prédiction, puis de
justifier les choix qui rendent l’évaluation fiable.

## Présentation courte

> Le projet porte sur la classification de sites web à partir de 30 caractéristiques
> numériques. Le pipeline charge les données, vérifie leur schéma, compare plusieurs
> modèles et enregistre le modèle retenu avec son prétraitement.
>
> La partie la plus importante est l’évaluation. Le jeu contient beaucoup de doublons ;
> je les garde dans le même groupe pour qu’un exemple identique ne se retrouve pas en
> entraînement et en test. L’imputation est également apprise à l’intérieur de chaque
> pli de validation croisée. Le modèle est choisi sur le F1 de validation, puis évalué
> sur le jeu de test réservé.
>
> Le résultat est utilisé par une API FastAPI et une commande de prédiction CSV.
> La CI vérifie le code, les tests et la construction Docker. MongoDB, MLflow et S3
> sont prévus comme intégrations optionnelles.

## Démonstration en sept minutes

| Temps | Support | Point à expliquer |
| --- | --- | --- |
| 0 à 1 min | README | Le problème et les 30 caractéristiques d’entrée |
| 1 à 2 min | Schéma et données | Encodage de la cible, doublons et annotations contradictoires |
| 2 à 4 min | Ingestion et entraînement | Découpage par groupes et prétraitement dans les plis |
| 4 à 5 min | Rapport de résultats | F1 de validation croisée et F1 sur le test |
| 5 à 6 min | API | Charger un CSV et lire la réponse |
| 6 à 7 min | Tests et GitHub Actions | Ce qui est vérifié et ce qui reste à construire |

Avant l’entretien, installer les dépendances, entraîner le modèle et lancer l’API.
Garder `examples/predict.csv` prêt à charger. La commande de prédiction CSV permet
de poursuivre la démonstration si le navigateur pose problème.

## Questions à préparer

### Pourquoi choisir le F1 ?

Le projet traite une classification binaire. Le F1 combine la précision et le rappel
de la classe positive. Le choix final d’une métrique dépendrait du coût d’un faux
positif et d’un faux négatif, ainsi que du sens confirmé des labels.

R² est une métrique de régression ; son utilisation dans la version initiale a été
remplacée par une comparaison sur le F1.

### Comment éviter les fuites de données ?

Trois précautions sont appliquées : réserver le test jusqu’à l’évaluation finale,
garder les exemples identiques dans un seul groupe et ajuster le prétraitement à
l’intérieur de chaque pli. Une évaluation sur une autre source reste nécessaire
pour tester la généralisation.

### Pourquoi conserver les labels contradictoires ?

La source ne donne pas de règle fiable pour départager ces annotations. Les corriger
au hasard ajouterait une hypothèse non vérifiée. Le code les garde ensemble dans les
partitions et le rapport signale les 64 groupes concernés.

### Pourquoi utiliser une imputation KNN ?

Ce choix reprend le prétraitement de la base pédagogique et permet de traiter des
valeurs manquantes. Le CSV fourni n’en contient pas. Une comparaison avec une imputation
simple serait utile avant de traiter davantage de données.

### Comment assurer la cohérence des prédictions ?

Le prétraitement ajusté et le classifieur sont enregistrés ensemble. L’API et la
commande CSV chargent le même objet et vérifient les colonnes d’entrée. Elles ne
réajustent pas le prétraitement sur les nouvelles données.

### Que fait l’intégration MLflow ?

Avec l’option `--track-mlflow`, elle enregistre les métriques, les scores de validation
croisée et le modèle dans un run. Le registre de modèles et la promotion automatique
restent à ajouter. Cette intégration n’a pas été testée sur un serveur réel pendant
la préparation.

### Le rapport KS constitue-t-il un suivi de dérive ?

Il compare les distributions de l’entraînement et du test à un instant donné.
Un suivi en production demanderait de conserver les distributions des nouvelles
entrées et de les comparer dans le temps. Les p-values actuelles ont aussi des limites
sur les variables discrètes et les tests multiples.

### Que vérifie la CI ?

Le formatage, le lint, huit tests et la construction de l’image Docker. Les tests
couvrent le schéma, la séparation des doublons, le prétraitement dans les plis,
la sérialisation et les réponses de l’API.

### Comment passer à un déploiement de production ?

Versionner l’image et le modèle, définir des critères de promotion, ajouter
l’authentification et les quotas, puis surveiller les erreurs et les performances.
Une procédure de retour au modèle précédent serait également nécessaire.

## Repères pour la discussion

Le modèle retenu est une Random Forest : **F1 de test 0,9593** et **F1 moyen de CV 0,9544**.
Ces scores concernent les données fournies, pas des sites récents évalués en conditions
réelles. Le fichier de démonstration sert à montrer une prédiction, pas à prouver la
performance du modèle.

Le projet part d’une base pédagogique associée à Krish Naik. Pour parler des contributions,
s’appuyer sur les changements visibles dans l’historique : correction de l’évaluation,
gestion des doublons, API, tests et documentation.
