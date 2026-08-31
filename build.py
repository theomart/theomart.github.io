#!/usr/bin/env python3
"""Construit le site theomart.in dans _site/. Une seule dépendance externe, markdown, et le
rendu est une substitution de chaînes dans templates/, sans moteur de template.
`python3 build.py --serve` construit puis sert sur http://localhost:4400 .
"""
import functools, json, re, shutil, sys
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import markdown

SITE_URL = "https://theomart.in"
PORT = 4400
ROOT = Path(__file__).parent
OUT = ROOT / "_site"
YEAR = str(date.today().year)

# Toutes les pages du site, une entrée par page, éditable à la main.
# `src` est un fragment HTML de pages/. Une entrée sans `src` mais avec `heading` est un index
# d'écrits, dont la liste d'articles est fabriquée à partir de posts/.
# `other` est l'URL de la même page dans l'autre langue.
PAGES = [
    {"src": "fr/index.html", "url": "/", "other": "/en/", "title": "Theo Martin, agents de code en production",
     "description": "Je construis des agents de code en production et j'aide les équipes à tirer vraiment parti des leurs, audit du repo, formation Claude Code intra, office hours. À Paris."},
    {"src": "fr/offre.html", "url": "/offre/", "other": "/en/services/", "title": "Formation Claude Code intra, audit, office hours · Theo Martin",
     "description": "Audit du setup agentique, formation Claude Code intra sur votre repo, office hours, build d'un système d'agents. Prix affichés en euros HT, depuis Paris."},
    {"heading": "Écrits", "url": "/ecrits/", "other": "/en/writing/", "title": "Écrits · Theo Martin",
     "description": "Des notes sur Claude Code, les agents de code, les LLM en production et ce qu'on met dans un harness."},
    {"src": "fr/a-propos.html", "url": "/a-propos/", "other": "/en/about/", "title": "À propos · Theo Martin",
     "description": "Huit ans de ML et de systèmes LLM en production, dont cinq chez Amazon, puis Tech Lead de l'équipe Core AI chez Akeneo. Indépendant à Paris."},
    {"src": "en/index.html", "url": "/en/", "other": "/", "title": "Theo Martin, coding agents in production",
     "description": "I build coding agents that run in production, and I help teams get real value out of theirs, repo audit, in-house Claude Code training, office hours. Based in Paris."},
    {"src": "en/services.html", "url": "/en/services/", "other": "/offre/", "title": "Claude Code training on your repo, audit · Theo Martin",
     "description": "Agentic setup audit, in-house Claude Code training on your own repo, office hours, building an agent system. Public prices in euros, based in Paris."},
    {"heading": "Writing", "url": "/en/writing/", "other": "/ecrits/", "title": "Writing · Theo Martin",
     "description": "Notes on Claude Code, coding agents, LLMs in production, and what goes into a harness."},
    {"src": "en/about.html", "url": "/en/about/", "other": "/a-propos/", "title": "About · Theo Martin",
     "description": "Eight years of ML and production LLM systems, five of them at Amazon, then Tech Lead of the Core AI team at Akeneo. Independent, based in Paris."},
    {"src": "fr/mentions-legales.html", "url": "/mentions-legales/", "other": "/en/legal/", "title": "Mentions légales · Theo Martin",
     "description": "Éditeur, hébergeur, absence de cookies et de traceurs."},
    {"src": "en/legal.html", "url": "/en/legal/", "other": "/mentions-legales/", "title": "Legal notice · Theo Martin",
     "description": "Publisher, host, and the absence of cookies and trackers."},
]

# Pied de page, par langue. Le site n'a pas de moteur de gabarit, donc le lien change ici.
FOOTER = {
    "fr": '<a href="/ecrits/feed.xml">RSS</a> &middot; <a href="/mentions-legales/">Mentions légales</a>',
    "en": '<a href="/feed.xml">RSS</a> &middot; <a href="/en/legal/">Legal</a>',
}
FEED_URL = {"fr": "/ecrits/feed.xml", "en": "/feed.xml"}
OG_IMAGE = {"fr": "/static/og-image.png", "en": "/static/og-image-en.png"}

# Anciennes URLs du site Jekyll qui n'ont plus de page à elles. La clé est le fichier produit
# dans _site/, ce qui couvre d'un coup /team et /team.html sur GitHub Pages.
REDIRECTS = {
    "blog.html": "/en/writing/",
    "aiservices.html": "/en/services/",
    "aiservices/strategy.html": "/en/services/",
    "aiservices/ml.html": "/en/services/",
    "aiservices/genai.html": "/en/services/",
    "aiservices/automation.html": "/en/services/",
    "aiservices/productivity.html": "/en/services/",
    "team.html": "/en/about/",
    "success.html": "/en/services/",
    "talk.html": "/en/",
    "about/index.html": "/en/about/",
    "aispeedrace.html": "/en/",
    "fr/index.html": "/",
    "fr/aiservices.html": "/offre/",
    "fr/aiservices/strategy.html": "/offre/",
    "fr/aiservices/ml.html": "/offre/",
    "fr/aiservices/genai.html": "/offre/",
    "fr/aiservices/automation.html": "/offre/",
    "fr/aiservices/productivity.html": "/offre/",
    "fr/team.html": "/a-propos/",
    "fr/success.html": "/offre/",
    "fr/talk.html": "/",
    # Brouillon jamais rendu par Jekyll, faute de front matter, mais servi en 200 malgré tout.
    "2024/09/03/ai-experts.html": "/en/writing/dont-trust-ai-experts/",
}
NAV = {
    "fr": [("/", "Accueil"), ("/offre/", "Offre"), ("/ecrits/", "Écrits"), ("/a-propos/", "À propos")],
    "en": [("/en/", "Home"), ("/en/services/", "Services"), ("/en/writing/", "Writing"), ("/en/about/", "About")],
}
WRITING_URL = {"fr": "/ecrits/", "en": "/en/writing/"}
NOT_FOUND = {
    "fr": ("Page introuvable · Theo Martin", '<h1>Page introuvable</h1>\n<p>Ce lien ne mène nulle part. <a class="cta" href="/">Retour à l\'accueil</a></p>'),
    "en": ("Page not found · Theo Martin", '<h1>Page not found</h1>\n<p>This link leads nowhere. <a class="cta" href="/en/">Back to the home page</a></p>'),
}
MOVED = {"fr": "Cette page a déménagé, sa nouvelle adresse est", "en": "This page has moved, its new address is"}
MONTHS = {  # pas de locale, les runners GitHub n'ont pas fr_FR installé
    "fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split(),
    "en": "January February March April May June July August September October November December".split(),
}
REDIRECT = """<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}"><title>{title}</title></head>
<body><p>{moved} <a href="{target}">{target}</a></p></body></html>
"""

MARKER = re.compile(r"\{\{[^{}]*\}\}")
PROBLEMS, WRITTEN = [], []

def problem(message):  # on note le défaut et on continue, un seul build montre tout ce qui cloche
    PROBLEMS.append(message)

def read(path):
    return path.read_text(encoding="utf-8")

def parse_front_matter(text, source):
    """Front matter plat, `cle: valeur`, guillemets optionnels, ni liste ni imbrication."""
    if not text.startswith("---"):
        problem(f"{source} : pas de front matter")
        return {}, text
    _, raw, body = text.split("---", 2)
    meta = {}
    for line in raw.strip().splitlines():
        key, _, value = line.partition(":")
        if value.strip():
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body.lstrip()

def render(template, values):
    """Substitution bête et méchante, chaque {{ cle }} devient sa valeur."""
    for key, value in values.items():
        template = template.replace("{{ " + key + " }}", value)
    return template

def path_for(url):
    """/offre/ devient _site/offre/index.html, / devient _site/index.html."""
    return OUT / url.strip("/") / "index.html" if url.strip("/") else OUT / "index.html"

def write(path, html, source):
    """Écrit une page. Un marqueur non substitué est une erreur, jamais une page publiée."""
    left = MARKER.search(html)
    if left:
        problem(f"{source} : marqueur {left.group(0)} laissé tel quel dans la page produite")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    WRITTEN.append(path)
    print(f"  {path.relative_to(OUT)}")

def nav(lang, current_url):
    here = ' aria-current="page"'
    links = (f'<a href="{url}"{here if url == current_url else ""}>{label}</a>' for url, label in NAV[lang])
    return "<nav>\n" + "\n".join(links) + "\n</nav>"

def shell(url, title, description, other, nav_url=None):
    """Les marqueurs communs à base.html et post.html. `nav_url` sert aux articles, dont le lien
    de nav à souligner est l'index des écrits et pas leur propre URL."""
    lang = "en" if url.startswith("/en") else "fr"  # tout l'anglais vit sous /en/
    alt = "fr" if lang == "en" else "en"
    return {"lang": lang, "alt_lang": alt, "title": escape(title), "description": escape(description),
            "nav": nav(lang, url if nav_url is None else nav_url), "lang_switch_href": SITE_URL + other, "lang_switch_label": alt.upper(),
            "canonical": SITE_URL + url, "year": YEAR, "content": "", "footer_links": FOOTER[lang], "og_locale": "fr_FR" if lang == "fr" else "en_US",
            "feed_url": SITE_URL + FEED_URL[lang], "og_image": SITE_URL + OG_IMAGE[lang]}

def long_date(iso, lang):
    year, month, day = iso.split("-")
    name = MONTHS[lang][int(month) - 1]
    return f"{int(day)} {name} {year}" if lang == "fr" else f"{name} {int(day)}, {year}"

def escape_lone_hashes(text):
    """Les hashtags LinkedIn en début de ligne, #AI, deviendraient des titres de niveau un :
    Python-Markdown n'exige pas d'espace après le dièse. On les échappe, hors blocs de code."""
    lines, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            line = re.sub(r"^(#{1,6})(?=[^\s#])", r"\\\1", line)
        lines.append(line)
    return "\n".join(lines)

def feed(posts, lang, self_url):
    """Flux RSS, pour ne pas casser les abonnés de l'ancien /feed.xml produit par jekyll-feed."""
    items = "".join(
        f"<item><title>{escape(post['title'])}</title>"
        f"<link>{SITE_URL}{post['url']}</link><guid>{SITE_URL}{post['url']}</guid>"
        f"<pubDate>{format_datetime(datetime.fromisoformat(post['date']).replace(tzinfo=timezone.utc))}</pubDate>"
        f"<description>{escape(post.get('summary', ''))}</description></item>\n"
        for post in posts[:20])
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>\n'
            f"<title>Theo Martin</title><link>{SITE_URL}</link>"
            f'<atom:link xmlns:atom="http://www.w3.org/2005/Atom" href="{SITE_URL}{self_url}" rel="self"/>'
            f"<description>{'Écrits sur les agents de code' if lang == 'fr' else 'Writing on coding agents'}</description>"
            f"<language>{lang}</language>\n{items}</channel></rss>\n")

def load_posts():
    """Lit posts/*.md, valide le front matter, rend le markdown, trie par date décroissante."""
    posts = []
    for path in sorted((ROOT / "posts").glob("*.md")):
        source = f"posts/{path.name}"
        if not re.match(r"\d{4}-\d{2}-\d{2}-", path.name):
            print(f"  ignoré, {source} n'est pas un article nommé AAAA-MM-JJ-slug.md")
            continue
        meta, body = parse_front_matter(read(path), source)
        absent = [field for field in ("title", "date", "lang") if not meta.get(field)]
        if absent:
            problem(f"{source} : front matter sans {', '.join(absent)}")
            continue
        if meta["lang"] not in NAV or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["date"]):
            problem(f"{source} : lang doit valoir fr ou en et date suivre AAAA-MM-JJ, lu lang='{meta['lang']}' date='{meta['date']}'")
            continue
        meta["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        meta["url"] = WRITING_URL[meta["lang"]] + meta["slug"] + "/"
        meta["body"] = markdown.markdown(escape_lone_hashes(body), extensions=["extra", "smarty"])
        meta["long_date"] = long_date(meta["date"], meta["lang"])
        posts.append(meta)
    posts.sort(key=lambda post: post["date"], reverse=True)
    return posts

def post_list(posts):
    return '<ul class="post-list">\n' + "".join(
        f'<li class="post-item">\n<span class="post-date">{post["long_date"]}</span>\n'
        f'<a class="post-title" href="{post["url"]}">{escape(post["title"])}</a>\n'
        f'<p class="post-summary">{escape(post.get("summary", ""))}</p>\n</li>\n'
        for post in posts) + "</ul>"

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    base = read(ROOT / "templates" / "base.html")
    post_template = read(ROOT / "templates" / "post.html")
    posts = load_posts()
    # Un post `noindex` reste servi et redirigé, mais sort de l'index, du sitemap et des flux.
    live = [post for post in posts if not post.get("noindex")]

    print("Pages :")
    for page in PAGES:
        values = shell(page["url"], page["title"], page["description"], page["other"])
        if "heading" in page:
            values["content"] = (f'<h1>{page["heading"]}</h1>\n<p class="lede">{page["description"]}</p>\n'
                                 + post_list([p for p in live if WRITING_URL[p["lang"]] == page["url"]]))
        elif (ROOT / "pages" / page["src"]).exists():
            values["content"] = read(ROOT / "pages" / page["src"])
        else:
            problem(f"pages/{page['src']} est absent, la page {page['url']} n'a pas été construite")
            continue
        write(path_for(page["url"]), render(base, values), page.get("src", page["url"]))

    print("Articles :")
    for post in posts:
        other = "en" if post["lang"] == "fr" else "fr"
        # Les articles ne sont pas traduits, la bascule de langue mène à l'index de l'autre langue.
        values = shell(post["url"], f"{post['title']} · Theo Martin", post.get("summary", ""), WRITING_URL[other], nav_url=WRITING_URL[post["lang"]])
        values.update(robots='<meta name="robots" content="noindex,follow">' if post.get("noindex") else "", post_title=escape(post["title"]), post_date=post["long_date"], post_iso_date=post["date"], post_body=post["body"],
                      ld_json=json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"], "datePublished": post["date"],
                          "inLanguage": post["lang"], "description": post.get("summary", ""), "url": values["canonical"], "author": {"@type": "Person", "name": "Theo Martin"}}, ensure_ascii=False))
        write(path_for(post["url"]), render(post_template, values), f"posts/{post['slug']}")

    print("Redirections des anciennes URLs :")
    for post in [post for post in posts if post.get("legacy_url")]:
        legacy = post["legacy_url"].strip("/")
        path = OUT / legacy if legacy.endswith(".html") else OUT / legacy / "index.html"
        write(path, REDIRECT.format(lang=post["lang"], target=SITE_URL + post["url"],
              title=escape(post["title"]), moved=MOVED[post["lang"]]), f"redirection {post['legacy_url']}")

    print("Redirections des anciennes pages :")
    for source_path, target in REDIRECTS.items():
        lang = "en" if target.startswith("/en") else "fr"
        write(OUT / source_path, REDIRECT.format(lang=lang, target=SITE_URL + target,
              title="Theo Martin", moved=MOVED[lang]), f"redirection /{source_path}")

    print("Flux RSS :")
    # /feed.xml garde son adresse historique, il portait le blog anglais sous Jekyll.
    write(OUT / "feed.xml", feed([p for p in live if p["lang"] == "en"], "en", "/feed.xml"), "feed.xml")
    write(OUT / "ecrits" / "feed.xml", feed([p for p in live if p["lang"] == "fr"], "fr", "/ecrits/feed.xml"), "ecrits/feed.xml")

    print("Pages 404 et fichiers annexes :")
    for lang, (title, body) in NOT_FOUND.items():
        values = shell("/" if lang == "fr" else "/en/", title, title, "/en/" if lang == "fr" else "/", nav_url="")
        values["content"] = body
        write(OUT / "404.html" if lang == "fr" else OUT / "en" / "404.html", render(base, values), f"404 {lang}")
    locs = "".join(f"  <url><loc>{SITE_URL}{p['url']}</loc>" + (f"<lastmod>{p['date']}</lastmod>" if p.get("date") else "") + "</url>\n" for p in PAGES + live)
    write(OUT / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{locs}</urlset>\n', "sitemap.xml")
    write(OUT / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", "robots.txt")
    for name, copy in (("static", shutil.copytree), ("CNAME", shutil.copy), ("llms.txt", shutil.copy)):
        if not (ROOT / name).exists():
            problem(f"{name} est absent de la racine du projet")
            continue
        copy(ROOT / name, OUT / name)
        print(f"  {name} copié tel quel")

    print(f"\n{len(WRITTEN)} fichiers écrits dans _site/, dont {len(posts)} articles.")
    if PROBLEMS:
        print(f"\nBUILD EN ÉCHEC, {len(PROBLEMS)} problème(s) :\n  - " + "\n  - ".join(PROBLEMS), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        handler = functools.partial(SimpleHTTPRequestHandler, directory=str(OUT))
        print(f"\nAperçu sur http://localhost:{PORT} , Ctrl+C pour arrêter.")
        ThreadingHTTPServer(("", PORT), handler).serve_forever()
