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
    # --- Financeurs et établissement porteur ---------------------------
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
    # --- Fédérations hospitalières -------------------------------------
    {
        # Logo officiel, servi par le site de la FHF (fhf.fr).
        "LOGO": "/images/logo-fhf.svg",
        "DESCRIPTION": "FHF (Fédération hospitalière de France)",
        "URL": "https://www.fhf.fr/",
    },
    {
        # Logo 2018, récupéré via bergonie.fr (institut membre d'Unicancer).
        "LOGO": "/images/logo-unicancer.png",
        "DESCRIPTION": "Unicancer",
        "URL": "https://www.unicancer.fr/",
    },
    {
        # Logo RVB 2023, servi par le site de la FHP (fhp.fr).
        "LOGO": "/images/logo-fhp.png",
        "DESCRIPTION": "FHP (Fédération de l'hospitalisation privée)",
        "URL": "https://www.fhp.fr/",
    },
    # --- Sociétés savantes ---------------------------------------------
    {
        # Logo servi par achbt.org.
        "LOGO": "/images/logo-achbt.jpg",
        "DESCRIPTION": "ACHBT (Association de chirurgie hépato-bilio-pancréatique et transplantation)",
        "URL": "https://www.achbt.org/",
    },
    {
        # Pictogramme AFEF : le site (thème sombre) ne sert que des logotypes blancs.
        "LOGO": "/images/logo-afef.png",
        "DESCRIPTION": "AFEF (Association française pour l'étude du foie)",
        "URL": "https://afef.asso.fr/",
    },
    {
        # Intitulé complet à confirmer.
        # Logo servi par afihge.org.
        "LOGO": "/images/logo-afihge.png",
        "DESCRIPTION": "AFIHGE (Association française des internes d'hépato-gastro-entérologie)",
        "URL": "https://www.afihge.org/",
    },
    {
        # Logo servi par afsos.org.
        "LOGO": "/images/logo-afsos.png",
        "DESCRIPTION": "AFSOS (Association francophone des soins oncologiques de support)",
        "URL": "https://www.afsos.org/",
    },
    {
        # Logo servi par angh.net.
        "LOGO": "/images/logo-angh.jpg",
        "DESCRIPTION": "ANGH (Association nationale des gastroentérologues des hôpitaux généraux)",
        "URL": "https://angh.net/",
    },
    {
        # Logo extrait du site asfarglobal.org (SVG inline encapsulant un PNG).
        "LOGO": "/images/logo-asfar.png",
        "DESCRIPTION": "ASFAR",
        "URL": "https://asfarglobal.org/",
    },
    {
        # Logo servi par ffcd.fr.
        "LOGO": "/images/logo-ffcd.jpg",
        "DESCRIPTION": "FFCD (Fédération francophone de cancérologie digestive)",
        "URL": "https://ffcd.fr/",
    },
    {
        # Logo servi par le site de la SFCD, qui héberge les pages FRENCH.
        "LOGO": "/images/logo-french.jpg",
        "DESCRIPTION": "FRENCH (Fédération de recherche en chirurgie)",
        "URL": "https://www.sfchirurgiedigestive.fr/french/presentation",
    },
    {
        # Logo servi par gercor.com.
        "LOGO": "/images/logo-gercor.png",
        "DESCRIPTION": "GERCOR (Groupe coopérateur multidisciplinaire en oncologie)",
        "URL": "https://www.gercor.com/",
    },
    {
        # Logo servi par sfchirurgiedigestive.fr (et non sfcd.fr, qui est le
        # syndicat des femmes chirurgiens dentistes).
        "LOGO": "/images/logo-sfcd.png",
        "DESCRIPTION": "SFCD (Société française de chirurgie digestive)",
        "URL": "https://www.sfchirurgiedigestive.fr/",
    },
    {
        # Logo servi par sfco.fr. Le site titre « Francophone », le logo
        # imprime encore « Française ».
        "LOGO": "/images/logo-sfco.png",
        "DESCRIPTION": "SFCO (Société francophone de chirurgie oncologique)",
        "URL": "https://sfco.fr/",
    },
    {
        # Logo servi par sfed.org.
        "LOGO": "/images/logo-sfed.png",
        "DESCRIPTION": "SFED (Société française d'endoscopie digestive)",
        "URL": "https://www.sfed.org/",
    },
    {
        # Logo servi par sfpo.com (site protégé par Cloudflare).
        "LOGO": "/images/logo-sfpo.png",
        "DESCRIPTION": "SFPO (Société française de pharmacie oncologique)",
        "URL": "https://sfpo.com/",
    },
    {
        # Logo servi par siad.radiologie.fr.
        "LOGO": "/images/logo-siad.png",
        "DESCRIPTION": "SIAD (Société d'imagerie abdominale et digestive)",
        "URL": "https://siad.radiologie.fr/",
    },
    {
        # Logo servi par snfge.org.
        "LOGO": "/images/logo-snfge.png",
        "DESCRIPTION": "SNFGE (Société nationale française de gastro-entérologie)",
        "URL": "https://www.snfge.org/",
    },
    # --- Associations d'internes ---------------------------------------
    {
        # Logo servi par aerio-oncologie.org.
        "LOGO": "/images/logo-aerio.png",
        "DESCRIPTION": "AERIO (Association d'enseignement et de recherche des internes en oncologie)",
        "URL": "https://aerio-oncologie.org/",
    },
    {
        # Logo servi par sfjro.fr.
        "LOGO": "/images/logo-sfjro.jpg",
        "DESCRIPTION": "SFjRO (Société française des jeunes radiothérapeutes-oncologues)",
        "URL": "https://www.sfjro.fr/",
    },
    # --- Instances professionnelles ------------------------------------
    {
        # Logo servi par cnpipa.fr.
        "LOGO": "/images/logo-cnpipa.png",
        "DESCRIPTION": "CNP IPA (Conseil national professionnel des infirmier·es en pratique avancée)",
        "URL": "https://cnpipa.fr/",
    },
    {
        "LOGO": "",
        "DESCRIPTION": "Présidents de CME de CHU et de CHG",
        "URL": "",
    },
    # --- Groupes et réseaux de recherche -------------------------------
    {
        # Logo et lien déjà utilisés dans les pages du site.
        "LOGO": "/images/francim.jpg",
        "DESCRIPTION": "FRANCIM (réseau des registres des cancers)",
        "URL": "https://www.francim-reseau.org/",
    },
    {
        # Logo servi par unicancer.fr.
        "LOGO": "/images/logo-ucgi.png",
        "DESCRIPTION": "UCGI (Unicancer Gastrointestinal Group)",
        "URL": "https://www.unicancer.fr/fr/les-groupes-d-experts/unicancer-gastrointestinal-group-ucgi/",
    },
    {
        # Logo et lien déjà utilisés dans les pages du site.
        "LOGO": "/images/frap.png",
        "DESCRIPTION": "Réseau FRAP",
        "URL": "https://www.frap-network.org/",
    },
    # --- Associations et partenaires institutionnels -------------------
    {
        # Logo servi par ligue-cancer.net.
        "LOGO": "/images/logo-ligue-cancer.png",
        "DESCRIPTION": "La Ligue contre le cancer",
        "URL": "https://www.ligue-cancer.net/",
    },
    {
        # Logo servi par adiresca.fr.
        "LOGO": "/images/logo-adiresca.jpg",
        "DESCRIPTION": "ADIRESCA (Association des dispositifs spécifiques régionaux du cancer)",
        "URL": "https://adiresca.fr/",
    },
    # --- Associations de patients --------------------------------------
    {
        # Logo et lien déjà utilisés dans les pages du site.
        "LOGO": "/images/arcad.jpg",
        "DESCRIPTION": "Fondation ARCAD",
        "URL": "https://www.fondationarcad.org",
    },
    {
        # Logo et lien déjà utilisés dans les pages du site.
        "LOGO": "/images/albi.png",
        "DESCRIPTION": "ALBI France",
        "URL": "https://albi-france.org",
    },
    {
        # Logo et lien déjà utilisés dans les pages du site.
        "LOGO": "/images/soshepatites.png",
        "DESCRIPTION": "SOS Hépatites",
        "URL": "https://soshepatites.org",
    },
    {
        # Logo et lien déjà utilisés dans les pages du site.
        "LOGO": "/images/ffh.png",
        "DESCRIPTION": "France Fer Hémochromatose",
        "URL": "https://www.hemochromatose.org",
    },
    {
        # Logo et lien déjà utilisés dans les pages du site.
        "LOGO": "/images/etendard.jpg",
        "DESCRIPTION": "L'Étendard des cancers digestifs",
        "URL": "https://www.facebook.com/Etendardducancerdigestif/?locale=fr_FR",
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
