import datetime
import os
import shlex
import shutil
import sys

from invoke import task
from invoke.main import program
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file
from pelican.utils import slugify

OPEN_BROWSER_ON_SERVE = True
SETTINGS_FILE_BASE = "pelicanconf.py"
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    "settings_base": SETTINGS_FILE_BASE,
    "settings_publish": "publishconf.py",
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    "deploy_path": SETTINGS["OUTPUT_PATH"],
    # Host and port for `serve`
    "host": "localhost",
    "port": 8000,
}


@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])


@task
def build(c):
    """Build local version of site"""
    pelican_run("-s {settings_base}".format(**CONFIG))


@task
def rebuild(c):
    """`build` with the delete switch"""
    pelican_run("-d -s {settings_base}".format(**CONFIG))


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    pelican_run("-r -s {settings_base}".format(**CONFIG))


@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG["deploy_path"],
        (CONFIG["host"], CONFIG["port"]),
        ComplexHTTPRequestHandler,
    )

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    sys.stderr.write("Serving at {host}:{port} ...\n".format(**CONFIG))
    server.serve_forever()


@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


@task
def preview(c):
    """Build production version of site"""
    pelican_run("-s {settings_publish}".format(**CONFIG))

@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    def cached_build():
        cmd = "-s {settings_base} -e CACHE_CONTENT=true LOAD_CONTENT_CACHE=true"
        pelican_run(cmd.format(**CONFIG))

    cached_build()
    server = Server()
    theme_path = SETTINGS["THEME"]
    watched_globs = [
        CONFIG["settings_base"],
        f"{theme_path}/templates/**/*.html",
    ]

    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_glob = "{}/**/*{}".format(SETTINGS["PATH"], extension)
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = f"{theme_path}/static/**/*{extension}"
        watched_globs.append(static_file_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if OPEN_BROWSER_ON_SERVE:
        # Open site in default browser
        import webbrowser

        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


@task
def publish(c):
    """Publish to production via rsync"""
    pelican_run("-s {settings_publish}".format(**CONFIG))
    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {ssh_port}" '
        "{} {ssh_user}@{ssh_host}:{ssh_path}".format(
            CONFIG["deploy_path"].rstrip("/") + "/", **CONFIG
        )
    )


@task(help={"title": "Titre de l'actualité (demandé si absent)",
            "date": "Date de l'événement AAAA-MM-JJ (défaut : aujourd'hui)",
            "time": "Heure HH:MM (défaut : 09:00)",
            "tags": "Tags séparés par des virgules (défaut : agenda)"})
def new(c, title="", date="", time="09:00", tags="agenda"):
    """Crée content/actualites/AAAA-MM-JJ-slug.md avec l'en-tête pré-rempli"""
    title = title.strip() or input("Titre de l'actualité : ").strip()
    if not title:
        sys.exit("Titre vide, abandon.")
    day = (
        datetime.date.fromisoformat(date) if date else datetime.date.today()
    )
    slug = slugify(title, regex_subs=SETTINGS["SLUG_REGEX_SUBSTITUTIONS"])
    folder = os.path.join(SETTINGS["PATH"], SETTINGS["ARTICLE_PATHS"][0])
    path = os.path.join(folder, f"{day.isoformat()}-{slug}.md")
    if os.path.exists(path):
        sys.exit(f"{path} existe déjà, abandon.")
    header = (
        f"Title: {title}\n"
        f"Date: {day.isoformat()} {time}\n"
        f"Category: Actualités\n"
        f"Tags: {tags}\n"
        f"Slug: {slug}\n"
        f"Author: {SETTINGS['AUTHOR']}\n"
        f"Summary: \n"
        f"\n"
    )
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(header)
    print(path)


def pelican_run(cmd):
    cmd += " " + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))
