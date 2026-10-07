# Présenter le projet sur LinkedIn

## Rubrique « Projets »

**Titre**

Network Security — Pipeline MLOps et déploiement sur AWS

**Description**

Projet réalisé dans le cadre de mon apprentissage AWS, en complément de mes formations
Google Cloud sur le MLOps, l’évaluation des modèles et la sécurité de l’IA.

À partir d’une base pédagogique, j’ai travaillé sur un pipeline de classification de
sites web utilisant 30 caractéristiques numériques : ingestion depuis MongoDB, validation
du schéma, préparation des données et comparaison de cinq familles de modèles scikit-learn.
Le projet intègre le suivi des expériences avec MLflow sur DagsHub et l’archivage des
artefacts sur Amazon S3.

L’application expose les prédictions via FastAPI. Conteneurisée avec Docker, elle a été
publiée dans Amazon ECR et exécutée sur Amazon EC2. Un workflow GitHub Actions organise
la construction, la publication et le lancement sur un runner auto-hébergé.

La préparation récente a renforcé l’évaluation : validation croisée sur le F1,
prétraitement appris dans chaque pli et séparation des caractéristiques identiques entre
entraînement et test. La Random Forest retenue atteint un F1 de test de 0,9593.
Huit tests automatisés et la construction Docker sont vérifiés en CI.

Ce projet m’a permis de relier l’entraînement d’un modèle à sa traçabilité, à sa mise à
disposition par API et à son déploiement sur AWS.

**Compétences**

Python · scikit-learn · MLOps · MongoDB · MLflow · FastAPI · Docker · GitHub Actions ·
Amazon S3 · Amazon ECR · Amazon EC2

**Lien**

https://github.com/informatikerVonBreuf/networksecurity

## Version courte pour la rubrique « Infos »

Je développe mes compétences cloud et MLOps à travers des projets pratiques sur AWS,
en complément de formations Google Cloud en évaluation, opérations et sécurité de l’IA.

Mon projet Network Security relie l’ingestion de données MongoDB, l’entraînement
scikit-learn, le suivi MLflow, l’archivage S3 et une API FastAPI conteneurisée, déployée
avec Amazon ECR et EC2. Une relecture de l’évaluation a permis de mieux gérer les doublons
et les fuites de données ; la version corrigée atteint un F1 de test de 0,9593 et dispose
de huit tests automatisés.

## Formations à mentionner

Les intitulés visibles dans la capture sont des badges de fin de formation Google Cloud :

- Machine Learning Operations (MLOps) with Agent Platform: Model Evaluation ;
- Machine Learning Operations (MLOps): Getting Started ;
- Machine Learning Operations (MLOps) for Generative AI ;
- Model Armor: Securing AI Deployments ;
- Google Cloud Agent Governance and Security ;
- Secure Enterprise AI Agents.

Les liens de vérification individuels des badges peuvent accompagner leur ajout au profil.
Leur intitulé « Completion Badge » évite de les confondre avec une certification
professionnelle Google Cloud obtenue par examen.

## Repères pour les échanges avec un recruteur

Le déploiement ECR/EC2 correspond à l’exécution initiale confirmée par le propriétaire.
Le F1 de 0,9593 et les huit tests concernent la préparation récente du code. Le projet
n’implémente pas d’agent ou de modèle génératif, même si ces sujets font partie du parcours
de formation.
