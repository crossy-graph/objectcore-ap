"""Step site: write the GitHub Pages site (docs/) from dist/model.json: documentation pages and figure pages."""
import csv
import json
import pathlib
import sys
from html import escape

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import site_kit  # noqa: E402
from objectcore_utils import CONTENT, DATA, DIST, DOCS, IMG, RELEASE, RELEASE_DATE, VISUALS, ensure_dirs, write_text  # noqa: E402

CREDIT = "Data: ObjectCore-AP %s (%s), CC-BY-4.0 profile; example values are invented. Font: Fira Sans (SIL OFL)." % (RELEASE, RELEASE_DATE)


def captions(m):
    caps = [("pipeline", "V.1", "From community to DCAT-AP export: seven stages with the numbers of the current build."),
            ("model", "V.2", "Structure of the profile: dataset, object and event classes with their RDF classes."),
            ("crosswalk", "V.3", "The %d super-properties and how the profile treats each of them." % len(m["crosswalk"])),
            ("tests", "V.4", "Test results: every example against the profile shapes and the official DCAT-AP 3.0.1 shapes.")]
    for i, ex in enumerate(m["examples"], 1):
        caps.append(("example-" + ex["file"].replace(".ttl", ""), "E.%d" % i,
                     "Object biography of the example %s: dataset, object and events." % ex["file"]))
    return caps


def md(path, title, body):
    write_text(DOCS / path, "---\nlayout: default\ntitle: %s\n---\n\n%s" % (title, body))


def table(headers, rows):
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    out = "| " + " | ".join(headers) + " |\n|" + "---|" * len(headers) + "\n"
    return out + "".join("| " + " | ".join(esc(c) for c in r) + " |\n" for r in rows)


def doc_pages(m):
    n = m["counts"]
    md("index.md", "Overview",
       "# ObjectCore-AP\n\nApplication profile for the Object Core Metadata Profile (OCMDP) of NFDI4Objects. "
       "It is a formal extension of DCAT-AP 3.0.1, built on DCAT-AP+ in LinkML. The core comes only from the DCAT-AP family; "
       "everything else is an extension mapped to CIDOC CRM and its extensions. The focus is events and object biography.\n\n"
       "The pages show the current build: release %s, %d classes, %d slots, %d event classes, %d super-properties, %d valid and %d invalid examples.\n\n"
       "* [Visuals](visuals/index.html): the whole chain from community to export, drawn from the current data\n"
       "* [Profile](profile.html): classes and slots\n* [Crosswalk](crosswalk.html): super-properties to profile elements and DCAT-AP\n"
       "* [Findings](findings.html): what the example datasets showed\n\n"
       "> The namespace `https://w3id.org/nfdi4objects/objectcore-ap/` is provisional until it is registered at w3id.org. "
       "DCAT-AP+ has no official release; the profile pins commit 198ac222.\n"
       % (m["release"], n["classes"], n["slots"], n["event_classes"], n["super_properties"], n["examples_valid"], n["examples_invalid"]))
    cls = [[c["name"], c["class_uri"], c["is_a"], c["description"]] for c in m["classes"]]
    sl = [[s["name"], s["slot_uri"], s["range"], s["description"]] for s in m["slots"]]
    md("profile.md", "Profile",
       "# Profile\n\nGenerated from `src/objectcore_ap/schema/objectcore_ap.yaml`.\n\n## Classes\n\n" + table(["Class", "RDF class", "Parent", "Description"], cls)
       + "\n## Slots\n\n" + table(["Slot", "Predicate", "Range", "Description"], sl))
    with open(DATA / "crosswalk.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    md("crosswalk.md", "Crosswalk",
       "# Crosswalk\n\nSuper-properties from the task-area communities, the profile element that carries them and the DCAT-AP 3.0.1 export slot. "
       "The German columns are the working language of the workbook.\n\n"
       + table(["SP", "Name", "Profile element", "Cardinality", "DCAT-AP 3.0.1", "Kind"],
               [[r["Super-Property"], r["Name_en"], r["ObjectCore-AP-Element"], r["Kardinalität"], r["DCAT-AP 3.0.1 (Export)"], r["Art"]] for r in rows]))
    body = (CONTENT / "example-findings.md").read_text(encoding="utf-8").split("\n", 1)[1]
    md("findings.md", "Findings", "# Findings from the example datasets\n" + body)


def fig_card(name, label, cap, link=None):
    img = IMG / (name + ".png")
    w, h = _png_size(img)
    src = "img/%s.png" % name
    return ('<section><img src="%s" width="%d" height="%d" loading="lazy" alt="%s">'
            '<div class="row2"><span class="n">%s</span><span class="cap">%s</span>'
            '<button type="button" onclick="navigator.clipboard.writeText(this.dataset.t)" data-t="%s">Copy</button></div>'
            '<p class="credit">%s</p><a href="img/%s.png">PNG</a> \u00b7 <a href="img/%s.svg">SVG</a></section>'
            % (src, w, h, escape(cap, True), label, escape(cap), escape(cap, True), escape(CREDIT), name, name))


def _png_size(p):
    b = p.read_bytes()
    return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")


def page(title, active, m, inner):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s \u00b7 ObjectCore-AP</title><link rel="stylesheet" href="../assets/site.css"></head><body>%s<main><h1>%s</h1>%s</main></body></html>\n'
            % (escape(title), site_kit.nav_static(m, active), escape(title), inner))


def visual_pages(m):
    caps = captions(m)
    cards = "".join('<section><a href="%s.html"><img src="img/%s.png" width="%d" height="%d" loading="lazy" alt="%s"></a>'
                    '<div class="row2"><span class="n">%s</span><span class="cap"><a href="%s.html">%s</a></span></div></section>'
                    % (n, n, _png_size(IMG / (n + ".png"))[0], _png_size(IMG / (n + ".png"))[1], escape(c, True), l, n, escape(c))
                    for n, l, c in caps)
    write_text(VISUALS / "index.html", page("Visuals", "visuals/index.html", m,
               '<p>The chain from community to DCAT-AP export, drawn from the current data of the build.</p><div class="grid">%s</div>' % cards))
    for n, l, c in caps:
        write_text(VISUALS / (n + ".html"), page("%s %s" % (l, c.split(":")[0]), "visuals/%s.html" % n, m, fig_card(n, l, c)))


def main():
    ensure_dirs()
    m = json.loads((DIST / "model.json").read_text(encoding="utf-8"))
    site_kit.write_assets(m)
    doc_pages(m)
    visual_pages(m)
    print("site: %d figure pages, 4 documentation pages in docs/" % len(captions(m)))


if __name__ == "__main__":
    main()
