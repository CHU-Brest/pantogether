"""
thumbnails — plugin Pelican pour PAN·TOGETHER
==============================================

Associe une image de couverture à un billet d'actualité.

Dans l'en-tête du billet :

    Thumbnail: bob.jpg

Le fichier est cherché dans ``content/thumbnails/``. Le plugin expose
``article.thumbnail_url`` (chemin absolu, préfixé par ``SITEURL``), consommé
par ``actualites.html`` et ``index.html``.

Repli sur ``default.png`` quand le champ est absent **ou** quand le fichier
annoncé n'existe pas — dans ce second cas un avertissement est émis au build,
pour qu'une coquille dans le nom ne se traduise pas par une image cassée en
ligne.
"""

import os

from pelican import signals

logger = __import__("logging").getLogger(__name__)

THUMB_DIR = "thumbnails"
DEFAULT_THUMB = "default.png"


def _url(settings, filename):
    return "{}/{}/{}".format(settings.get("SITEURL", ""), THUMB_DIR, filename)


def add_thumbnail(generator):
    settings = generator.settings
    source_dir = os.path.join(settings["PATH"], THUMB_DIR)

    for article in generator.articles + generator.drafts:
        name = (getattr(article, "thumbnail", "") or "").strip()

        if name:
            # Un chemin ne doit pas permettre de sortir du dossier des vignettes.
            name = os.path.basename(name)
            if os.path.isfile(os.path.join(source_dir, name)):
                article.thumbnail_url = _url(settings, name)
                continue
            logger.warning(
                "[thumbnails] %s : vignette « %s » introuvable dans %s/ — "
                "repli sur %s.", article.source_path, name, THUMB_DIR, DEFAULT_THUMB
            )

        article.thumbnail_url = _url(settings, DEFAULT_THUMB)


def register():
    signals.article_generator_finalized.connect(add_thumbnail)
