"""Step model: condense the current profile, crosswalk, examples and test results into dist/model.json.

All figures and pages are drawn from this file, so they always show the data of the current build.
"""
import csv
import json
import pathlib
import sys

import rdflib
import yaml
from rdflib.namespace import DCTERMS, RDF, SKOS

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from objectcore_utils import DATA, DIST, EXAMPLES, RELEASE, SCHEMA, ensure_dirs, write_json  # noqa: E402

OC = rdflib.Namespace("https://w3id.org/nfdi4objects/objectcore-ap/")
DCAT = rdflib.Namespace("http://www.w3.org/ns/dcat#")
SCHEMA_ORG = rdflib.Namespace("http://schema.org/")

EVENT_BASE = ["ObjectEvent"]


def label(g, n):
    for p in (SCHEMA_ORG.name, SKOS.prefLabel, DCTERMS.title, rdflib.FOAF.name):
        v = g.value(n, p)
        if v is not None:
            return str(v)
    return str(n).rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def short(uri):
    u = str(uri)
    for pre, base in (("crm", "http://www.cidoc-crm.org/cidoc-crm/"), ("crmsci", "http://www.cidoc-crm.org/extensions/crmsci/"),
                      ("crmdig", "http://www.cidoc-crm.org/extensions/crmdig/"), ("crminf", "http://www.cidoc-crm.org/extensions/crminf/"),
                      ("oc", str(OC)), ("prov", "http://www.w3.org/ns/prov#")):
        if u.startswith(base):
            return f"{pre}:{u[len(base):]}"
    return u


def schema_model():
    s = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    classes = []
    for name in sorted(s["classes"]):
        c = s["classes"][name]
        classes.append({
            "name": name, "class_uri": c.get("class_uri", ""), "is_a": c.get("is_a", ""), "mixins": c.get("mixins", []),
            "description": " ".join(str(c.get("description", "")).split()),
            "slots": list(c.get("slots", [])), "slot_usage": sorted(c.get("slot_usage", {}))})
    slots = [{"name": n, "slot_uri": s["slots"][n].get("slot_uri", ""), "range": s["slots"][n].get("range", ""),
              "description": " ".join(str(s["slots"][n].get("description", "")).split())} for n in sorted(s["slots"])]
    return classes, slots


def example_model(path):
    g = rdflib.Graph().parse(str(path))
    ds = next(iter(sorted(g.subjects(RDF.type, OC.ObjectCoreDataset))), None)
    out = {"file": path.name, "triples": len(g), "dataset": label(g, ds) if ds else "", "object": "", "object_types": [],
           "slots_used": sorted({short(p) for p in g.predicates() if str(p).startswith(str(OC))}),
           "events": [], "has_dating": False, "has_geometry": False, "has_uncertainty": False}
    objs = sorted(g.objects(ds, DCTERMS.subject)) if ds else []
    for o in objs[:1]:
        out["object"] = label(g, o)
        out["object_types"] = sorted(short(t) for t in g.objects(o, RDF.type) if str(t) != "http://www.w3.org/ns/prov#Entity")
        out["has_dating"] = (o, OC.dating, None) in g
        out["has_geometry"] = any(True for _ in g.objects(None, rdflib.URIRef("http://www.opengis.net/ont/geosparql#asWKT")))
        out["has_uncertainty"] = any(True for _ in g.subject_objects(OC.uncertainty))
        for e in sorted(set(g.objects(None, OC.biography))):
            types = sorted(short(t) for t in g.objects(e, RDF.type) if str(t) != "http://www.w3.org/ns/prov#Activity")
            et = g.value(e, DCTERMS.type)
            out["events"].append({"id": str(e).rsplit("/", 1)[-1], "types": types, "event_type": label(g, et) if et else "",
                                  "description": str(g.value(e, DCTERMS.description) or "")})
    return out


def main():
    ensure_dirs()
    classes, slots = schema_model()
    event_classes = [c["name"] for c in classes if c["name"] != "ObjectEvent" and (c["is_a"] in EVENT_BASE or "ObjectEventMixin" in c["mixins"])]
    with open(DATA / "crosswalk.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    tests = json.loads((DIST / "test_results.json").read_text(encoding="utf-8"))["results"] if (DIST / "test_results.json").exists() else []
    examples = [example_model(p) for p in sorted((EXAMPLES / "valid").glob("*.ttl"))]
    model = {
        "release": RELEASE, "classes": classes, "slots": slots, "event_classes": sorted(event_classes),
        "crosswalk": rows, "examples": examples, "tests": tests,
        "counts": {"classes": len(classes), "slots": len(slots), "event_classes": len(event_classes),
                   "super_properties": len(rows), "examples_valid": len(examples),
                   "examples_invalid": len(list((EXAMPLES / "invalid").glob("*.ttl")))}}
    write_json(DIST / "model.json", model)
    print("model:", json.dumps(model["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
