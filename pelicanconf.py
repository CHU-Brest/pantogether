AUTHOR = 'CHU Brest'
SITENAME = 'PAN·TOGETHER'
SITE_DESCRIPTION = "Réseau national de recherche clinique dédié aux cancers digestifs de mauvais pronostic."

# Bandeau fin affiché au-dessus de l'en-tête, sur toutes les pages.
# Mettre à None (ou "") pour le retirer ; surchargeable dans publishconf.py.
SITE_BANNER = "Site en construction"

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
# « coordonnees » passe avant « docs_panels » : ce dernier fige le HTML en
# panneaux, les marqueurs {@} / {tel} ne seraient plus substitués après lui.
PLUGINS = ["coordonnees", "docs_panels", "thumbnails", "pelican.plugins.sitemap"]

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
STATIC_PATHS = ["images", "favicon.ico", "data", "assets", "thumbnails"]

# favicon.ico copié à la racine du site (ce que les navigateurs et Google
# vont chercher en priorité).
EXTRA_PATH_METADATA = {"favicon.ico": {"path": "favicon.ico"}}

# Verrous et fichiers temporaires des suites bureautiques : jamais publiés.
IGNORE_FILES = [".#*", ".~lock.*", "~$*"]

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

# Frise des partenaires et financeurs, en bas de la page d'accueil.
# LOGO       : chemin de l'image dans le site (par ex. "/images/logo-inca.svg").
#              Laisser vide tant que le logo n'est pas disponible : la carte
#              affiche alors le seul intitulé, sans case vide.
# DESCRIPTION: intitulé affiché sous le logo, et texte alternatif de l'image.
# URL        : site du partenaire. Laisser vide pour une carte non cliquable.
PARTNERS = [
    {
        # Logo 2025 de l'INCa, domaine public (Wikimedia Commons).
        "LOGO": "/images/logo-inca.svg",
        "DESCRIPTION": "INCa (Institut national du cancer)",
        "URL": "https://www.cancer.fr/",
    },
    {
        # Logo officiel du CHU (chu-brest.fr), diffusé en CC BY 4.0 sur
        # Wikimedia Commons — auteur : CHU Brest.
        "LOGO": "/images/logo-chu-brest.svg",
        "DESCRIPTION": "CHU de Brest",
        "URL": "https://www.chu-brest.fr/",
    },
]
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
