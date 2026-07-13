"""
docs_panels — plugin Pelican pour PAN·TOGETHER
================================================

Transforme une page markdown (métadonnée ``Template: docs``) en une mise en page
« documentation » à panneaux, fidèle au design du réseau :

* chaque titre de niveau 1 (``#`` en markdown, donc ``<h1>`` rendu) devient un
  **panneau** (``<section class="doc-panel">``) affiché un à la fois via le JS ;
* la **navigation de gauche** (``.docs-nav``) est générée automatiquement à partir
  de ces titres ;
* le premier panneau reçoit la classe ``active`` (évite le flash au chargement).

Le plugin expose deux attributs sur la page, consommés par ``docs.html`` :
``page.doc_nav_html`` et ``page.doc_panels_html``.
"""

import re

from markupsafe import Markup
from pelican import signals

# Icône par défaut de la nav de gauche (personnalisable ultérieurement par item).
DEFAULT_ICON = (
    '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></svg>'
)

# <h1 ...>contenu</h1>  (insensible à la casse, multi-lignes)
H1_RE = re.compile(r"<h1([^>]*)>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
ID_ATTR_RE = re.compile(r'id\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")


def _slugify(text):
    """Repli quand un titre n'a pas d'id (extension markdown ``toc`` désactivée)."""
    text = TAG_RE.sub("", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text or "section"


def _title_text(inner_html):
    return TAG_RE.sub("", inner_html).strip()


def process_content(content):
    # Uniquement les Pages explicitement marquées ``Template: docs``.
    if content.__class__.__name__ != "Page":
        return
    if getattr(content, "template", None) != "docs":
        return

    html = content._content or ""
    heads = list(H1_RE.finditer(html))

    # Aucun H1 (page stub vide, par ex.) : un panneau unique titré par la page.
    if not heads:
        pid = getattr(content, "slug", None) or "section"
        panels = (
            '<section class="doc-panel active" id="{id}">'
            "<h1>{title}</h1>{body}</section>"
        ).format(id=pid, title=content.title, body=html)
        nav = (
            '<li><a href="#{id}" data-target="{id}" data-label="{label}">{icon}{label}</a></li>'
        ).format(id=pid, label=content.title, icon=DEFAULT_ICON)
        content.doc_nav_html = Markup(nav)
        content.doc_panels_html = Markup(panels)
        return

    preamble = html[: heads[0].start()]
    panels = []
    nav = []

    for i, m in enumerate(heads):
        start = m.start()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        segment = html[start:end]

        id_match = ID_ATTR_RE.search(m.group(1))
        title = _title_text(m.group(2))
        pid = id_match.group(1) if id_match else _slugify(title)

        # Le tout premier panneau récupère l'éventuel préambule (avant le 1er #).
        if i == 0 and preamble.strip():
            segment = preamble + segment

        active = " active" if i == 0 else ""
        panels.append(
            '<section class="doc-panel{active}" id="{id}">{body}</section>'.format(
                active=active, id=pid, body=segment
            )
        )
        nav.append(
            '<li><a href="#{id}" data-target="{id}" data-label="{label}">{icon}{label}</a></li>'.format(
                id=pid, label=title, icon=DEFAULT_ICON
            )
        )

    content.doc_nav_html = Markup("\n".join(nav))
    content.doc_panels_html = Markup("\n".join(panels))


def register():
    signals.content_object_init.connect(process_content)
