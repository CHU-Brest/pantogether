AUTHOR = 'CHU Brest'
SITENAME = 'PAN·TOGETHER'
SITE_DESCRIPTION = "Réseau national de recherche clinique dédié aux cancers digestifs de mauvais pronostic."
SITEURL = ""

PATH = "content"

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'fr'

# Dates en français sans dépendre d'une locale système (souvent absente).
_MOIS_FR = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def fr_date(value):
    if not value:
        return ""
    return "{} {} {}".format(value.day, _MOIS_FR[value.month - 1], value.year)


JINJA_FILTERS = {"fr_date": fr_date}

# ------------------------------------------------------------------
# Thème & plugins
# ------------------------------------------------------------------
THEME = "theme"
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["docs_panels", "pelican.plugins.sitemap"]

# Sitemap XML généré à la racine du site par le plugin pelican-sitemap.
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.6, "pages": 0.7, "indexes": 0.5},
    "changefreqs": {"articles": "monthly", "pages": "monthly", "indexes": "weekly"},
}

# Markdown : on active `toc` pour que les titres reçoivent un id (ancres + panneaux)
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {},
    },
    'output_format': 'html5',
}

# ------------------------------------------------------------------
# Sources de contenu
# ------------------------------------------------------------------
PAGE_PATHS = ["pages", "extra"]
ARTICLE_PATHS = ["actualites"]
STATIC_PATHS = ["images", "favicon.ico"]

# favicon.ico copié à la racine du site (ce que les navigateurs et Google
# vont chercher en priorité).
EXTRA_PATH_METADATA = {"favicon.ico": {"path": "favicon.ico"}}

# ------------------------------------------------------------------
# URLs propres (répertoires)
# ------------------------------------------------------------------
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
ARTICLE_URL = "actualites/{slug}/"
ARTICLE_SAVE_AS = "actualites/{slug}/index.html"

# On ne génère que la landing comme « direct template » ; le listing Actualités
# est une page (Template: actualites). Pas de pages auteurs/catégories/tags/archives.
DIRECT_TEMPLATES = ["index"]
CATEGORY_SAVE_AS = ""
TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = ""

# ------------------------------------------------------------------
# Navigation & réseaux
# ------------------------------------------------------------------
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

SOCIAL = (
    ("LinkedIn", "#"),
    ("X / Twitter", "#"),
)
LINKS = ()

# Flux désactivés en développement
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

# URLs relatives pratiques en développement local
# RELATIVE_URLS = True
