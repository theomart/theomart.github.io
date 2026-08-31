---
title: "Votre nouveau poste, c'est office manager d'agents"
date: 2026-03-25
lang: fr
summary: "Le plus gros de la journée autour d'un agent de code est de la plomberie, ce qui compte c'est les CLAUDE.md, les skills et les connecteurs."
---

Le copier-coller entre l'IA et vos outils n'a pas disparu, il a changé de place.

Je fais tourner jusqu'à neuf sessions Claude Code en parallèle, sur des worktrees séparés, et l'essentiel de ma journée ne se passe ni à prompter ni à coder, il se passe à rendre l'environnement utilisable. Coller des messages Slack dans Claude parce que le connecteur n'est pas validé. Télécharger des pages Notion pour les remettre dans le contexte parce qu'il n'y a pas d'intégration. Recopier des logs de CI à la main parce que la sortie de l'étape noie la context window. Renouveler des tokens d'API expirés parce que personne n'a mis de rotation en place. Cliquer sur approuver quarante fois par jour. L'agent réfléchit, moi je fais la plomberie.

Quand quelque chose casse, je ne le répare pas une fois, je le répare pour la fois d'après. La sortie de CircleCI est trop verbeuse, j'écris un skill qui la filtre avant que l'agent charge tout. L'agent gère mal un test qui échoue, j'ajoute les instructions pour qu'il sache quoi faire avant de se cogner au mur. J'ai essayé de lui dire que quand un skill échoue, il n'a qu'à réécrire le skill lui-même, il a essayé, il est devenu verbeux, il a produit des instructions boursouflées et il a tourné en rond, donc je reprends les skills à la main. La boucle d'auto-amélioration, c'est moi. Ça s'améliore quand même, les agents commencent à comprendre leur propre outillage et l'écart se réduit.

La partie qui a le plus de valeur dans mon travail en ce moment n'est rien de tout ça. C'est d'écrire les CLAUDE.md qui posent les conventions, d'affiner les skills, de configurer les outils, de pousser pour que les connecteurs finissent par être validés, d'indexer la doc interne pour que les agents la trouvent. Rendre accessible à l'IA ce qui n'était accessible qu'aux humains, et parfois ça veut juste dire exporter une page Notion parce que l'intégration n'existe pas encore.

Les équipes chez qui ça marche ont monté le bureau d'abord. Stripe donne à chaque agent une VM isolée, sans accès à internet ni à la prod, ce qui leur enlève l'approbation manuelle du chemin, et ils annoncent plus de mille PR par semaine. Je le lis dans leur propre billet et pas de l'intérieur, donc à prendre pour ce que c'est, mais ce qu'ils décrivent est cohérent avec ce que je vois : le modèle n'était pas la partie dure, le workspace l'était.

Le métier est là maintenant, construire l'endroit où les agents peuvent travailler sans vous dans la pièce. Tant que le connecteur Slack n'est pas validé, vous en êtes encore à copier-coller les points d'avancement.

---

Rien de tout ça ne se joue sur le modèle, ça se joue sur [le scaffolding autour](/ecrits/le-modele-cest-la-partie-facile/), et sur ce que vous donnez à lire à l'agent avant qu'il commence, ce qui est [le problème le moins diagnostiqué](/ecrits/votre-agent-se-noie-dans-son-contexte/) que je croise.

## Sources

- TechCrunch, « Vibe coding turned senior devs into AI babysitters » (septembre 2025) : https://techcrunch.com/2025/09/14/vibe-coding-has-turned-senior-devs-into-ai-babysitters-but-they-say-its-worth-it/
- Ethan Mollick, « Management as AI Superpower » : https://www.oneusefulthing.org/p/management-as-ai-superpower
- Addy Osmani, « The 80% Problem in Agentic Coding » : https://addyo.substack.com/p/the-80-problem-in-agentic-coding
- Silas Reinagel, « Your Job Is to Build the Workspace » (janvier 2026) : https://www.silasreinagel.com/ai/agents/ai-engineering/productivity/automation/2026/01/16/your-job-is-to-build-the-workspace/
- Stripe Minions : https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- DoltHub, « How I Use Multiple Agents in Parallel » : https://www.dolthub.com/blog/2025-08-28-how-i-use-multiple-agents-in-parallel/
- HBR, « To Thrive in the AI Era, Companies Need Agent Managers » (février 2026) : https://hbr.org/2026/02/to-thrive-in-the-ai-era-companies-need-agent-managers
