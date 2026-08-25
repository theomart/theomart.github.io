# theomart.in

Site statique. Un script Python de 220 lignes, une dépendance, zéro framework. Hébergé sur GitHub Pages.

## Modifier une page

Les pages sont des fragments HTML dans `pages/fr/` et `pages/en/`. On ouvre le fragment, on écrit dedans, il n'y a ni front matter ni balise à respecter, c'est juste le corps de la page. Le titre et la meta description de chaque page vivent dans la table `PAGES` en haut de `build.py`, une entrée par page.

Les deux pages de liste, `/ecrits/` et `/en/writing/`, sont fabriquées par le build à partir des articles. Elles n'ont pas de fragment, on ne les écrit pas à la main.

## Écrire un article

Un fichier dans `posts/`, nommé `AAAA-MM-JJ-slug.md`, qui commence par ceci :

```yaml
---
title: "Titre de l'article"
date: 2026-08-25
lang: fr
summary: "Une phrase, 160 caractères maximum, elle sert de meta description et de résumé dans la liste."
---
```

Puis du markdown normal. `lang: fr` publie l'article sous `/ecrits/<slug>/`, `lang: en` sous `/en/writing/<slug>/`, et la page de liste de la bonne langue se met à jour toute seule. Si l'article reprend une ancienne adresse du blog, ajouter `legacy_url: /ancienne/adresse.html` et le build fabrique la redirection à cette ancienne adresse, pour que les liens entrants continuent de marcher.

## Prévisualiser en local

```bash
pip install -r requirements.txt
python3 build.py --serve
```

Puis ouvrir http://localhost:4400 . Il n'y a pas de rechargement automatique, on relance la commande après chaque modification.

## Déployer

Pousser sur `main`, GitHub Actions construit et publie. Rien d'autre à faire.

Le build est strict et c'est voulu. Un article sans titre, sans date ou sans langue, une page dont le fragment manque, un marqueur `{{ ... }}` resté visible dans une page produite, et le build s'arrête en nommant le fichier fautif. Le job échoue et le site en ligne reste celui d'avant, plutôt que de publier une page cassée.
