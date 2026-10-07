# Pr?sentation en entretien

## Pitch de 90 secondes

? Ce projet montre comment transformer un entra?nement de classification de sites web
? partir de caract?ristiques num?riques en un pipeline reproductible. Il s?pare
l'ingestion, la validation, la pr?paration des donn?es, la s?lection des mod?les et
l'inf?rence. Le mode local me permet de d?montrer le parcours complet sans cloud.

Un point cl? est la qualit? de l'?valuation : les caract?ristiques identiques restent
dans une seule partition et l'imputation est ajust?e ? l'int?rieur de chaque pli de
validation crois?e. Le mod?le est choisi sur le F1 de CV ; le test est r?serv? ?
l'?valuation finale. Le r?sultat est enregistr? avec son pr?traitement et le contrat
des colonnes, puis servi par une API FastAPI.

Le projet poss?de des tests automatis?s et une CI. MongoDB, MLflow et S3 sont des
int?grations optionnelles. Je distingue cette d?monstration d'un service de production :
le monitoring continu, l'authentification et la promotion des mod?les restent ? construire. ?

Adapter ce texte ? ce que tu sais effectivement expliquer. La base para?t p?dagogique ;
ne pas revendiquer des d?ploiements cloud ou une cr?ation enti?rement originale si ce
n'est pas ton exp?rience. Les commits refl?tent la pr?paration actuelle du projet.

## Parcours de pr?sentation de 7 minutes

| Temps | Montrer | Message |
|---|---|---|
| 0?1 min | README et probl?me | Classification sur 30 caract?ristiques ; pas un scanner d'URL |
| 1?2 min | Sch?ma et donn?es | Cibles -1/1, doublons et annotations contradictoires |
| 2?4 min | Ingestion puis entra?nement | Split/CV par groupes et imputation dans chaque pli |
| 4?5 min | `docs/results.json` | Mod?le retenu, F1 CV et test, limites de g?n?ralisation |
| 5?6 min | `/docs` puis `/predict` | M?me bundle pour entra?nement et inf?rence |
| 6?7 min | Tests et workflow | V?rifications r?elles ; ?tapes vers la production |

Pr?parer l'environnement et entra?ner avant l'entretien. G?n?rer le CSV de d?monstration,
lancer Uvicorn, garder le README et les r?sultats ouverts. Montrer une erreur 422 avec un
CSV mal form? si le temps le permet. En solution de secours, utiliser la pr?diction batch.
Les cinq exemples de d?monstration viennent des donn?es sources : ils ne constituent pas
un test ind?pendant de performance.

## Questions fr?quentes

**Pourquoi le F1 et pas R? ?**
Il s'agit d'une classification binaire. Le F1 combine pr?cision et rappel de la classe
positive. Le choix d?finitif d?pend du co?t d'un faux positif/faux n?gatif et de la
signification confirm?e des labels. Le code initial utilisait R? : cela a ?t? corrig?.

**Comment ?vites-tu les fuites de donn?es ?**
Le holdout n'intervient pas dans le choix du mod?le ; les doublons restent group?s,
y compris dans la CV ; le pr?traitement est appris uniquement sur chaque sous-ensemble
d'entra?nement. Cela ne remplace pas une ?valuation temporelle ou externe.

**Pourquoi garder les labels contradictoires ?**
La source ne fournit pas de r?gle fiable pour les d?partager. Les garder dans le m?me
groupe ?vite de les disperser entre partitions ; ils restent un probl?me d'annotation
? investiguer. Je ne les corrige pas arbitrairement.

**Pourquoi l'imputation KNN ?**
Elle reprend une approche de la base du projet et permet de traiter les valeurs
manquantes futures. Le fichier actuel n'a pas de NaN. Je comparerais en production
une imputation plus simple, un indicateur de valeurs manquantes et le co?t de KNN.

**Comment garantis-tu la coh?rence de l'inf?rence ?**
Le bundle s?rialis? contient le pr?traitement ajust?, le classifieur et les noms des
colonnes. L'API et la CLI batch utilisent ce m?me objet ; un mauvais sch?ma est rejet?.

**Qu'apporte MLflow ?**
L'int?gration journalise les m?triques, la comparaison CV et le mod?le dans un run,
uniquement si elle est demand?e. Le registre, la promotion et le d?ploiement du mod?le
ne sont pas impl?ment?s ni d?montr?s sur un serveur r?el dans cette pr?paration.

**Est-ce du monitoring de d?rive ?**
Le rapport actuel compare les distributions train/test par KS. Il s'agit d'un diagnostic
de donn?es, pas d'un suivi dans le temps. Les caract?ristiques discr?tes et les tests
multiples limitent l'interpr?tation des p-values.

**Qu'est-ce qui est test? en CI ?**
Lint et formatage, sch?ma, fronti?res de s?paration des doublons, apprentissage du
pr?traitement par pli, s?rialisation et API, puis construction de l'image Docker.
Les syst?mes MongoDB/MLflow/AWS n?cessitent des tests d'int?gration s?par?s.

**Comment ferais-tu un d?ploiement fiable ?**
Image versionn?e par commit, donn?es et mod?le versionn?s, registre avec crit?res de
promotion, tests de smoke, d?ploiement progressif, observabilit? et rollback. Ce sont
les prochaines ?tapes ; la CI actuelle ne d?ploie pas de service AWS.

## Travail ? savoir expliquer sans aide

Ex?cuter la d?mo, retracer un artefact dans les quatre ?tapes, justifier le groupement
des doublons, expliquer la diff?rence CV/test et montrer un test qui d?tecte une
r?gression. ?viter de m?moriser un score isol? : utiliser le rapport mesur? actuel.
