# CLAUDE.md — site perso theomart.in

Site statique bilingue, français à la racine et anglais sous `/en/`, construit par un seul script Python et publié sur GitHub Pages.

## Ce dépôt est public

Tout ce qui est commité ici est lisible par n'importe qui, ce fichier compris. Deux règles priment sur toutes les autres.

**Mission sous NDA.** Theo est en mission chez un grand compte tenu par un NDA. La seule formule autorisée pour en parler est « un groupe du CAC 40 », employée seule. Ne jamais lui accoler le secteur d'activité, la stack technique de la mission, le nom du client ou un nom de projet interne, et ne jamais donner d'élément qui permettrait de recouper ces choses entre elles. Akeneo et Amazon sont des employeurs passés, librement citables. Devant une formulation qui hésite, ne pas l'écrire.

**Rien de personnel.** La vie privée de Theo n'entre pas ici, même en allusion : santé, la sienne ou celle de ses proches, relations, famille, finances personnelles, patrimoine, situation fiscale ou administrative, adresse postale, numéro de téléphone. Ni chiffre d'affaires, ni taux négocié avec un tiers, ni nom de prospect. La matière source vit dans un dépôt privé séparé, un agent qui l'a sous la main n'en recopie jamais le contenu ici.

Les seuls contacts publiables sont `contacttheomartin@gmail.com`, `https://www.linkedin.com/in/theomart/` et `https://github.com/theomart`.

## Ce dossier a un parent privé

Le repo vit dans `projects/site-perso/site/` d'un dépôt privé. La recherche, les relevés de prix des concurrents, les arbitrages commerciaux et le journal des sessions sont dans le dossier parent, `../wiki/`, `../raw/`, `../log.md`. Rien de tout ça ne descend ici, et ce qui est écrit ici est destiné à être lu par n'importe qui.

## Arborescence

```
build.py                   le seul script, 300 lignes maximum
requirements.txt           markdown, et rien d'autre
CNAME                      theomart.in, ne pas toucher
templates/base.html        coquille de toutes les pages
templates/post.html        coquille des articles
pages/fr/*.html            fragments HTML éditables à la main
pages/en/*.html
posts/AAAA-MM-JJ-slug.md   front matter plat + markdown
static/                    style.css, favicon.ico, theo.jpg, theo-portrait.webp, og-image*.png, copié tel quel
.github/workflows/deploy.yml
_site/                     sortie du build, jamais commitée
```

URLs : `/`, `/offre/`, `/formation-claude-code/`, `/ecrits/`, `/a-propos/`, `/mentions-legales/` en français, `/en/`, `/en/services/`, `/en/claude-code-training/`, `/en/writing/`, `/en/about/`, `/en/legal/` en anglais, les articles sous `/ecrits/<slug>/` et `/en/writing/<slug>/`. La page formation est hors nav, c'est la page d'entrée de la requête « formation Claude Code », elle porte un `FAQPage` et elle est reliée depuis l'accueil, l'offre et l'article sur les prix.

Deux flux RSS, `/feed.xml` pour l'anglais et `/ecrits/feed.xml` pour le français. `/feed.xml` garde son adresse historique, c'est celle que `jekyll-feed` servait, des abonnés en dépendent peut-être.

Le dictionnaire `REDIRECTS` en haut de `build.py` porte les anciennes URLs du site Jekyll qui n'ont plus de page à elles, `/team`, `/resume`, `/success`, `/talk`, `/aiservices`, les pages `/fr/`. Ne pas le vider, ce sont des liens entrants qui vivent encore.

Les deux pages de liste d'articles sont générées par `build.py` à partir de `posts/`, elles n'ont pas de fragment dans `pages/` et ne s'écrivent pas à la main. Le titre, la meta description et l'URL de bascule de langue de chaque page vivent dans la table `PAGES` en haut de `build.py`. Ajouter une page veut dire ajouter un fragment, une entrée dans `PAGES` et une entrée dans `NAV`.

## Contrat des marqueurs

Le rendu est un `str.replace` sur les gabarits, il n'y a pas de moteur de template et il n'y en aura pas. `templates/base.html` et `templates/post.html` portent ces marqueurs, espaces compris, exactement sous cette forme :

`{{ lang }}`, `{{ alt_lang }}`, `{{ title }}`, `{{ description }}`, `{{ content }}`, `{{ nav }}`, `{{ lang_switch_href }}`, `{{ lang_switch_label }}`, `{{ canonical }}`, `{{ og_locale }}`, `{{ og_image }}`, `{{ feed_url }}`, `{{ year }}`, `{{ footer_links }}`, `{{ robots }}`, `{{ alternates }}`

`og_image` est l'URL absolue de `static/og-image.png` (français) ou `static/og-image-en.png` (anglais), une carte 1200×630 aux couleurs du thème clair, texte à gauche et le portrait de `static/theo.jpg` à droite. Les deux se régénèrent en rasterisant un HTML, elles ne sont pas produites par le build. `static/theo.jpg` est le portrait carré en couleur sur fond studio, il sert aux cartes OG et au JSON-LD. Les pages affichent `static/theo-portrait.webp`, le même portrait détouré par Vision de macOS, passé en noir et blanc dans le fichier, recadré en 512×640 et posé sur le fond de la page avec un fondu en bas, ce qui tient dans les deux thèmes sans boîte. Il porte `fetchpriority="high"`, c'est l'image la plus grande au-dessus du pli. `feed_url` est l'URL absolue du flux RSS de la langue courante.

`lang_switch_href` est l'URL absolue de la page équivalente dans l'autre langue. `alt_lang` et `og_locale` en découlent, `fr`/`en` et `fr_FR`/`en_US`. `alternates` porte les trois `hreflang` d'une paire, `fr`, `en` et `x-default` sur la page française, calculés par `alternates()` depuis l'URL et `other`. Sur un article, il vaut la chaîne vide sauf si le front matter nomme sa jumelle dans `translation`, auquel cas `lang_switch_href` mène à la jumelle et non à l'index de l'autre langue.

`{{ robots }}` est collé au `canonical` dans les deux gabarits et vaut la chaîne vide par défaut. Il porte `noindex,follow` pour un article marqué `noindex`, et `noindex` sur les deux pages 404, qui sont servies en 200 à leur propre adresse, `/404.html` et `/en/404.html`, et se déclarent canoniques d'elles-mêmes plutôt que de l'accueil.

`templates/post.html` porte les mêmes marqueurs, plus `{{ post_title }}`, `{{ post_date }}` en date longue localisée, `{{ post_iso_date }}`, `{{ post_body }}` et `{{ ld_json }}`, le JSON-LD `BlogPosting` de l'article, déjà sérialisé par `build.py`.

Un marqueur laissé non substitué dans une page produite fait échouer le build. Inventer un marqueur dans un gabarit sans l'alimenter dans `build.py` casse donc le déploiement, ce qui est le comportement voulu.

## Front matter des articles

Plat, une clé par ligne, valeurs éventuellement entre guillemets. Le parseur fait dix lignes et ne gère ni liste ni imbrication, ne pas lui donner de YAML sophistiqué.

```yaml
---
title: "Titre de l'article"
date: 2026-08-25
lang: fr
summary: "Une phrase, 160 caractères max, sert de meta description et de résumé dans la liste."
source: linkedin
legacy_url: /jekyll/update/2024/08/26/colbert.html
noindex: true
translation: slug-de-la-jumelle
---
```

`title`, `date` au format `AAAA-MM-JJ` et `lang` valant `fr` ou `en` sont obligatoires, leur absence fait échouer le build en nommant le fichier. `summary`, `source`, `legacy_url`, `noindex` et `translation` sont facultatifs. `translation` est le slug de l'article équivalent dans l'autre langue, sans date ni préfixe d'URL, et chaque jumelle nomme l'autre ; un slug qui ne correspond à aucun article fait échouer le build. Cinq paires le portent. Un `legacy_url` fait générer à cette ancienne adresse une page de redirection avec meta refresh, canonical et lien de secours, pour ne pas casser les liens entrants du vieux blog.

`noindex: true` sort l'article de l'index des écrits, du sitemap et du flux RSS, et lui met un `noindex,follow`. Sa page et sa redirection restent servies, les liens entrants continuent de marcher. Les 40 posts LinkedIn recyclés d'avant 2026 le portent : ils parlent de ML généraliste, ils faisaient la moitié du sitemap, et ils disaient au moteur que le domaine parle d'autre chose que de ce qui est vendu. Un article de 2026 ne le porte pas.

## Allure

Trois polices, aucune téléchargée. Une serif système pour tout ce qui se lit, Iowan Old Style sur Apple, Palatino sur Windows, déclarée dans `--font`. Une sans système pour l'interface, nav, `.meta`, `.cta`, déclarée dans `--font-ui`. Une mono pour les dates, les prix et le code. Ne pas charger de police, et surtout ni Inter ni Geist, qui sont devenues la signature des sites générés. Corps à 18 px, interligne 1.55, échelle de titres fluide en `clamp()` avec un ratio de 1.2 à 1.25, letter-spacing négatif sur le `h1` seulement.

Les liens gardent la couleur du texte, seul le souligné porte l'accent. Une seule couleur d'accent, la rouille, et des neutres chauds jusque dans le thème sombre. Pas d'ombre, pas de dégradé, pas de carte, pas d'icône, pas de grain par filtre, au plus deux micro-interactions sur tout le site, le bouton qui s'enfonce et le fondu entre pages par `@view-transition`. Ce qui donne l'air « cher » à une page texte, c'est l'échelle et le rythme, pas une section de plus.

L'accueil ouvre sur la promesse en `h1`, pas sur le nom, puis la phrase d'accroche en `.lede`, une ligne de faits en `.meta` et un seul bouton. La preuve est un artefact inspectable, le CLAUDE.md de ce site cité dans un `pre`, jamais une capture d'écran ni un logo. Le contact est un bouton `mailto:` avec un sujet pré-rempli, l'adresse reste écrite en dessous.

## Classes CSS autorisées

Les fragments n'utilisent que celles-ci, la feuille de style ne stylise que celles-ci. Pas de framework, pas d'utilitaires façon Tailwind, pas de classe inventée hors de cette liste.

`.lede`, `.offer`, `.offer-price`, `.meta`, `.cta`, `.note`, `.portrait`, `.post-list`, `.post-item`, `.post-date`, `.post-title`, `.post-summary`, `.stack`, `.rule`

`.offer` contient un `h3`, un `.offer-price`, un `p` et un `ul`.

## Ton d'écriture

Tout est à la première personne du singulier, Theo est seul, il n'y a ni « nous » ni « notre équipe ».

Franglais assumé, repo et pas dépôt, harness et pas harnais, review et pas relecture, subagents, hooks, skills, prompt, CLAUDE.md. Pas de vocabulaire de cabinet, on nomme la chose concrète plutôt que la catégorie. Phrases longues jointes par des virgules, jamais de tiret cadratin. Chiffres arrondis. Pas de phrase d'introduction qui annonce ce qui va être dit, on entre dans le sujet. Pas de règle de trois, pas de parallélisme négatif à répétition. Une affirmation qui ne vient pas de l'expérience directe de Theo porte sa réserve.

Les prix sont affichés publiquement, en euros HT, c'est une décision prise.

## Modifier le build

`build.py` tient en 300 lignes et se lit de haut en bas. Il n'a qu'une dépendance externe, `markdown`. Pas de moteur de template, pas de Jekyll, pas de npm, pas de classe, pas de plugin. Entre une astuce élégante et trois lignes évidentes, écrire les trois lignes. Un ajout qui ferait dépasser le budget de lignes est le signe qu'il faut retirer autre chose, pas augmenter le budget.

Le build est bavard, une ligne par fichier produit et un décompte final, et il échoue en nommant le fichier fautif plutôt que de publier une page cassée. Les défauts sont accumulés puis affichés ensemble à la fin, un seul build montre donc tout ce qui cloche.

`python3 build.py --serve` construit puis sert `_site/` sur http://localhost:4400 .

## Déploiement

Push sur `main`, le workflow installe Python et `markdown`, lance `python3 build.py` et publie `_site/` via `actions/upload-pages-artifact` et `actions/deploy-pages`. La source Pages du dépôt est réglée sur GitHub Actions. Ne pas committer `_site/`, ne pas remettre de branche `gh-pages`, ne pas toucher au `CNAME`.
