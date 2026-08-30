"""Convertit `pantogether.xlsx` en JSON pour la page de recherche des RCP.

Outil **manuel** : à relancer quand le classeur change. Il écrit deux fichiers
dans `content/data/` :

* ``rcp.json``        — les données servies à la page ``/rcp/`` ;
* ``rcp-qualite.txt`` — le rapport des anomalies corrigées et des divergences
  restantes, à relire avant de versionner le JSON.

Usage :  make data        (ou  uv run --group data python build_dataset.py)
"""

import base64
import datetime as dt
import json
import re
import unicodedata
import warnings
from collections import Counter, defaultdict

import polars as pl

warnings.filterwarnings("ignore", category=FutureWarning)

SOURCE = "pantogether.xlsx"
OUT_JSON = "content/data/rcp.json"
OUT_REPORT = "rcp-qualite.txt"

# Champs dont la valeur est stockée en base64 pour ne pas exposer de données de
# contact en clair aux robots de collecte ; le JS les décode à la demande.
EMAIL_COLS = [
    "MEDECIN_EMAIL", "SECRETARIAT_EMAIL", "RCP_AMA_EMAIL",
    "IDEC_EMAIL", "IPA_EMAIL", "ARC_EMAIL",
]

# Les numéros suivent le même régime. Les fax ne sont pas affichés par la fiche,
# mais ils voyagent dans le JSON : les laisser en clair reviendrait à publier ce
# qu'on masque par ailleurs.
TEL_COLS = [
    "SECRETARIAT_TEL", "RCP_AMA_TEL", "IDEC_TEL", "IPA_TEL", "ARC_TEL",
    "SECRETARIAT_FAX", "RCP_AMA_FAX", "IDEC_FAX", "IPA_FAX", "ARC_FAX",
]

CONTACT_COLS = EMAIL_COLS + TEL_COLS

# Tant que le DPO n'a pas donné son accord pour publier les coordonnées réelles,
# elles sont remplacées par des valeurs factices AVANT d'atteindre le JSON : le
# fichier livré ne contient donc aucune donnée personnelle, même encodée. Passer
# à False publie les vraies coordonnées — ne le faire qu'une fois l'accord obtenu.
HIDE_PII = True

PII_EMAIL = "contact@example.fr"
PII_TEL = "+33 000000000"

# Les champs de texte libre (RCP_SOUMISSION surtout) contiennent parfois une
# adresse recopiée à la main. Elle échappe alors à l'encodage d'EMAIL_COLS et se
# retrouverait en clair dans le JSON servi, donc offerte aux robots de collecte.
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# Numéros français, dans les trois formes que prend le classeur :
# « +33 1 23 45 67 89 », « +331 23 45 67 89 » ou « 01 23 45 67 89 ».
PHONE_RE = re.compile(r"(?:\+33|0)[\s.\u2013-]?\d(?:[\s.\u2013-]?\d{2}){4}")

# Une colonne de contact correctement encodée ne contient que l'alphabet base64.
B64_RE = re.compile(r"[A-Za-z0-9+/]+={0,2}")

# Connecteurs laissés en suspens par le retrait d'une adresse en fin de phrase
# (« Dossier à soumettre par mail à ___ »).
DANGLING_RE = re.compile(r"(?:\s+(?:[àa]|au|aux|de|du|des))?[\s:;,.\u2013-]*$")

# Colonnes multivaluées, séparateur « ; » dans le classeur.
MULTI_COLS = ["PLATEAUX", "SOS", "SOS_AUTRES"]

NUM_COLS = ["CENTRE_LATITUDE", "CENTRE_LONGITUDE"]

OUTREMER = {"Guadeloupe", "Martinique", "Guyane", "La Réunion", "Mayotte"}

# Suffixes accolés au nom du centre, extraits en indicateurs booléens.
NOM_SUFFIXES = {
    "_Centre coordonnateur du réseau": "est_coordonnateur",
    "_Centre expert référent": "est_referent",
}

# --- Tables de canonisation -------------------------------------------------
# Ne fusionnent que de véritables doublons. Les distinctions d'autorisation
# (chirurgie mention A / B1, endoscopie bilio-pancréatique) sont conservées.
CANON_PLATEAUX = {
    "Anatomopathologie": "Plateforme d'anatomopathologie",
    "Imagerie": "Plateforme d'imagerie",
    "Plateforme de biologie moléculaire sur site": "Plateforme de biologie moléculaire",
    "Centre d'Investigation Clinique multithématique":
        "Centre d'Investigation Clinique multithématique du CHU",
    "Anesthésie de réanimation": "Plateau de réanimation",
}

CANON_SOS = {
    "Unité de soins palliatifs dévolue": "Unité de soins palliatifs dédiée",
}

CANON_SOS_AUTRES = {
    "Socio-esthéticiennes": "Socio-esthéticienne",
    "utn: unité transversale de nutrition": "UTN : unité transversale de nutrition",
}

CANON_FREQUENCE = {
    "Hebodomadaire": "Hebdomadaire",
}


def slugify(text):
    text = unicodedata.normalize("NFD", str(text or ""))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower().replace("œ", "oe").replace("æ", "ae")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


class Report:
    """Accumule les observations pour le rapport qualité."""

    def __init__(self):
        self.fixes = defaultdict(list)   # libellé de correction -> [lignes]
        self.dropped = []
        self.notes = []

    def fix(self, ligne, champ, avant, apres):
        self.fixes[f"{champ} : {avant!r} → {apres!r}"].append(ligne)


def clean_cell(value):
    """Chaîne nettoyée, ou None si la cellule est vide."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    return text or None


def split_multi(value):
    if not value:
        return []
    return [p.strip() for p in str(value).split(";") if p.strip()]


def canon_list(values, table, ligne, champ, report):
    """Applique la table de canonisation en dédoublonnant, ordre préservé."""
    out = []
    for v in values:
        c = table.get(v, v)
        if c != v:
            report.fix(ligne, champ, v, c)
        if c not in out:
            out.append(c)
    return out


def mask_contact(valeur):
    """`nom.prenom@chu.fr` → `n***@chu.fr`, `+33 1 23 45 67 89` → `+33 1 …89`.

    Le rapport qualité et les messages d'erreur doivent rester lisibles sans
    republier en clair ce qu'on vient précisément de retirer.
    """
    if "@" in valeur:
        local, _, domaine = valeur.partition("@")
        return f"{local[:1]}***@{domaine}"
    return f"{valeur[:6].strip()} …{valeur[-2:]}"


def anonymise(rec, hide_pii=HIDE_PII):
    """Substitue des coordonnées factices aux coordonnées réelles.

    Appliquée en amont de l'encodage base64 : la valeur réelle ne quitte jamais
    le classeur. L'encodage reste appliqué ensuite pour que la forme du JSON, et
    donc le code d'affichage, soient identiques dans les deux modes.
    """
    if not hide_pii:
        return
    for col in EMAIL_COLS:
        if col in rec:
            rec[col] = PII_EMAIL
    for col in TEL_COLS:
        if col in rec:
            rec[col] = PII_TEL


def strip_emails(rec, ligne, report):
    """Retire les adresses en clair des champs de texte libre.

    Les colonnes de contact dédiées (EMAIL_COLS) sont encodées en base64 plus
    loin et restent donc joignables depuis la fiche : on ne perd pas le moyen de
    contact, on retire seulement le doublon exposé en clair.
    """
    for champ, valeur in list(rec.items()):
        if champ in CONTACT_COLS or not isinstance(valeur, str):
            continue
        adresses = EMAIL_RE.findall(valeur)
        if not adresses:
            continue
        nettoye = re.sub(r"\s+", " ", EMAIL_RE.sub("", valeur)).strip()
        # Le retrait laisse une fin de phrase bancale (« … par mail à », « … : »).
        # On la rabote, puis on rend le point final si la phrase en avait un.
        nettoye = DANGLING_RE.sub("", nettoye)
        if nettoye and valeur.rstrip().endswith("."):
            nettoye += "."
        for adresse in adresses:
            report.fix(ligne, champ, mask_contact(adresse), "retiré (adresse en clair)")
        if nettoye:
            rec[champ] = nettoye
        else:
            rec.pop(champ)
            report.notes.append(
                f"ligne {ligne} : {champ} supprimé, ne contenait qu'une adresse")


def check(records):
    """Garde-fou : aucune donnée de contact en clair dans le JSON servi.

    Trois vérifications : pas d'adresse ni de numéro dans les champs ordinaires,
    et colonnes de contact effectivement encodées. Lève `AssertionError` plutôt
    que d'écrire un fichier fautif — si elle se déclenche, c'est qu'une forme
    d'adresse ou de numéro a échappé aux motifs, ou qu'une colonne de contact a
    été ajoutée sans être inscrite dans CONTACT_COLS.
    """
    fuites = []
    for rec in records:
        rcp = rec.get("id", "?")
        for champ, valeur in rec.items():
            if champ in CONTACT_COLS:
                if isinstance(valeur, str) and not B64_RE.fullmatch(valeur):
                    fuites.append((rcp, champ, valeur, "non encodé"))
                continue
            for texte in valeur if isinstance(valeur, list) else [valeur]:
                if not isinstance(texte, str):
                    continue
                fuites += [(rcp, champ, a, "adresse") for a in EMAIL_RE.findall(texte)]
                fuites += [(rcp, champ, n, "numéro") for n in PHONE_RE.findall(texte)]
    if fuites:
        detail = "\n".join(f"  {i} / {c} [{quoi}] : {mask_contact(v)}"
                           for i, c, v, quoi in fuites)
        raise AssertionError(
            f"{len(fuites)} donnée(s) de contact en clair dans le JSON :\n{detail}")
    return len(records)


def build_record(raw, ligne, report):
    rec = {}
    for key, value in raw.items():
        cleaned = clean_cell(value)
        if cleaned is not None:
            rec[key] = cleaned

    # --- nom du centre : extraire les suffixes de rôle ---
    nom = rec.get("CENTRE_NOM", "")
    for suffix, flag in NOM_SUFFIXES.items():
        if suffix in nom:
            nom = nom.replace(suffix, "")
            rec[flag] = True
            report.fix(ligne, "CENTRE_NOM", suffix, f"indicateur {flag}")
    if nom:
        rec["CENTRE_NOM"] = nom.strip()

    # --- colonnes multivaluées ---
    plateaux = canon_list(
        split_multi(rec.get("PLATEAUX")), CANON_PLATEAUX, ligne, "PLATEAUX", report)
    sos = canon_list(
        split_multi(rec.get("SOS")), CANON_SOS, ligne, "SOS", report)
    autres = canon_list(
        split_multi(rec.get("SOS_AUTRES")), CANON_SOS_AUTRES, ligne, "SOS_AUTRES", report)

    # Une ligne a recopié tout le vocabulaire SOS dans SOS_AUTRES : on retire
    # de SOS_AUTRES ce qui est déjà couvert par SOS.
    dedup = [v for v in autres if v not in sos]
    for v in autres:
        if v in sos:
            report.fix(ligne, "SOS_AUTRES", v, "retiré (déjà dans SOS)")

    for col, values in (("PLATEAUX", plateaux), ("SOS", sos), ("SOS_AUTRES", dedup)):
        if values:
            rec[col] = values
        else:
            rec.pop(col, None)

    # --- fréquence ---
    freq = rec.get("RCP_FREQUENCE")
    if freq and freq in CANON_FREQUENCE:
        report.fix(ligne, "RCP_FREQUENCE", freq, CANON_FREQUENCE[freq])
        rec["RCP_FREQUENCE"] = CANON_FREQUENCE[freq]

    # --- visio : déjà booléen dans le classeur ---
    rec["RCP_VISIO"] = bool(raw.get("RCP_VISIO"))

    # --- coordonnées ---
    for col in NUM_COLS:
        if col in rec:
            try:
                rec[col] = float(rec[col])
            except (TypeError, ValueError):
                report.fix(ligne, col, rec[col], "supprimé (non numérique)")
                rec.pop(col)

    lat, lon = rec.get("CENTRE_LATITUDE"), rec.get("CENTRE_LONGITUDE")
    if lat is not None and not (-25 <= lat <= 52):
        report.notes.append(f"ligne {ligne} : latitude hors plage France ({lat})")
    if lon is not None and not (-65 <= lon <= 56):
        report.notes.append(f"ligne {ligne} : longitude hors plage France ({lon})")

    # --- outre-mer ---
    rec["outremer"] = rec.get("CENTRE_REGION") in OUTREMER

    # --- adresses en clair dans le texte libre ---
    # Avant l'encodage ci-dessous, qui ne couvre que les colonnes dédiées.
    strip_emails(rec, ligne, report)

    # --- coordonnées de contact : masquées puis encodées ---
    anonymise(rec)
    for col in CONTACT_COLS:
        if col in rec:
            rec[col] = base64.b64encode(rec[col].encode("utf-8")).decode("ascii")

    return rec


def check_finess(records, report):
    """Signale les incohérences entre lignes partageant un même FINESS."""
    groups = defaultdict(list)
    for rec in records:
        if rec.get("FINESS"):
            groups[rec["FINESS"]].append(rec)

    watched = ["CENTRE_NOM", "CENTRE_VILLE", "CENTRE_REGION",
               "CENTRE_LATITUDE", "CENTRE_LONGITUDE", "PLATEAUX", "SOS"]
    for finess, rows in sorted(groups.items()):
        if len(rows) < 2:
            continue
        for col in watched:
            values = {json.dumps(r.get(col), ensure_ascii=False, sort_keys=True)
                      for r in rows}
            if len(values) > 1:
                nom = rows[0].get("CENTRE_NOM", "?")
                report.notes.append(
                    f"FINESS {finess} ({nom}) : {len(values)} valeurs "
                    f"différentes de {col} sur {len(rows)} lignes")


def make_ids(records):
    seen = Counter()
    for rec in records:
        base = "-".join(filter(None, [
            slugify(rec.get("AXE")),
            slugify(rec.get("CENTRE_VILLE")),
            slugify(rec.get("RCP_NOM")),
        ])) or "rcp"
        base = base[:80].strip("-")
        seen[base] += 1
        rec["id"] = base if seen[base] == 1 else f"{base}-{seen[base]}"


def collect_vocab(records):
    def multi(col):
        v = set()
        for r in records:
            v.update(r.get(col, []))
        return sorted(v)

    def single(col):
        return sorted({r[col] for r in records if r.get(col)})

    return {
        "axes": single("AXE"),
        "regions": single("CENTRE_REGION"),
        "jours": single("RCP_JOUR"),
        "frequences": single("RCP_FREQUENCE"),
        "plateaux": multi("PLATEAUX"),
        "sos": multi("SOS"),
        "sos_autres": multi("SOS_AUTRES"),
    }


def write_report(path, report, raw_count, records, vocab):
    lines = [
        "RAPPORT QUALITÉ — dataset RCP PAN·TOGETHER",
        f"Généré le {dt.date.today().isoformat()} depuis {SOURCE}",
        "=" * 72,
        "",
        ("COORDONNÉES MASQUÉES (hide_pii=True) — aucune donnée personnelle"
         if HIDE_PII else
         "!! COORDONNÉES RÉELLES PUBLIÉES (hide_pii=False) — accord DPO requis"),
        "",
        f"Lignes lues        : {raw_count}",
        f"Lignes ignorées    : {len(report.dropped)}",
        f"Lignes retenues    : {len(records)}",
        "",
    ]

    if report.dropped:
        lines += ["LIGNES IGNORÉES", "-" * 72]
        lines += [f"  ligne {n} : {motif}" for n, motif in report.dropped]
        lines.append("")

    lines += ["CORRECTIONS APPLIQUÉES AUTOMATIQUEMENT", "-" * 72]
    if report.fixes:
        for libelle in sorted(report.fixes):
            rows = report.fixes[libelle]
            apercu = ", ".join(str(r) for r in rows[:8])
            suite = f" … (+{len(rows) - 8})" if len(rows) > 8 else ""
            lines.append(f"  [{len(rows):3d}x] {libelle}")
            lines.append(f"         lignes : {apercu}{suite}")
    else:
        lines.append("  (aucune)")
    lines.append("")

    lines += [
        "DIVERGENCES NON RÉSOLUES — à arbitrer dans le classeur source",
        "-" * 72,
        "  Ces lignes partagent un même FINESS mais portent des valeurs",
        "  différentes. Le script ne tranche pas : il conserve chaque ligne",
        "  telle quelle. Les divergences de coordonnées GPS sont les plus",
        "  gênantes, car elles déplacent des marqueurs sur la carte.",
        "",
    ]
    if report.notes:
        lines += [f"  {n}" for n in report.notes]
    else:
        lines.append("  (aucune)")
    lines.append("")

    lines += ["VOCABULAIRES RETENUS", "-" * 72]
    for key, values in vocab.items():
        lines.append(f"  {key} ({len(values)}) :")
        lines += [f"      - {v}" for v in values]
        lines.append("")

    lines += ["TAUX DE REMPLISSAGE PAR CHAMP", "-" * 72]
    counts = Counter()
    for rec in records:
        counts.update(k for k, v in rec.items() if v not in (None, "", [], False))
    for col, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        pct = round(100 * n / max(len(records), 1))
        lines.append(f"  {col:22s} {n:4d}/{len(records)} ({pct:3d}%)")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    df = pl.read_excel(SOURCE)
    raw_rows = df.to_dicts()
    report = Report()
    records = []

    for index, raw in enumerate(raw_rows):
        ligne = index + 2  # +1 pour l'en-tête, +1 pour l'indexation à 1
        if not clean_cell(raw.get("CENTRE_NOM")):
            report.dropped.append((ligne, "CENTRE_NOM vide — ligne considérée vide"))
            continue
        records.append(build_record(raw, ligne, report))

    make_ids(records)
    check_finess(records, report)
    check(records)
    vocab = collect_vocab(records)

    payload = {
        "genere_le": dt.date.today().isoformat(),
        "source": SOURCE,
        "emails": "base64",
        "hide_pii": HIDE_PII,
        "count": len(records),
        "vocab": vocab,
        "rcp": records,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    write_report(OUT_REPORT, report, len(raw_rows), records, vocab)

    mode = ("coordonnées masquées" if HIDE_PII else
            "COORDONNÉES RÉELLES — accord DPO requis")
    print(f"[build_dataset] {SOURCE} → {OUT_JSON} ({len(records)} RCP, {mode})")
    print(f"[build_dataset] rapport qualité → {OUT_REPORT}")
    corrections = sum(len(v) for v in report.fixes.values())
    print(f"[build_dataset] {corrections} corrections, "
          f"{len(report.notes)} divergences signalées, "
          f"{len(report.dropped)} ligne(s) ignorée(s)")


if __name__ == "__main__":
    main()
