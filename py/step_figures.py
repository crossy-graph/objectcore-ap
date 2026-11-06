"""Step figures: draw the figures (SVG, then PNG) from dist/model.json into docs/visuals/img/."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from objectcore_utils import DIST, IMG, ensure_dirs  # noqa: E402
from svgkit import (CLASS, INSTANCE, MUTED, OWL, PROP, REAL, TERM, Canvas, H, W, tw, to_png, wrap)  # noqa: E402

CATS = [("Taken from DCAT-AP", INSTANCE, "#000000"), ("Imported from DCAT-AP+", TERM, "#ffffff"),
        ("Tightened (NFDI core)", REAL, "#ffffff"), ("Extension", CLASS, "#ffffff"), ("Open", OWL, "#000000")]


SHORT = {"Taken from DCAT-AP": "taken from DCAT-AP", "Imported from DCAT-AP+": "from DCAT-AP+", "Tightened (NFDI core)": "tightened", "Extension": "extensions", "Open": "open"}


def category(art):
    a = art.lower()
    if "offen" in a:
        return CATS[4][0]
    if a.startswith("verschärft"):
        return CATS[2][0]
    if a.startswith("importiert"):
        return CATS[1][0]
    if a.startswith("übernommen"):
        return CATS[0][0]
    return CATS[3][0]


def load():
    return json.loads((DIST / "model.json").read_text(encoding="utf-8"))


def fig_pipeline(m):
    c = Canvas("From community to export")
    n = m["counts"]
    cat_count = {}
    for r in m["crosswalk"]:
        cat_count[category(r["Art"])] = cat_count.get(category(r["Art"]), 0) + 1
    tests = m["tests"]
    inv_ok = sum(1 for t in tests if t["expected"] == "invalid" and t["profile"] == "violations")
    val_ok = sum(1 for t in tests if t["expected"] == "valid" and t["profile"] == "conforms")
    dc = sum(1 for t in tests if t.get("dcat_ap_301") == "conforms")
    c.header("From community to DCAT-AP export",
             "Seven stages of ObjectCore-AP, with the numbers of the current build (release %s)" % m["release"])
    cols = [
        ("1  Communities", "4 task areas", INSTANCE, ["TA1 Documentation", "TA2 Collections", "TA3 Archaeometry", "TA4 Protecting",
                                                        "MDSE, KuR-MDS,", "heritage records"]),
        ("2  Super-properties", "%d SPs" % n["super_properties"], PROP, ["%d %s" % (v, SHORT[k]) for k, v in sorted(cat_count.items(), key=lambda kv: (-kv[1], kv[0]))]),
        ("3  Core", "Levels A, B, C", REAL, ["A  dataset", "B  object", "C  event", "Core from the", "DCAT-AP family"]),
        ("4  Profile", "%d classes" % n["classes"], CLASS, ["%d slots" % n["slots"], "%d event classes" % n["event_classes"], "LinkML profile on", "DCAT-AP+; CRM and", "its extensions"]),
        ("5  Generated", "dist/", TERM, ["JSON Schema", "SHACL (merged)", "OWL", "model.json"]),
        ("6  Tests", "%d examples" % (n["examples_valid"] + n["examples_invalid"]), REAL,
         ["%d of %d valid conform" % (val_ok, n["examples_valid"]), "%d of %d invalid rejected" % (inv_ok, n["examples_invalid"]), "SHACL, pyshacl"]),
        ("7  Export", "DCAT-AP 3.0.1", OWL, ["Every record is also a", "dcat:Dataset", "%d of %d valid pass the" % (dc, n["examples_valid"]), "official SHACL", "(recorded)"]),
    ]
    bw, gap, x0, y0 = 205, 32.5, 60, 190
    for i, (t, sub, fill, det) in enumerate(cols):
        x = x0 + i * (bw + gap)
        c.text(x, y0 - 18, t, 22, 500, "#9a3412", maxw=bw)
        c.box(x, y0, bw, 130, sub, None, fill)
        if i:
            c.arrow(x - gap + 2, y0 + 65, x - 2, y0 + 65)
        yy = y0 + 175
        for d in det:
            c.text(x + 4, yy, d, 18, 400, "#1f1f1d", maxw=bw)
            yy += 30
    # lower band: what each stage is made of
    c.rect(60, 560, 1630, 290, "#f6f6f3", "#d8d6ce", 10, 1)
    c.text(84, 600, "How the stages are produced", 24, 500, maxw=600)
    rows = [("1 to 3", "Workbook “ObjectCore-AP Arbeitsmatrix”: communities, super-properties, core levels, decisions B-01 to B-08."),
            ("4", "src/objectcore_ap/schema/objectcore_ap.yaml is the single source of truth for the profile."),
            ("5", "python main.py generate  runs the LinkML generators and the SHACL post-processing."),
            ("6", "python main.py test  validates every example against the profile shapes."),
            ("7", "Instances carry oc: and dcat: types, so the same RDF is valid DCAT-AP 3.0.1.")]
    yy = 642
    for k, v in rows:
        c.text(84, yy, k, 20, 500, "#9a3412", maxw=80)
        for l in wrap(v, 20, 1480, 400, 2):
            c.text(170, yy, l, 20, 400, "#1f1f1d", maxw=1500)
            yy += 28
        yy += 18
    c.note("Numbers are read from dist/model.json; the DCAT-AP 3.0.1 result is recorded in data/dcatap_results.json unless the test step runs with --dcatap.")
    return c


def fig_model(m):
    c = Canvas("Structure of the profile")
    cls = {x["name"]: x for x in m["classes"]}
    c.header("Structure of the profile", "%d classes in three core levels; each box shows the class and its RDF class" % m["counts"]["classes"])
    lanes = [("A  Dataset", ["ObjectCoreDataset", "ObjectCoreDistribution"], CLASS),
             ("B  Object", ["PhysicalObject", "Sample", "DigitalRepresentation", "Dating", "ObjectLocation", "ObjectGeometry", "AgentInRole", "Uncertainty"], CLASS),
             ("C  Event", m["event_classes"], CLASS)]
    y = 135
    bw, bh, gap, x0 = 335, 62, 20, 270
    for name, items, fill in lanes:
        rows = (len(items) + 3) // 4
        lh = rows * (bh + 14) + 20 + (70 if name.startswith("C") else 0)
        c.rect(60, y, 1630, lh, "#f6f6f3", "#d8d6ce", 10, 1)
        c.text(80, y + 38, name, 26, 500, "#9a3412", maxw=180)
        yy = y + 14
        if name.startswith("C"):
            c.box(x0, yy, 4 * bw + 3 * gap, 54, "ObjectEvent (base)", "time span, place, participation, uncertainty, evidence, event type", fill=OWL, tsize=20, ssize=15)
            yy += 70
        for i, it in enumerate(items):
            col, row = i % 4, i // 4
            x, yb = x0 + col * (bw + gap), yy + row * (bh + 14)
            sub = cls[it]["class_uri"] or "(no class_uri)"
            c.box(x, yb, bw, bh, it, sub, fill, "#ffffff", tsize=20, ssize=15)
        y += lh + 16
    c.note("Source: src/objectcore_ap/schema/objectcore_ap.yaml. Classes inherited from DCAT-AP+ (Agent, Concept, PeriodOfTime and others) are not drawn.")
    return c


def fig_crosswalk(m):
    c = Canvas("Super-properties and where they come from")
    c.header("Super-properties and their origin", "%d super-properties of the crosswalk, grouped by how the profile treats them" % len(m["crosswalk"]))
    groups = {k: [] for k, _, _ in CATS}
    for r in m["crosswalk"]:
        groups[category(r["Art"])].append(r)
    cw, gap = 306, 25
    for i, (name, fill, ink) in enumerate(CATS):
        x = 60 + i * (cw + gap)
        c.box(x, 140, cw, 70, "%s" % name, "%d super-properties" % len(groups[name]), fill, ink, tsize=20, ssize=16)
        yy = 230
        for r in groups[name]:
            label = "%s  %s" % (r["Super-Property"], r["Name_en"])
            ls = wrap(label, 17, cw - 20, 400, 2)
            hh = 14 + 22 * len(ls)
            c.rect(x, yy, cw, hh, "#ffffff", "#000000", 8, 1)
            for j, l in enumerate(ls):
                c.text(x + 10, yy + 22 + j * 22, l, 17, 400, "#1f1f1d", maxw=cw - 16)
            yy += hh + 8
        if yy > H - 50:
            raise ValueError("crosswalk figure overflows")
    c.note("Source: data/crosswalk.csv. SP-30 (software, service, teaching material) waits until a community needs it.")
    return c


def ev_name(m, types):
    by_uri = {x["class_uri"]: x["name"] for x in m["classes"] if x["class_uri"]}
    names = [by_uri.get(t, t) for t in types]
    names = [n for n in names if n not in ("ObjectEvent",)]
    return ", ".join(sorted(set(names))) or "Event"


def fig_example(m, ex):
    c = Canvas("Object biography: " + ex["file"])
    c.header("Object biography: %s" % ex["object"], "Record %s, %d triples. Dataset, object and events of the example" % (ex["file"], ex["triples"]))
    c.box(60, 330, 330, 160, ex["dataset"], "oc:ObjectCoreDataset + dcat:Dataset", INSTANCE, tsize=21)
    c.text(60, 306, "A  Dataset", 22, 500, "#9a3412")
    c.arrow(392, 410, 500, 410)
    c.text(446, 396, "subject", 15, 400, MUTED, "middle")
    c.text(500, 306, "B  Object", 22, 500, "#9a3412")
    ot = ", ".join(ex["object_types"]) or "prov:Entity"
    c.box(500, 330, 380, 160, ex["object"], ot, REAL, "#ffffff", tsize=21, ssize=15)
    c.text(1010, 150, "C  Events (oc:biography)", 22, 500, "#9a3412")
    evs = ex["events"]
    if not evs:
        c.rect(1010, 330, 680, 100, "#ffffff", "#000000", 10, 1.5, "8 6")
        c.text(1030, 388, "No biography events in this record", 22, 400, MUTED, maxw=640)
    else:
        eh, eg = 76, 12
        top = 170
        for i, e in enumerate(evs):
            y = top + i * (eh + eg)
            sub = (e["event_type"] + " · " if e["event_type"] else "") + ", ".join(e["types"])
            c.box(1010, y, 680, eh, ev_name(m, e["types"]), sub, CLASS, "#ffffff", tsize=21, ssize=15)
            c.arrow(882, 410, 1008, y + eh / 2, "#000000", 1.5)
        if top + len(evs) * (eh + eg) > H - 60:
            raise ValueError("too many events")
    c.text(60, 580, "Extension slots used in this record", 22, 500, maxw=700)
    x, y = 60, 600
    for s in ex["slots_used"]:
        w = tw(s, 16) + 18
        if x + w > 940:
            x, y = 60, y + 36
        c.chip(x, y, s)
        x += w + 8
    flags = [("dating", ex["has_dating"]), ("geometry", ex["has_geometry"]), ("uncertainty", ex["has_uncertainty"])]
    c.text(60, y + 80, "Present: " + ", ".join(k for k, v in flags if v) if any(v for _, v in flags) else "No dating, geometry or uncertainty in this record", 18, 400, MUTED, maxw=900)
    c.note("Source: examples/rdf/valid/%s. All values in the examples are invented." % ex["file"])
    return c


def fig_tests(m):
    c = Canvas("Test results")
    c.header("Test results", "Every example against the profile shapes and, for valid ones, the official DCAT-AP 3.0.1 shapes")
    cols = [("Example", 60, 760), ("Expected", 840, 220), ("Profile SHACL", 1080, 300), ("DCAT-AP 3.0.1", 1400, 290)]
    for t, x, w in cols:
        c.text(x, 160, t, 22, 500, "#9a3412", maxw=w)
    y = 180
    for t in m["tests"]:
        ok = (t["profile"] == "conforms") == (t["expected"] == "valid")
        c.rect(60, y, 1630, 54, "#ffffff", "#d8d6ce", 8, 1)
        c.text(76, y + 35, t["file"], 20, 400, maxw=740)
        c.text(840, y + 35, t["expected"], 20, 400, maxw=210)
        c.rect(1080, y + 8, 290, 38, REAL if ok else RED_FILL, "#000000", 8, 1)
        c.text(1225, y + 34, ("conforms" if t["profile"] == "conforms" else "rejected") + (" as expected" if ok else " UNEXPECTED"), 18, 500, "#ffffff", "middle", 270)
        if "dcat_ap_301" in t:
            c.rect(1400, y + 8, 290, 38, REAL if t["dcat_ap_301"] == "conforms" else RED_FILL, "#000000", 8, 1)
            c.text(1545, y + 34, "%s (%s)" % (t["dcat_ap_301"], t["dcat_ap_source"]), 18, 500, "#ffffff", "middle", 270)
        else:
            c.text(1545, y + 34, "not applicable", 18, 400, MUTED, "middle", 270)
        y += 62
    c.note("Source: dist/test_results.json. “recorded” means the official DCAT-AP shapes were not run in this build (see data/dcatap_results.json).")
    return c


RED_FILL = "#b91c1c"


def main():
    ensure_dirs()
    m = load()
    figs = {"pipeline": fig_pipeline(m), "model": fig_model(m), "crosswalk": fig_crosswalk(m), "tests": fig_tests(m)}
    for ex in m["examples"]:
        figs["example-" + ex["file"].replace(".ttl", "")] = fig_example(m, ex)
    for name in sorted(figs):
        svg = figs[name].svg()
        (IMG / (name + ".svg")).write_text(svg, encoding="utf-8", newline="\n")
        (IMG / (name + ".png")).write_bytes(to_png(svg))
    print("figures: %d SVG + PNG in docs/visuals/img/" % len(figs))


if __name__ == "__main__":
    main()
