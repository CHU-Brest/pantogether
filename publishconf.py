# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# Site publié sur GitHub Pages (URL de projet, sous-chemin /pantogether/).
# SITEURL doit inclure ce sous-chemin pour que le CSS, le JS et les images
# soient chargés depuis la bonne adresse.
SITEURL = "https://chu-brest.github.io/pantogether"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""
