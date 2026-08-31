---
title: "Votre agent se noie dans son contexte"
date: 2026-03-28
lang: fr
summary: "Le contexte gonflé est le mode de défaillance le moins diagnostiqué : outils chargés d'avance, corpus bruts, et les subagents comme pare-feu."
---

Le contexte gonflé est le mode de défaillance le moins diagnostiqué des systèmes d'agents. On donne à l'agent tout ce dont il pourrait avoir besoin, il n'arrive pas à retrouver la partie pertinente, il fait du pattern matching sur le mauvais signal, et il sort quelque chose de plausible et de faux. C'est le modèle qu'on accuse, et c'est le contexte qui pose problème.

Plus d'outils chargés d'avance dégrade la sélection d'outil. Plus de matériau source passé directement enterre le signal dans le bruit. Plus d'instructions dans un seul prompt et l'agent s'accroche à l'interprétation la plus probable statistiquement, pas à la bonne. Ce sont les conséquences du fait de donner trop de choses à traiter d'un coup, et ça se dégrade avec la longueur du contexte au lieu de rester proportionnel.

---

## Les outils chargés d'avance

La sélection d'outil se dégrade à mesure que le nombre d'outils disponibles augmente. Quand un modèle choisit parmi cinq outils, il raisonne sur celui qui convient. Quand il choisit parmi deux cents, il fait du pattern matching sur les noms et les descriptions. L'écart de qualité est important et il reste invisible tant qu'on ne compare pas les deux directement.

Claude Code règle ça au niveau de l'architecture avec ToolSearch, un outil d'entrée unique dont le seul travail est de charger les définitions des autres outils à la demande. L'agent démarre avec un outil, interroge ToolSearch en décrivant ce dont il a besoin, et récupère quelques définitions pertinentes. Il les a choisies pour la tâche en cours, pas parce qu'elles étaient toutes préchargées.

L'approche naïve consiste à tout charger d'avance pour que l'agent ait toujours tout sous la main. C'est ce que j'ai vu par défaut à peu près partout, et ça donne de moins bons résultats.

---

## Le corpus brut

Le même principe vaut pour le matériau source. Un agent chargé d'extraire des données structurées de deux cents conversations ne devrait pas recevoir deux cents conversations. Il devrait recevoir un manifest : des métadonnées sur ces conversations, qui elles concernent, quand elles ont eu lieu, quelle longueur, quelle catégorie de sujet. L'agent lit le manifest, repère les conversations pertinentes, et va chercher celles-là seulement, sur les passages qui l'intéressent.

C'est du travail en plus, fait une fois, par un script déterministe qui tourne vite et qui est reproductible. L'alternative c'est l'agent qui relit les deux cents conversations à chaque exécution, qui paie le contexte plein à chaque fois, qui produit des extractions instables parce que le signal utile est noyé, et sans aucun moyen de savoir quelles conversations ont réellement contribué au résultat.

Construisez une passe de résumé avant la passe d'extraction, un index avant la passe de recherche. L'artefact intermédiaire est tout l'intérêt de l'affaire, il compresse l'espace d'information pour que l'agent d'extraction reçoive une entrée bornée et pertinente au lieu du corpus brut.

---

## Les subagents comme pare-feu de contexte

L'autre outil de la discipline de tokens, c'est l'isolation par subagent. Un agent qui tourne longtemps accumule du contexte au fil de son travail, les sorties d'outils, les résultats intermédiaires, les tours de conversation précédents. Quand il arrive à la tâche quinze sur vingt, il traîne encore le contexte des tâches un à quatorze, sans rapport avec la quinzième, et le rapport signal sur bruit de sa context window s'est dégradé.

Les subagents corrigent ça en donnant à chaque tâche bornée un contexte neuf. L'agent parent passe un payload compact, les entrées de cette tâche, le schéma de sortie attendu, rien d'autre. Le subagent fait le travail, écrit sa sortie dans un fichier, et s'arrête. Son contexte disparaît. Le parent lit le fichier de sortie, pas le contexte du subagent.

Ça revient à traiter les subagents comme des pare-feu de contexte. Chacun démarre propre, fait une chose, et écrit son résultat dans un stockage durable. Le contexte accumulé du parent ne contamine jamais le travail ciblé de l'enfant, et le contexte accumulé de l'enfant ne gonfle jamais celui du parent.

Le pattern marche parce que la mémoire partagée est le système de fichiers et pas la context window. N'importe quel agent, dans n'importe quelle session, peut lire les fichiers de sortie, et aucun agent n'a besoin de porter le contexte du travail antérieur sauf s'il en a explicitement besoin.

---

## Ce que la discipline de tokens coûte vraiment

L'objection au chargement progressif et à l'isolation par subagent, c'est que ça ajoute de la complexité. Écrire un script de manifest, définir un schéma de payload pour les subagents, câbler les passations par fichiers entre les étapes, ça fait plus de travail que de tout passer à un seul agent en lui demandant de se débrouiller.

L'arbitrage est réel, et il n'est pas serré. Un agent qui se noie dans du contexte inutile ne produit pas des résultats un peu moins bons. Il produit des sorties d'apparence plausible, fausses de manière précise et non évidente, la catégorie de panne la plus difficile à attraper en review.

La discipline de tokens s'accumule aussi dans le bon sens. Un manifest construit une fois se réutilise à toutes les étapes. Un index construit une fois rend toutes les recherches suivantes moins chères. Le coût initial est payé une fois, le bénéfice revient à chaque invocation d'agent sur ces données.

L'absence de discipline s'accumule dans l'autre sens. Un agent qui relit la source brute à chaque exécution paie le contexte plein à chaque exécution, sa qualité d'extraction se dégrade à mesure que le contexte grossit, et son coût par exécution monte avec le volume de données. Il n'y a pas de plancher.

---

## La question que ça force

La discipline de tokens force une question que la plupart des designs d'agents que j'ai vus sautent : qu'est-ce que cet agent a besoin de savoir, là, maintenant.

Y répondre étape par étape produit une autre architecture que « on donne tout à l'agent ». Vous vous retrouvez avec un pipeline où chaque étape a un contrat d'information explicite avec la suivante, où chaque étape produit un artefact précis dans un format précis, et où l'étape suivante lit cet artefact et rien d'autre. Borné, reproductible, débuggable.

C'est un système différent d'un agent unique bourré de contexte, et il finit les tâches de façon fiable à l'échelle là où la version bourrée n'y arrive pas.

C'est la même conclusion que [le modèle, c'est la partie facile](/ecrits/le-modele-cest-la-partie-facile/), prise par l'autre bout, et le découpage en segments bornés a son propre calcul dans [le problème des 99 %](/ecrits/le-probleme-des-99-pourcent/). Regarder ça dans un vrai repo est [ce que je vends](/offre/).
