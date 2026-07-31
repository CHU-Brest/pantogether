# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# Site publié sur le domaine personnalisé pantogether.fr (servi à la racine).
# SITEURL sans sous-chemin : CSS/JS/images, liens internes, canoniques et
# sitemap pointent tous vers https://pantogether.fr/...
SITEURL = "https://pantogether.fr"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Domaine personnalisé GitHub Pages : le fichier CNAME est copié à la racine
# du site publié pour conserver l'adresse pantogether.fr.
STATIC_PATHS = STATIC_PATHS + ["CNAME"]
EXTRA_PATH_METADATA = {**EXTRA_PATH_METADATA, "CNAME": {"path": "CNAME"}}

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""
