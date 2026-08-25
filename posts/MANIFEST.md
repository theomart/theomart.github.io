# MANIFEST, contenu de `posts/`

Document de contrôle, hors publication. `build.py` doit ignorer ce fichier (il n'a pas de front matter, donc il ne devrait pas être ramassé, mais autant l'exclure explicitement).

État : 53 fichiers publiables dans `posts/`, soit 40 anciens posts migrés, 9 articles récents sélectionnés en anglais et 4 réécritures françaises de quatre d'entre eux.

---

## 1. Les anciens posts migrés

40 fichiers sur les 41 `.markdown` que contenait `_posts/` (`TEMPLATE.md` n'est pas un post, il n'a pas été compté). Conversion de format seulement : le corps est repris caractère pour caractère, sans correction de style, d'emoji ni de faute. Rien n'a été écarté pour cause de NDA ou de contenu personnel, aucun de ces 41 fichiers ne touche à la mission sous NDA ni à quoi que ce soit de privé, ils sont tous antérieurs et tous techniques.

### Le champ `legacy_url`, à lire avant de générer les redirections

Le brief supposait que la plupart des posts avaient `categories: jekyll update`. **C'est l'inverse.** 39 posts sur 40 portent `categories: thoughts` et servent donc à `/thoughts/AAAA/MM/JJ/slug.html`. Un seul, `colbert`, porte `jekyll update` et sert à `/jekyll/update/2024/08/26/colbert.html`.

Le permalien a été reconstruit à partir du modèle Jekyll par défaut (`/:categories/:year/:month/:day/:title.html`), vérifié post par post : `_config.yml` ne redéfinit aucun `permalink`, le thème est `minima` qui ne le surcharge pas, et pour les 40 fichiers la date du front matter est identique à celle du nom de fichier, donc aucun décalage possible entre les deux.

### Titres, retitrés

Le champ `title` de l'import Jekyll était un titre tronqué, pas un titre. L'import LinkedIn coupait la première ligne du post à 60 caractères, retours à la ligne compris, et le résultat a été repris tel quel dans le blog Jekyll.

**Le compte réel est 32, pas 7.** Sept posts portaient en plus un retour à la ligne dans le champ, ce que la migration a normalisé, mais la troncature elle-même touche 32 des 40 titres. La mesure est nette : les 32 titres coupés font entre 55 et 60 caractères, les 8 titres intacts en font 53 ou moins, et aucun ne tombe entre les deux. Les 8 intacts sont `ocr-just-got-better`, `dont-trust-ai-experts`, `hugging-face-was-a-sassy-chatbot`, `gaugan2`, `to-train-a-classifier`, `takeways-from-the-mixtral-paper`, `colbert` et `if-you-are-looking-for-a-product-manager`.

Les 32 titres coupés ont été réécrits à partir du corps de chaque post, courts et descriptifs, en anglais comme les posts. **Seul le champ `title` a été touché.** Le corps, la date, le `legacy_url` et le nom de fichier sont inchangés, donc les URLs publiques ne bougent pas. Les `summary` ont été relus au passage : aucun n'avait été contaminé par le titre cassé, ils avaient été écrits depuis le corps, aucun n'a eu besoin d'être corrigé.

Les 8 titres intacts gardent leurs coquilles d'origine, « Dont trust AI experts », « Takeways from the Mixtral paper », « GauGAN2, NVIDIAs model ». Elles viennent des posts LinkedIn eux-mêmes et ne sont pas un artefact de migration, les corriger serait une décision éditoriale à part. **À trancher par Theo.**

#### Les 32 titres réécrits

| Ancien titre, coupé | Nouveau titre |
|---|---|
| Some Friday AI fun Can a gorilla ride a camel? This is the | Can a gorilla ride a camel? |
| Machine learning uses optimization, but in a slightly differ | Machine learning is not classical optimization |
| The most impactful artists of tomorrow will be the ones who | The artists of tomorrow will navigate latent space |
| 1 No product that has been called AI as of today is intellig | Intelligence is the ability to generalize |
| A human brain requires less data to be trained on a given ta | Humans only look more sample efficient than neural nets |
| ReLU is so dominant in the field because it embraces the fac | Why ReLU dominates |
| Learning rate schedules allow for changing the learning rate | Learning rate schedules, explained with a radar |
| Leetcode style coding interviews are great because - They al | What Leetcode interviews get right, and what they don't |
| Meta AI published a blogpost titled Using AI to bring childr | Meta AI animates children's drawings |
| One cool idea behind deep learning is the manifold hypothesi | The manifold hypothesis, explained with a shoelace |
| One way a project that was supposed to bring big money ends | How a point estimate turns a project into a loss |
| Mathematical intuition is an amazing tool, but it has its li | Good intuition cannot be handed to you |
| A lot of people, when they hear that we are using logarithm | The logarithm is not a hack |
| Token facts cheat sheet for practical estimations Tokens | Token facts cheat sheet |
| We often talk about the sample efficiency of ML models and | The sample efficiency comparison is unfair |
| Amazing read by M Waleed Kadous from Anyscale httpslnkd | Numbers every LLM developer should know |
| How do we get LLMs to know what a software bug is without m | A non technical dive into alignment |
| What you need to know about Groq and LPUs How can Groq run L | Groq and LPUs, why they run LLMs faster |
| Did you know? Cosmic rays is one of the greatest threat to | Cosmic rays can make your LLM training fail |
| Amazing post by Yi Tay about the challenges of training LLM | Training LLMs from scratch as a startup |
| Anyscale again! They built a FREE model comparator, where yo | A free comparator for open source LLMs |
| How do you continue training on an already pre trained LLM | Continual pretraining instead of retraining from scratch |
| Some takeaways I got from the conversation between Lex Frid | Takeaways from Lex Fridman's interview with Sam Altman |
| New model from Mistral AI Mistral Large! TLDR - Second bes | Mistral AI releases Mistral Large |
| TLDRs on Googles Gemma, spoiler dont use Gemma 7B yet? N | Google's Gemma, don't use the 7B yet |
| The AI product market is overcrowdednot with effective tool | The AI market is crowded with promises, not products |
| Developers who dont use AI-assisted coding are already falli | Developers who don't use AI assisted coding are falling behind |
| 18 lessons to develop better products using LLMs - Use n | 18 lessons for building products on LLMs |
| People saying with AI you take 3 min to generate code and 2 | Three minutes to generate, two hours to debug |
| You should encourage employees to wear Meta glasses to captu | Tribal knowledge never reaches the coding agent |
| Qwen releases QwQ-32B, small reasoning model which rivals wi | Qwen releases QwQ-32B |
| Rewriting from scratch is increasingly viable due to AI-assi | Rewriting from scratch is becoming viable |


### Résumés

Le champ `summary` n'existait dans aucun original, il est écrit ici, en anglais comme les posts, descriptif, 160 caractères maximum, vérifié par assertion sur les 53 fichiers, les quatre français compris.

### Liste

| Date | Titre | Fichier | `legacy_url` |
|---|---|---|---|
| 2020-07-30 | Can a gorilla ride a camel? | `2020-07-30-some-friday-ai-fun-can-a-gorilla-ride-a-camel-this-is-the.md` | `/thoughts/2020/07/30/some-friday-ai-fun-can-a-gorilla-ride-a-camel-this-is-the.html` |
| 2022-07-02 | Machine learning is not classical optimization | `2022-07-02-machine-learning-uses-optimization-but-in-a-slightly-differ.md` | `/thoughts/2022/07/02/machine-learning-uses-optimization-but-in-a-slightly-differ.html` |
| 2022-07-08 | GauGAN2, NVIDIAs model keeps amazing me | `2022-07-08-gaugan2-nvidias-model-keeps-amazing-me.md` | `/thoughts/2022/07/08/gaugan2-nvidias-model-keeps-amazing-me.html` |
| 2022-07-12 | The artists of tomorrow will navigate latent space | `2022-07-12-the-most-impactful-artists-of-tomorrow-will-be-the-ones-who.md` | `/thoughts/2022/07/12/the-most-impactful-artists-of-tomorrow-will-be-the-ones-who.html` |
| 2022-07-15 | Intelligence is the ability to generalize | `2022-07-15-1-no-product-that-has-been-called-ai-as-of-today-is-intellig.md` | `/thoughts/2022/07/15/1-no-product-that-has-been-called-ai-as-of-today-is-intellig.html` |
| 2022-07-16 | Humans only look more sample efficient than neural nets | `2022-07-16-a-human-brain-requires-less-data-to-be-trained-on-a-given-ta.md` | `/thoughts/2022/07/16/a-human-brain-requires-less-data-to-be-trained-on-a-given-ta.html` |
| 2022-07-24 | To train a classifier, you need a dataset | `2022-07-24-to-train-a-classifier-you-need-a-dataset.md` | `/thoughts/2022/07/24/to-train-a-classifier-you-need-a-dataset.html` |
| 2022-07-26 | Why ReLU dominates | `2022-07-26-relu-is-so-dominant-in-the-field-because-it-embraces-the-fac.md` | `/thoughts/2022/07/26/relu-is-so-dominant-in-the-field-because-it-embraces-the-fac.html` |
| 2022-08-02 | Learning rate schedules, explained with a radar | `2022-08-02-learning-rate-schedules-allow-for-changing-the-learning-rate.md` | `/thoughts/2022/08/02/learning-rate-schedules-allow-for-changing-the-learning-rate.html` |
| 2022-08-09 | What Leetcode interviews get right, and what they don't | `2022-08-09-leetcode-style-coding-interviews-are-great-because-they-al.md` | `/thoughts/2022/08/09/leetcode-style-coding-interviews-are-great-because-they-al.html` |
| 2022-08-17 | Meta AI animates children's drawings | `2022-08-17-meta-ai-published-a-blogpost-titled-using-ai-to-bring-childr.md` | `/thoughts/2022/08/17/meta-ai-published-a-blogpost-titled-using-ai-to-bring-childr.html` |
| 2022-08-19 | The manifold hypothesis, explained with a shoelace | `2022-08-19-one-cool-idea-behind-deep-learning-is-the-manifold-hypothesi.md` | `/thoughts/2022/08/19/one-cool-idea-behind-deep-learning-is-the-manifold-hypothesi.html` |
| 2023-07-06 | How a point estimate turns a project into a loss | `2023-07-06-one-way-a-project-that-was-supposed-to-bring-big-money-ends.md` | `/thoughts/2023/07/06/one-way-a-project-that-was-supposed-to-bring-big-money-ends.html` |
| 2023-07-25 | Good intuition cannot be handed to you | `2023-07-25-mathematical-intuition-is-an-amazing-tool-but-it-has-its-li.md` | `/thoughts/2023/07/25/mathematical-intuition-is-an-amazing-tool-but-it-has-its-li.html` |
| 2023-07-31 | The logarithm is not a hack | `2023-07-31-a-lot-of-people-when-they-hear-that-we-are-using-logarithm.md` | `/thoughts/2023/07/31/a-lot-of-people-when-they-hear-that-we-are-using-logarithm.html` |
| 2024-06-21 | Token facts cheat sheet | `2024-06-21-token-facts-cheat-sheet-for-practical-estimations-tokens.md` | `/thoughts/2024/06/21/token-facts-cheat-sheet-for-practical-estimations-tokens.html` |
| 2024-06-25 | The sample efficiency comparison is unfair | `2024-06-25-we-often-talk-about-the-sample-efficiency-of-ml-models-and.md` | `/thoughts/2024/06/25/we-often-talk-about-the-sample-efficiency-of-ml-models-and.html` |
| 2024-07-01 | Numbers every LLM developer should know | `2024-07-01-amazing-read-by-m-waleed-kadous-from-anyscale-httpslnkd.md` | `/thoughts/2024/07/01/amazing-read-by-m-waleed-kadous-from-anyscale-httpslnkd.html` |
| 2024-07-09 | A non technical dive into alignment | `2024-07-09-how-do-we-get-llms-to-know-what-a-software-bug-is-without-m.md` | `/thoughts/2024/07/09/how-do-we-get-llms-to-know-what-a-software-bug-is-without-m.html` |
| 2024-07-12 | Groq and LPUs, why they run LLMs faster | `2024-07-12-what-you-need-to-know-about-groq-and-lpus-how-can-groq-run-l.md` | `/thoughts/2024/07/12/what-you-need-to-know-about-groq-and-lpus-how-can-groq-run-l.html` |
| 2024-07-15 | OCR just got better | `2024-07-15-ocr-just-got-better.md` | `/thoughts/2024/07/15/ocr-just-got-better.html` |
| 2024-07-23 | Takeways from the Mixtral paper with no chitchat | `2024-07-23-takeways-from-the-mixtral-paper-with-no-chitchat.md` | `/thoughts/2024/07/23/takeways-from-the-mixtral-paper-with-no-chitchat.html` |
| 2024-07-24 | Cosmic rays can make your LLM training fail | `2024-07-24-did-you-know-cosmic-rays-is-one-of-the-greatest-threat-to.md` | `/thoughts/2024/07/24/did-you-know-cosmic-rays-is-one-of-the-greatest-threat-to.html` |
| 2024-07-24 | Hugging Face was a sassy chatbot | `2024-07-24-hugging-face-was-a-sassy-chatbot.md` | `/thoughts/2024/07/24/hugging-face-was-a-sassy-chatbot.html` |
| 2024-07-28 | If you are looking for a product manager, here is one | `2024-07-28-if-you-are-looking-for-a-product-manager-here-is-one.md` | `/thoughts/2024/07/28/if-you-are-looking-for-a-product-manager-here-is-one.html` |
| 2024-07-29 | Training LLMs from scratch as a startup | `2024-07-29-amazing-post-by-yi-tay-about-the-challenges-of-training-llm.md` | `/thoughts/2024/07/29/amazing-post-by-yi-tay-about-the-challenges-of-training-llm.html` |
| 2024-08-08 | A free comparator for open source LLMs | `2024-08-08-anyscale-again-they-built-a-free-model-comparator-where-yo.md` | `/thoughts/2024/08/08/anyscale-again-they-built-a-free-model-comparator-where-yo.html` |
| 2024-08-09 | Continual pretraining instead of retraining from scratch | `2024-08-09-how-do-you-continue-training-on-an-already-pre-trained-llm.md` | `/thoughts/2024/08/09/how-do-you-continue-training-on-an-already-pre-trained-llm.html` |
| 2024-08-09 | Takeaways from Lex Fridman's interview with Sam Altman | `2024-08-09-some-takeaways-i-got-from-the-conversation-between-lex-frid.md` | `/thoughts/2024/08/09/some-takeaways-i-got-from-the-conversation-between-lex-frid.html` |
| 2024-08-10 | Mistral AI releases Mistral Large | `2024-08-10-new-model-from-mistral-ai-mistral-large-tldr-second-bes.md` | `/thoughts/2024/08/10/new-model-from-mistral-ai-mistral-large-tldr-second-bes.html` |
| 2024-08-15 | Google's Gemma, don't use the 7B yet | `2024-08-15-tldrs-on-googles-gemma-spoiler-dont-use-gemma-7b-yet-n.md` | `/thoughts/2024/08/15/tldrs-on-googles-gemma-spoiler-dont-use-gemma-7b-yet-n.html` |
| 2024-08-19 | The AI market is crowded with promises, not products | `2024-08-19-the-ai-product-market-is-overcrowdednot-with-effective-tool.md` | `/thoughts/2024/08/19/the-ai-product-market-is-overcrowdednot-with-effective-tool.html` |
| 2024-08-26 | ColBERT: Contextualized Late Interaction over BERT | `2024-08-26-colbert.md` | `/jekyll/update/2024/08/26/colbert.html` |
| 2024-08-30 | Dont trust AI experts | `2024-08-30-dont-trust-ai-experts.md` | `/thoughts/2024/08/30/dont-trust-ai-experts.html` |
| 2024-09-21 | Developers who don't use AI assisted coding are falling behind | `2024-09-21-developers-who-dont-use-ai-assisted-coding-are-already-falli.md` | `/thoughts/2024/09/21/developers-who-dont-use-ai-assisted-coding-are-already-falli.html` |
| 2024-10-09 | 18 lessons for building products on LLMs | `2024-10-09-18-lessons-to-develop-better-products-using-llms-use-n.md` | `/thoughts/2024/10/09/18-lessons-to-develop-better-products-using-llms-use-n.html` |
| 2025-02-05 | Three minutes to generate, two hours to debug | `2025-02-05-people-saying-with-ai-you-take-3-min-to-generate-code-and-2.md` | `/thoughts/2025/02/05/people-saying-with-ai-you-take-3-min-to-generate-code-and-2.html` |
| 2025-03-01 | Tribal knowledge never reaches the coding agent | `2025-03-01-you-should-encourage-employees-to-wear-meta-glasses-to-captu.md` | `/thoughts/2025/03/01/you-should-encourage-employees-to-wear-meta-glasses-to-captu.html` |
| 2025-03-17 | Qwen releases QwQ-32B | `2025-03-17-qwen-releases-qwq-32b-small-reasoning-model-which-rivals-wi.md` | `/thoughts/2025/03/17/qwen-releases-qwq-32b-small-reasoning-model-which-rivals-wi.html` |
| 2025-03-31 | Rewriting from scratch is becoming viable | `2025-03-31-rewriting-from-scratch-is-increasingly-viable-due-to-ai-assi.md` | `/thoughts/2025/03/31/rewriting-from-scratch-is-increasingly-viable-due-to-ai-assi.html` |

### Le seul ancien post non migré

`_posts/2024-09-03-ai-experts.markdown` n'a pas été migré. Ce n'est pas une décision NDA ni une décision de contenu personnel, c'est un fichier de travail :

- il n'a aucun front matter, donc pas de `title`, pas de `date`, pas de `categories` ;
- son corps est la même tribune empilée trois fois, trois brouillons successifs de « Don't trust AI experts » collés à la suite, avec des chiffres contradictoires d'une version à l'autre (« bottom 20% » puis « bottom 30% », « >50k people » puis « >10M people »), puis un quatrième bloc de 600 mots d'un ton complètement différent ;
- la version aboutie de ce même texte est publiée le 2024-08-30 sous `dont-trust-ai-experts`, et elle est migrée.

Jekyll le rendait probablement quand même, à `/2024/09/03/ai-experts.html`, avec un titre auto-généré « Ai Experts », mais sans layout et sans lien entrant plausible (il ne vient pas de LinkedIn, il n'a pas de `linkedin_urn`, il ressemble à un fichier commité par accident).

Le publier tel quel donnerait une page publique avec trois brouillons du même texte à la suite. Le nettoyer serait le réécrire, ce que le brief interdit. **Décision à confirmer par Theo :** soit on le laisse tomber, soit on ajoute une redirection `/2024/09/03/ai-experts.html` vers `2024-08-30-dont-trust-ai-experts` par sécurité. C'est la deuxième option qui semble la plus propre.

### Les hashtags LinkedIn, traités côté build

Trois posts migrés contiennent le bloc de hashtags LinkedIn en fin de texte, sous la forme d'une ligne `hashtag` suivie d'une ligne `#machinelearning`. Le corps est repris tel quel, donc ces lignes sont là, et Python-Markdown, contrairement à CommonMark, n'exige pas d'espace après le `#` pour un titre ATX, donc elles seraient rendues en `<h1>`.

La liste a été revérifiée sur les 40 posts, elle est complète, il n'y en a pas d'autres et aucune de ces lignes n'apparaît ailleurs dans le dépôt de posts. Dix lignes en tout, dans trois fichiers :

| Fichier | Lignes |
|---|---|
| `2022-07-02-machine-learning-uses-optimization-but-in-a-slightly-differ.md` | 26 `#machinelearning`, 28 `#optimization` |
| `2022-07-16-a-human-brain-requires-less-data-to-be-trained-on-a-given-ta.md` | 30 `#intelligence`, 32 `#agi`, 34 `#ai`, 36 `#artificialintelligence`, 38 `#humanvsai` |
| `2023-07-25-mathematical-intuition-is-an-amazing-tool-but-it-has-its-li.md` | 26 `#mathematics`, 28 `#education`, 30 `#learning` |

Les lignes `hashtag` nues qui les précèdent portent les numéros impairs correspondants, elles se rendent en paragraphe et ne posent pas de problème.

`build.py` traite le cas avec `escape_lone_hashes()`, qui échappe un `#` de début de ligne non suivi d'un espace, hors blocs de code. Le contenu n'est pas touché, ce qui est la règle. Rien à faire de plus ici.

---

## 2. Les articles récents sélectionnés

9 articles, tous en anglais, tous issus de `content/articles/`. Front matter réduit à `title`, `date`, `lang`, `summary`, sans `source` ni `legacy_url` puisqu'ils n'ont jamais été publiés.

**Dates.** Le dépôt ne donne pas de date de rédaction utilisable : tout `content/` a été commité d'un bloc le 2026-04-25 (« Ajoute la matiere markdown non commitee du depot »). La date retenue est donc celle du fichier, 2026-03-28 pour les cinq articles de la famille harness et 2026-03-25 pour les quatre autres. Ces dates sont cohérentes avec le contenu, l'article sur l'office manager cite une source HBR de février 2026 et le guide navigateurs parle de « March 2026 » dans son texte.

**Nettoyage appliqué.** Le titre H1 en tête de corps a été retiré partout, puisque le gabarit `post.html` rend déjà `{{ post_title }}` et qu'un H1 dupliqué casserait la hiérarchie. Sinon : la note de fin de brouillon de `agent-harness` (« Other angles worth their own pieces… ») a été supprimée, et sur l'article office manager le titre en clair, le séparateur et l'emoji 🤖 de tête, qui sont du formatage LinkedIn. Aucun paragraphe n'a été réécrit. Les sections `## Sources` et les lignes de sources ont été gardées, ce sont du contenu et elles portent la réserve sur ce qui n'est pas de première main.

| Fichier | Source | Pourquoi |
|---|---|---|
| `2026-03-28-the-model-is-the-easy-part.md` | `articles/agent-harness/article.md` | Le texte fondateur de l'offre : le harness compte plus que le modèle. Tient debout seul, ne dépend d'aucun post. Dit exactement la position datée du brief, les modèles se valent, l'écart s'est déplacé sur ce qu'on met autour. |
| `2026-03-28-your-agent-isnt-confused-its-drowning.md` | `articles/token-discipline/article.md` | La discipline de tokens, en entier : outils chargés d'avance, corpus bruts, subagents comme pare-feu de contexte. C'est un des mots-clés de l'offre. |
| `2026-03-28-every-agent-works-in-the-demo.md` | `articles/demo-vs-production-agents/article.md` | Ce qui casse entre la démo et la production, avec le test concret qui le révèle. Sujet listé nommément dans le brief. |
| `2026-03-28-the-99-percent-problem.md` | `articles/agent-pipeline-math/article.md` | Le calcul d'erreur composée sur les pipelines longs. Arithmétique, donc insensible au passage des modèles, c'est le plus durable des neuf. |
| `2026-03-28-most-skill-md-files-work-once.md` | `articles/claude-code-skills-guide/article.md` | L'entretien du harness au niveau d'un artefact concret. Le mot Claude Code n'apparaît ni dans le titre ni dans le corps, seul SKILL.md est nommé, ce qui reste du côté harness et pas du côté visite guidée de doc. |
| `2026-03-25-your-new-job-title-is-ai-office-manager.md` | `articles/agent-secretary-paradox/article-v7.md` | Le seul de première main et à la première personne, et de loin celui qui sert le mieux le positionnement : la valeur est dans les CLAUDE.md, les skills et les connecteurs, pas dans le prompt. C'est bien la v7, la dernière, les v2 à v6 sont dans `_drafts/`. |
| `2026-03-25-the-context-envelope.md` | `articles/context-envelope/full-article.md` | Le plus long et le plus opérationnel, écrit en première personne à partir d'apps en production, avec les pièges de cache, d'injection et de budget de tokens. Sert la mémoire et le contexte des agents. |
| `2026-03-25-the-mcp-paradox.md` | `articles/the-mcp-paradox.md` | Le long format du lot. Sa thèse est celle de l'offre : la contrainte n'est pas l'accès aux outils, c'est l'attention. Voir la réserve plus bas. |
| `2026-03-25-typescript-vs-javascript-for-ai-agents.md` | `articles/typescript-vs-javascript-agents/article-v4.md` | La boucle de retour que l'agent peut fermer tout seul, donc du harness sous un autre angle. v4 est la dernière version longue, v3 et v5 à v8 sont des découpes LinkedIn du même texte. |

### Réserves sur deux des neuf

**`the-mcp-paradox`.** C'est le seul écrit à la troisième personne, sur un ton de reportage, et il empile beaucoup d'affirmations de seconde main énoncées sans réserve, ce qui n'est pas la règle de voix du dépôt. Sa chronologie s'arrête en décembre 2025, donc il se lit en août 2026 comme une rétrospective qui s'arrête huit mois trop tôt, mais sa leçon de fond est toujours vraie et la date affichée fait le travail de cadrage. Il cite Opus 4 et Opus 4.5 dans des chiffres de benchmark, ce qui va vieillir. À garder ou à couper d'un mot.

**`typescript-vs-javascript-for-ai-agents`.** Les chiffres (2-3 % contre 8-12 % de régressions, 33 000 tokens contre 188 000) sont de seconde main et donnés à plat. La ligne de sources en fin d'article les couvre en partie. Rien de faux repéré, mais c'est le genre de chiffre qu'un CTO va vouloir sourcer.

---

## 2 bis. Les quatre articles français

Le site a le français en langue primaire mais les 49 articles publiables étaient tous en anglais, donc `/ecrits/` serait sorti vide alors que l'accueil et la page à propos y renvoient. Quatre des neuf articles récents ont été réécrits en français, pas traduits : même thèse, mêmes exemples, même structure, texte refait dans la voix du dépôt, franglais du métier conservé, phrases jointes par des virgules, chiffres arrondis.

Chaque version française a un slug distinct de l'anglaise, donc les deux vivent côte à côte sans s'écraser, `/ecrits/<slug-fr>/` et `/en/writing/<slug-en>/`. La date de l'article anglais est conservée. Front matter réduit à `title`, `date`, `lang: fr`, `summary`.

| Fichier français | Article anglais repris | Pourquoi celui-là devant un CTO de scale-up |
|---|---|---|
| `2026-03-25-office-manager-dagents.md` | `your-new-job-title-is-ai-office-manager` | Le seul de première main et à la première personne. Il dit la promesse de l'offre sans la vendre : la valeur est dans les CLAUDE.md, les skills et les connecteurs, pas dans le prompt. |
| `2026-03-28-le-modele-cest-la-partie-facile.md` | `the-model-is-the-easy-part` | Le texte fondateur. Un CTO qui compare des modèles y trouve le déplacement du problème, avec une mesure publique derrière. |
| `2026-03-28-votre-agent-se-noie-dans-son-contexte.md` | `your-agent-isnt-confused-its-drowning` | La discipline de tokens, qui est le créneau libre du marché d'après `MARCHE-2026-08.md`. Sujet opérationnel, actionnable dans le repo. |
| `2026-03-28-le-probleme-des-99-pourcent.md` | `the-99-percent-problem` | De l'arithmétique, donc insensible au passage des modèles, et le seul des quatre qui donne au lecteur un chiffre qu'il peut répéter à son équipe le lendemain. |

Les cinq autres ont été laissés en anglais. `every-agent-works-in-the-demo` et `most-skill-md-files-work-once` recouvrent largement le contrat de reprise et les fichiers d'état déjà portés par `le-modele-cest-la-partie-facile`, quatre traductions auraient dit trois fois la même chose. `the-context-envelope`, `the-mcp-paradox` et `typescript-vs-javascript-for-ai-agents` sont les trois qui portent le plus de chiffres de seconde main, donc les plus coûteux à réécrire sans les revérifier un par un.

### Ce qui a été vérifié, corrigé ou coupé

**Vérifié et gardé.** Le résultat LangChain sur Terminal Bench 2.0, de 52,8 % à 66,5 % de tâches réussies avec le même modèle en dessous, gpt-5.2-codex, harness seul. Publié par LangChain et toujours debout en août 2026. La version française l'arrondit à « d'environ 53 % à 66 % », donne « près de quatorze points » plutôt que le gain relatif de 26 %, nomme LangChain comme source et porte la réserve, la mesure n'a pas été rejouée.

**Vérifié, arrondi et couvert par une réserve.** Stripe Minions. L'anglais dit « 1,000+ PRs per week », leur chiffre public a monté depuis, le français dit « plus de mille PR par semaine », ce qui reste vrai dans les deux cas. La phrase dit explicitement que c'est lu dans leur billet et pas de l'intérieur.

**Erreur d'arithmétique corrigée.** L'anglais écrit « cut the chain to 5 steps and hit 77% », mais la comparaison qui précède part de 90 % de fiabilité par étape, et cinq étapes à 90 % donnent 59 %, pas 77 % : le 77 % est la valeur à 95 % par étape, la ligne mélangeait deux colonnes du tableau. Le français dit 59 %. Le point en sort renforcé, raccourcir la chaîne fait passer de 12 à 59 %, améliorer la fiabilité par étape ne fait passer que de 12 à 36 %. **La version anglaise n'a pas été touchée, l'erreur y est toujours.**

**Table de l'article des 99 % revérifiée ligne par ligne**, les douze valeurs sont justes, le français les affiche en entiers.

**Affirmations de population réécrites.** L'anglais dit « most teams spend 80% of their effort », « most teams still do this », « almost nobody enforces it ». Ce sont des chiffres et des fréquences sans source, interdits par le guide de style. Le français les rend en observation de première main, « partout où je suis passé », « c'est ce que j'ai vu par défaut à peu près partout », « je l'ai rarement vue tenue ». Le 80/20 sans source a été coupé.

**Ajout, pas dans l'anglais.** `le-modele-cest-la-partie-facile` porte un paragraphe qui lève la collision de vocabulaire sur le mot harness : les harness du commerce se valent à peu près en ce moment, c'est une observation datée et pas une loi, et c'est justement parce qu'ils ont convergé que l'écart s'est déplacé sur ce qu'on met dedans. C'est la position de `VOIX-ET-POSITIONS.md`, sans laquelle l'article se lirait comme « choisissez le bon outil ».

**NDA et vie privée.** Rien dans les quatre articles ne touche à la mission sous NDA ni à quoi que ce soit de personnel. Les outils cités, Slack, Notion, CircleCI, sont génériques et ne sont rattachés à aucun client, les seuls employeurs nommés sont ceux du texte anglais d'origine, et aucune des sources publiques n'est française ni sectorielle.

## 3. Ce qui a été écarté

### Écarté pour risque professionnel, à ne pas rouvrir

**`articles/agent-tick-analysis/agent-tick-dysfunction.md`.** C'est un post-mortem interne, à charge, d'un vrai projet raté, avec des noms de collègues en clair (« confirmed by Guillaume in two weeks », « validated by staff engineer Alex Hocquard at the December 11 architecture review »), des dates de réunions internes, un décompte de positions dont l'attribution a été volée, et la mention « build outside the PIM » qui identifie l'employeur sans effort. Ce n'est pas la ligne rouge NDA de la section 2, c'est autre chose et c'est pire pour un site public. **À ne publier sous aucune forme.**

### Écartés parce qu'ils ne tiennent pas debout seuls, ou parce que ce sont des posts

- `articles/context-engineering-posts/` (8 posts humanisés) et `articles/linkedin-context-engineering-series-v2.md` : des séries de posts LinkedIn, écrites pour se lire à la suite dans un fil.
- `articles/linkedin-content-analysis-2025.md` : analyse de contenu LinkedIn, exclue par la consigne.
- `articles/claude-code-golden-nuggets-linkedin.md` : un cheat sheet Claude Code, format LinkedIn avec flèches et hashtags. Écarté aussi sur le fond : c'est précisément la visite guidée de doc dont l'offre cherche à se distinguer, et son contenu (Tool Search v2.1, `/teleport`, niveaux de thinking) périme en quelques mois.
- `articles/developer-time-economics/versions/v9.md` : bon texte, mais c'est un post LinkedIn daté du 2026-03-10, avec en-tête de version, hashtags et compteur de caractères. `OVERVIEW.md` du même dossier est une note de structure interne.
- `articles/agent-personification-7k2m9/` : cinq angles du même sujet, aucun n'est la version canonique.
- `articles/claude-signature-irony/` : trois longueurs du même texte (`article.md`, `article-short.md`, `article-v2.md`) sans version promue, et le sujet est culturel plutôt que production.
- `articles/incident-openai-huggingface/script-video.md` : porte `statut: brouillon` et c'est un script vidéo de 10 minutes en français, pas un article. Le fond est bon, une conversion en article est un chantier à part.

### Écartés pour cause de péremption

- `articles/agent-collective-memory/article.md` : tient en dix lignes, c'est un pitch (« quelqu'un devrait construire ça ») adossé à des chiffres de marché qui bougent tous les trimestres, et il cite Claude Opus 4.5 comme état de l'art.
- `articles/pre-act-planning-agents.md` : résumé d'un papier de mai 2025 dont la conclusion (planifier avant d'agir) est intégrée dans tous les harness depuis, avec des comparaisons à GPT-4 et Llama 70B.
- `articles/velocity-ai-agents-who-won-who-lost.md` : commentaire de marché sur qui a gagné et qui a perdu, adossé à des chiffres de financement et de mortalité de startups. Ne sert pas le positionnement, et se démode vite.
- `articles/tensorzero-llm-optimization-deep-dive.md` et `tensorzero-linkedin-post.md` : deep dive sur un produit tiers.

### Écartés parce que hors offre

- `articles/thinking-and-tool-use-display.md` et `chat-bubble-asymmetry.md` : design d'interfaces de chat IA. Bien écrits, mais c'est un autre métier que celui que vend le site.
- `articles/strawberry-hallucination-detector.md` : explication d'un outil de détection d'hallucinations.
- `articles/ai-sycophancy-authority-problem.md` et `ai-sycophancy-short-en.md` : la sycophancy et l'autorité qu'on accorde aux modèles, sujet grand public.
- `articles/safe-space-ou-zone-interdite.md` : conversation sur la spiritualité et le rapport à l'analyse, français, sans rapport avec l'offre.
- `articles/agent-washing-9f3x2q/article-agent-washing.md` : critique du marketing agentique, court, et il réutilise le chiffre des 82 % déjà porté par `the-99-percent-problem`.
- `articles/multi-team-agent-coherence/article.md` : cinq équipes qui écrivent dans le même agent. Forme de post LinkedIn, cadré par le risque, et il liste des symptômes sans proposer de sortie.
- `articles/undefined-agentic-kills-ai.md` : sur le vocabulaire flou en stratégie IA. Écarté pour deux raisons, il est écrit à la deuxième personne comme le portrait d'un dirigeant précis (« New managers arrive and find unresolved problems you supposedly solved months ago »), ce qui se lit comme une pique à quelqu'un d'identifiable, et il est cadré par le risque et pas par l'ambition.

### Le cas le plus limite, à trancher par Theo

**`articles/ai-browser-tools-guide/article.md`**, « Your AI Agent Doesn't Need a Browser. It Needs the Right One. » Article solide, première personne, très technique, et sur un sujet qui est bien de la discipline de tokens (le surcoût de Playwright MCP, l'arbre de décision pixels contre DOM).

Écarté sur le critère 3, pas sur la qualité. C'est un comparatif d'outils, et il argumente que le choix de l'outil pèse lourd, ce qui frotte contre la position datée que le site doit tenir, les harness se valent à peu près aujourd'hui et l'écart s'est déplacé sur ce qu'on met dedans. Il est aussi le plus fragile des candidats sur la fraîcheur, il dit lui-même « in March 2026 », il note Lightpanda en bêta et Stagehand en v3. Il suffit de dire un mot pour le rentrer, la version nettoyée n'est pas écrite mais le nettoyage est trivial, un H1 en tête et rien d'autre.

**`mediumarticles/safe-yolo-ai-agents-v4.md`**, le protocole « Safe YOLO ». C'est la version la plus aboutie des quatre (v1 à v4, plus un rendu HTML de la v3). Sur le fond, faire tourner des agents en autonomie sans se mettre en danger, c'est bien le sujet de l'offre. Écarté pour trois raisons cumulées : le dossier se décrit lui-même comme « multiple versions, in-progress » ; le texte affirme sans réserve des drapeaux et des noms d'outils précis (`gemini agent --sandbox --checkpointing`, ClaudeCage, le mode Auto-allow) qu'un CTO peut vérifier en trente secondes et qui ne sont pas de première main ; et il est intégralement cadré par le risque, avec des tirets cadratins partout, des titres à emoji et un bloc de hashtags, donc très loin de la voix du guide. Récupérable si Theo veut le reprendre lui-même, pas publiable en l'état.

---

## 4. Les doutes qui restent

1. **Les coquilles des 8 titres intacts.** « Dont trust AI experts », « Takeways from the Mixtral paper », « GauGAN2, NVIDIAs model keeps amazing me ». Elles viennent des posts LinkedIn d'origine, pas de la migration, donc elles n'ont pas été touchées. À trancher par Theo. Les 32 titres tronqués, eux, sont réécrits, voir la section 1.
2. **`ai-experts` du 2024-09-03.** Non migré, une redirection vers `dont-trust-ai-experts` est recommandée. Voir la section 1.
3. **Le déséquilibre de langue reste réel.** 49 posts en anglais contre 4 en français. `/ecrits/` a de quoi ne pas être vide et les quatre entrées françaises sortent en tête parce que le tri est antéchronologique, mais la page mélange les deux langues. C'est une décision de gabarit, pas de contenu.
4. **Les quatre articles français vieillissent avec l'anglais.** Ce sont des réécritures, pas des traductions, donc corriger un chiffre d'un côté ne le corrige pas de l'autre. Deux divergences sont déjà volontaires et documentées en section 2 bis, à ne pas « réaligner » par erreur.
5. **Le dossier `content/mediumarticles/` n'a rien donné.** Il ne contient que les quatre versions de « Safe YOLO », toutes écartées. Si Theo attendait de la matière de là, il n'y en a pas.
