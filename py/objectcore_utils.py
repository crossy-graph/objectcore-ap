"""Shared constants and writers for ObjectCore-AP. No clock: dates come from RELEASE or from the data."""
import hashlib
import json
import pathlib

RELEASE = "0.1.0"
RELEASE_DATE = "2026-11-06"

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "src/objectcore_ap/schema/objectcore_ap.yaml"
VENDOR = ROOT / "src/objectcore_ap/schema/vendor/dcat_ap_plus.yaml"
EXAMPLES = ROOT / "examples/rdf"
DATA = ROOT / "data"
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"
VISUALS = DOCS / "visuals"
IMG = VISUALS / "img"
FONTS = ASSETS / "fonts"


def ensure_dirs():
    for d in (DIST, DOCS, VISUALS, IMG):
        d.mkdir(parents=True, exist_ok=True)


def write_json(path, obj):
    pathlib.Path(path).write_text(
        json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path, text):
    pathlib.Path(path).write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8", newline="\n")


def content_fingerprint(*paths):
    h = hashlib.sha256()
    for p in sorted(map(str, paths)):
        h.update(pathlib.Path(p).read_bytes())
    return h.hexdigest()[:12]
