# Progression du projet

Le dossier initial ne contenait pas de r?pertoire `.git`. Cet historique a ?t? cr??
pendant la pr?paration ; il ne pr?tend pas reconstituer chronologiquement les travaux
ant?rieurs. Les commits sont dat?s de leur ex?cution r?elle et publi?s par ?tapes.

1. `chore: establish project skeleton and safe configuration` : structure, d?pendances,
   environnement exemple, exclusions des fichiers g?n?r?s, Docker et workflow de qualit?.
2. `fix: make training reproducible and remove model selection leakage` : pipeline,
   sch?ma, donn?es sources, m?triques de classification et CV sans utilisation du test.
3. `feat: add documented inference API and regression tests` : API, outils de d?mo,
   tests, contrats document?s et suivi externe explicitement optionnel.
4. `fix: keep duplicate feature groups out of evaluation folds` : correction issue de
   l'audit des doublons, appliqu?e au holdout et ? la validation crois?e.
5. `docs: prepare interview walkthrough and measured validation report` : README,
   architecture, pr?sentation, limites et r?sultats mesur?s.

Les premi?res ?tapes du squelette sont incompl?tes par nature. La r?f?rence pour la
d?monstration et les v?rifications est le dernier commit de la branche `main`.
