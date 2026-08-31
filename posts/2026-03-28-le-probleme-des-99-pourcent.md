---
title: "Le problème des 99 %"
date: 2026-03-28
lang: fr
summary: "L'erreur composée sur les pipelines d'agents longs, la table de réussite à 99, 95 et 90 % par étape, et pourquoi raccourcir bat améliorer."
---

99 % de fiabilité par étape, ça sonne bien. Faites tourner vingt étapes et vous êtes à 82 %.

C'est le problème de structure des pipelines d'agents autonomes longs, et il explique la plupart des échecs qu'on met sur le dos de la capacité du modèle. Le calcul se moque du modèle que vous utilisez, l'erreur composée est une fonction de la longueur de la chaîne, pas de l'intelligence.

L'arithmétique : un pipeline de vingt étapes à 99 % de fiabilité par étape réussit de bout en bout 82 % du temps. Descendez à 95 % par étape, ce qui est déjà très bon pour des tâches d'agent réelles, et vingt étapes vous mènent à 36 %. Un pipeline sur trois se termine correctement, les autres échouent silencieusement quelque part au milieu.

---

## Pourquoi ça ne se voit pas venir

Le pipeline de démo fait cinq étapes et il marche. Le pipeline de production en fait vingt parce que les tâches de production sont plus compliquées. Ce taux d'échec est la conséquence prévisible d'une décision sur la longueur de la chaîne, et cette décision se prend le plus souvent sans faire le calcul.

Le mode de défaillance est aussi pénible à débugger. Un pipeline de vingt étapes qui échoue 18 % du temps n'échoue pas de façon constante, il casse à l'étape 7 une fois, à l'étape 14 la suivante, à l'étape 3 la troisième. Les erreurs ont l'air aléatoires mais elles sont probabilistes, l'échec est réparti le long de la chaîne au lieu d'être concentré sur une étape cassée.

Vous corrigez l'étape 7, vous relancez, ça casse à l'étape 11. Vous corrigez l'étape 11, ça casse à l'étape 4. C'est le pipeline lui-même le problème.

---

## Le calcul selon la longueur de chaîne

| Étapes | 99 % par étape | 95 % par étape | 90 % par étape |
|---|---|---|---|
| 5 | 95 % | 77 % | 59 % |
| 10 | 90 % | 60 % | 35 % |
| 20 | 82 % | 36 % | 12 % |
| 30 | 74 % | 21 % | 4 % |

À 90 % de fiabilité par étape, un pipeline de trente étapes se termine correctement 4 % du temps. C'est la longueur de la chaîne, pas la qualité du modèle.

Optimiser la fiabilité par étape en gardant la chaîne à sa longueur, c'est se battre sur le mauvais terrain. Passez la fiabilité par étape de 90 à 95 % au prix d'un effort d'ingénierie sérieux, et un pipeline de vingt étapes passe de 12 à 36 % de réussite. Ou coupez la chaîne à cinq étapes et vous êtes à 59 % sans avoir touché à la fiabilité par étape du tout, pour beaucoup moins de travail.

---

## La correction architecturale

Ni les retries ni un meilleur modèle ne règlent l'erreur composée. Des tâches plus étroites, si.

Un pipeline de vingt étapes devrait être quatre pipelines de cinq étapes avec des passations explicites entre eux. La passation est un fichier d'état, pas une chaîne de prompts. Chaque segment va au bout, écrit sa sortie, et s'arrête. Le segment suivant lit cette sortie et démarre à neuf. Si le segment 2 échoue, vous rejouez le segment 2, pas les étapes 1 à 20.

Les systèmes de CI/CD de production ont réglé ça il y a longtemps, des étapes avec des artefacts explicites entre elles, l'isolation des pannes au niveau de l'étape, des entrées et des sorties reproductibles pour chacune. Les mêmes principes s'appliquent aux pipelines d'agents pour la même raison, l'échec composé dans une longue chaîne séquentielle est un problème de structure, et l'architecture le traite mieux que la fiabilisation.

La débuggabilité y gagne aussi. Quand un segment de cinq étapes échoue, vous avez cinq étapes à examiner. Quand un pipeline de vingt étapes échoue, vous avez vingt étapes de contexte à éplucher, la panne a souvent eu lieu plusieurs étapes avant de devenir visible, et le modèle a déjà fait beaucoup de travail par-dessus un état intermédiaire corrompu.

---

## Ce que le calcul veut dire pour le design

Une chaîne autonome plus longue échange de la fiabilité contre moins de frais de passation. L'arbitrage peut se tenir pour des tâches à faible enjeu, il se tient rarement quand les échecs coûtent cher à détecter et à réparer.

Mettez un plafond dur sur le nombre d'étapes par segment. Cinq, c'est bien. Dix, c'est le maximum. Au-delà de dix, ça part en plusieurs segments avec des artefacts explicites entre eux.

Un travail compliqué découpé en plusieurs agents bornés à la suite, chacun avec une entrée claire et une sortie claire, a un profil de panne complètement différent d'un agent unique qui fait tout dans une seule context window. C'est la même quantité de travail dans les deux cas, c'est juste que l'une des deux versions arrive au bout.

Les 82 % de réussite d'un pipeline de vingt étapes à 99 % par étape ne sont pas une limite temporaire des modèles actuels, c'est de l'arithmétique. Les modèles vont devenir plus fiables par étape avec le temps, le calcul composé, lui, ne bougera pas.

Le taux par étape que vous multipliez bouge avec [le harness](/ecrits/le-modele-cest-la-partie-facile/) plus qu'avec le modèle, et la première chose qui le fait tomber est [le contexte gonflé](/ecrits/votre-agent-se-noie-dans-son-contexte/).
