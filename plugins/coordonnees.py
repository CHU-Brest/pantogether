"""
coordonnees — plugin Pelican pour PAN·TOGETHER
==============================================

Protège des collecteurs de spam les coordonnées écrites dans le markdown.

L'auteur écrit l'adresse ou le numéro **en clair**, entouré d'un marqueur ::

    - **Téléphone Secrétariat** : {tel}01 42 16 10 41{/tel}
    - **Courriel** : {@}jean-baptiste.bachet@aphp.fr{/@}

Le plugin les remplace par un bouton « Afficher… » qui ne porte que la valeur
brouillée ; ``bindCoordonnees()`` dans ``site.js`` ne la reconstitue qu'au clic
du visiteur. Le HTML publié ne contient donc jamais la coordonnée exploitable.

Le brouillage est un rot13 sur les lettres **et un rot5 sur les chiffres** (le
rot13 seul laisserait les numéros de téléphone intégralement lisibles), suivi
d'un encodage base64 : sans ce dernier, un ``wrna-oncgvfgr.onpurg@ncuc.se``
ressemblerait encore à une adresse pour un collecteur, et le rot13 est le
premier décodage qu'il essaierait.

Même motif que les fiches RCP (``rcp.js``), qui révèlent au clic des valeurs
encodées en base64 par ``build_dataset.py``.
"""

import base64
import html
import re

from pelican import signals

# {@}valeur{/@} ou {tel}valeur{/tel} — le marqueur fermant doit répéter l'ouvrant.
COORD_RE = re.compile(r"\{(@|tel)\}\s*(.+?)\s*\{/\1\}", re.DOTALL)

LIBELLES = {"@": "Afficher l'e-mail", "tel": "Afficher le numéro"}
KINDS = {"@": "mail", "tel": "tel"}


def rot(texte):
    """rot13 sur les lettres, rot5 sur les chiffres. Involutif."""
    out = []
    for c in texte:
        o = ord(c)
        if 65 <= o <= 90:      # A-Z
            out.append(chr((o - 65 + 13) % 26 + 65))
        elif 97 <= o <= 122:   # a-z
            out.append(chr((o - 97 + 13) % 26 + 97))
        elif 48 <= o <= 57:    # 0-9
            out.append(chr((o - 48 + 5) % 10 + 48))
        else:
            out.append(c)
    return "".join(out)


def brouille(texte):
    """Valeur telle qu'elle part dans le HTML : rot13/rot5 puis base64."""
    return base64.b64encode(rot(texte).encode("utf-8")).decode("ascii")


def _bouton(m):
    marqueur, valeur = m.group(1), m.group(2)
    return (
        '<button class="reveal-btn" type="button" data-kind="{kind}" '
        'data-coord="{coord}">{label}</button>'
    ).format(
        kind=KINDS[marqueur],
        coord=html.escape(brouille(valeur), quote=True),
        label=LIBELLES[marqueur],
    )


def process_content(content):
    # Pages comme articles : une actualité peut porter une adresse de contact.
    if not content._content:
        return
    content._content = COORD_RE.sub(_bouton, content._content)


def register():
    signals.content_object_init.connect(process_content)
