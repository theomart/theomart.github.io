---
title: "Le modèle, c'est la partie facile"
date: 2026-03-28
lang: fr
summary: "Le scaffolding autour d'un agent déplace plus le taux de réussite que le choix du modèle, et ce qu'un harness de production doit tenir."
---

Tout le monde choisit le meilleur modèle, et ce n'est pas là que se joue la partie.

LangChain a fait tourner son agent de code sur Terminal Bench 2.0, a gardé le même modèle en dessous, gpt-5.2-codex, et n'a touché qu'à la couche autour. Le taux de tâches réussies est passé d'environ 53 % à 66 %, près de quatorze points, sans nouveaux poids et sans prompt magique. Le modèle n'a pas changé, ce qu'il y a autour, si. Je n'ai pas rejoué la mesure, je la lis chez eux, mais l'ordre de grandeur correspond à ce que je vois quand je reprends un agent qui marche mal.

Cette chose a un nom, c'est le harness. L'infrastructure entre le modèle brut et la tâche réelle : les outils auxquels l'agent a accès, la façon dont l'état survit d'une session à l'autre, ce qui se passe quand il est interrompu, quel contexte il reçoit et à quel moment. Partout où je suis passé, l'effort part dans le choix du modèle et dans l'écriture du prompt, et tout le reste ramasse ce qui traîne. Les chiffres disent que le rapport est à l'envers.

Une précision, parce que le mot harness sert à deux choses. Les harness du commerce, Claude Code, Codex, Cursor, se valent à peu près en ce moment, c'est une observation datée et pas une loi, et si l'un reprend l'avantage demain je le dirai. Justement parce qu'ils ont convergé, l'écart s'est déplacé sur ce qu'on met dedans, et c'est de ça que parle la suite.

---

## Ce qui casse vraiment en production

Quand un agent échoue, le post-mortem tombe presque toujours sur l'infrastructure et pas sur la capacité. L'agent perd le fil de ce qu'il a déjà fait. On lui envoie quarante mille tokens de prompt là où huit cents tokens ciblés suffisaient. Il n'a aucun moyen de reprendre une tâche de plusieurs heures après la fin d'une session. Il reçoit des instructions ambiguës parce que personne n'a écrit les règles du jeu.

Aucun de ces problèmes n'est un problème de modèle, un modèle plus intelligent ne les règle pas.

Celui que je rencontre le plus souvent, ce sont les agents qui tournent parfaitement en démo et qui s'effondrent quand la session se termine. Pas de contrat de reprise, pas de fichier d'état, pas de note de passation. L'agent repart de zéro à chaque fois, il redécouvre ce qui a déjà été fait, parfois il le refait, parfois il saute des étapes. Vous avez construit un agent capable et aucun système pour le garder orienté dans le temps, ce sont deux problèmes différents et un seul des deux a un rapport avec le modèle.

---

## La discipline que ça demande

Construire un harness de qualité production, ça veut dire séparer deux types de travail que la plupart des implémentations que j'ai vues mélangent : les étapes déterministes et les étapes de modèle.

Le déterministe, c'est la lecture et l'écriture de fichiers, la construction du manifest, le suivi d'état, la déduplication, la constitution des lots. Des scripts font ça. Ils sont reproductibles, ils se rejouent sans effet de bord, ils donnent la même sortie pour la même entrée. Le modèle ne touche jamais à ce travail directement.

Le travail de modèle, c'est le jugement : extraire, synthétiser, classer. Là ce sont les agents. Ils reçoivent des entrées compactes et pré-traitées, et ils produisent des sorties structurées qui vont dans des fichiers, pas dans une mémoire de conversation.

L'erreur, c'est de laisser le modèle faire le travail déterministe. Quand un agent reconstruit son manifest à chaque exécution, qu'il lit les sources brutes au lieu de résumés pré-calculés, ou qu'il reconstitue son état depuis l'historique de conversation plutôt que depuis un fichier, vous lui faites faire du ménage au tarif du modèle. Lent, cher, non reproductible. Dit comme ça la séparation paraît évidente, et je l'ai rarement vue tenue.

---

## À quoi ressemble un état durable

Un harness qui survit à une interruption a besoin de fichiers d'état, pas d'un historique de chat. C'est l'exigence d'ingénierie la plus souvent oubliée dans les systèmes d'agents, et c'est aussi la plus simple à bien faire une fois qu'on arrête de considérer la conversation comme le registre.

Trois fichiers suffisent. Un manifest, en JSON ou en JSONL, qui énumère le travail à faire, construit une fois par un script déterministe et lu par toutes les étapes suivantes, et quand une session reprend, c'est lui qu'elle lit en premier, pas la conversation d'avant. Un log d'exécution, qui enregistre quelles tâches ont tourné, ce qu'elles ont produit et quand elles ont fini, en append-only et verrouillé pour les écritures concurrentes, et quand vous voulez savoir ce qui est déjà fait, vous greppez le log. Et un fichier de prochaines étapes, lisible par un humain, un paragraphe, mis à jour à la fin de chaque étape, qui dit à la session suivante ce qui vient de tourner et ce qui doit tourner ensuite. La passation est dans le système de fichiers, pas dans la conversation.

Les sessions deviennent des workers sans état posés sur un système de fichiers durable. Chacune démarre à froid et reprend exactement là où la précédente s'est arrêtée, et la taille de la context window n'a plus rien à voir avec la continuité entre les sessions.

---

## La discipline de tokens

L'autre mode de défaillance, c'est le contexte gonflé. Un agent qui reçoit tout échoue différemment d'un agent qui ne reçoit rien, il fait du pattern matching au lieu de raisonner, il se laisse distraire par du matériau sans rapport, et il produit de moins bons résultats pour plus cher.

Le remède, ce sont les vues intermédiaires compactes. Si la source brute fait deux cents conversations, vous construisez un manifest qui en résume les métadonnées, qui, quand, quelle longueur, quel sujet à peu près. L'agent d'extraction lit le manifest, pas les conversations, et il ne va chercher un contenu précis que quand il en a besoin.

Un agent doit recevoir le minimum de contexte qui rend la tâche faisable. Construisez une passe de résumé avant la passe d'extraction, un index avant la passe de recherche. Ne donnez jamais un corpus entier à un agent en lui demandant d'y trouver des choses, il va techniquement essayer, et le résultat sera cher et instable.

---

## Ce que ça donne dans un skill

Claude Code formalise tout ça dans un skill, un fichier SKILL.md qui apprend à l'agent un mode d'emploi pour une classe de tâches. Écrire un bon skill oblige à appliquer chacun des principes au-dessus.

La description est écrite pour le déclenchement et pas pour l'exhaustivité, elle porte les conditions d'usage et de non usage, pour que l'agent sache exactement quand l'invoquer. Le fichier reste court, deux cents lignes au maximum, et si vous avez besoin de plus, vous liez des fichiers de référence au lieu de gonfler sur place. Le workflow décrit des étapes distinctes et pas un mur d'instructions.

Puis viennent les scripts, un fichier Python par étape déterministe : construire le manifest, faire les lots, empaqueter les payloads, enregistrer l'exécution. Chaque script fait une chose, prend ses chemins en argument explicite, écrit sa sortie dans des fichiers et se rejoue sans effet de bord. Le SKILL.md nomme les scripts et leur ordre, l'agent suit l'ordre.

L'architecture qui sort de cette discipline n'est pas compliquée, elle est juste rigoureuse sur ce qui va où, sur l'endroit où vit l'état, et sur la façon dont les sessions se passent le relais.

---

## La partie inconfortable

Un harness, ça se construit rarement exprès. On part d'un prompt, on ajoute quelques outils, on branche un peu de contexte, et on appelle ça un agent. Ça marche en démo. Puis ça se dégrade doucement en production à mesure que les cas particuliers s'accumulent, sans personne pour avoir une manière de principe de les corriger.

Les équipes chez qui ça tient traitent le harness comme le produit. Le modèle est une commodité qu'on loue au token, et l'infrastructure autour, les skills, la gestion d'état, la séparation des étapes, la discipline de contexte, c'est ce que vous possédez et c'est ce qui s'accumule à mesure que les pannes de production sont réintégrées dans le système.

Quatorze points de taux de réussite gagnés en changeant le scaffolding autour d'un modèle inchangé, ce n'est pas un petit chiffre, c'est la mesure de ce que le système alentour laissait sur la table. La question de la capacité des modèles est à peu près réglée, celle de l'infrastructure ne l'est pas, et c'est là qu'est le travail.

---

La discipline de contexte est la partie que je vois sautée le plus souvent, [ici](/ecrits/votre-agent-se-noie-dans-son-contexte/), et l'arithmétique qui décide si un pipeline long arrive au bout est [là](/ecrits/le-probleme-des-99-pourcent/). Si vous voulez que quelqu'un regarde votre harness, [c'est ce que je vends](/offre/).

## Sources

- LangChain, « Improving Deep Agents with harness engineering » : https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
