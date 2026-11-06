"""Step test: validate the RDF examples against the profile shapes (and optionally the official DCAT-AP 3.0.1 shapes).

Writes dist/test_results.json (profile shapes: run live; DCAT-AP: run live if --dcatap is given, otherwise the recorded
result in data/dcatap_results.json is carried over and marked as recorded).
"""
import argparse
import glob
import json
import logging
import pathlib
import sys

logging.disable(logging.CRITICAL)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from objectcore_utils import DATA, DIST, ROOT, ensure_dirs, write_json  # noqa: E402


def main(argv=None):
    import pyshacl
    import rdflib
    from rdflib.namespace import SH
    ap = argparse.ArgumentParser()
    ap.add_argument("--dcatap", help="path to DCAT-AP/releases/3.0.1/shacl")
    a = ap.parse_args(argv)
    ensure_dirs()
    shapes = rdflib.Graph().parse(str(DIST / "objectcore_ap.shacl.merged.ttl"))
    dshapes = None
    if a.dcatap:
        dshapes = rdflib.Graph().parse(f"{a.dcatap}/dcat-ap-SHACL.ttl")
        dshapes.parse(f"{a.dcatap}/ranges.ttl")
        for ns, ps in list(dshapes.subject_objects(SH.property)):
            if dshapes.value(ps, SH.path) is None:
                dshapes.remove((ns, SH.property, ps))
    recorded = json.loads((DATA / "dcatap_results.json").read_text(encoding="utf-8"))
    results, bad = [], 0
    for f in sorted(glob.glob(str(ROOT / "examples/rdf/*/*.ttl"))):
        p = pathlib.Path(f)
        kind = p.parent.name
        g = rdflib.Graph().parse(f)
        conforms, _, _ = pyshacl.validate(g, shacl_graph=shapes, inference="rdfs", advanced=True)
        row = {"file": f"{kind}/{p.name}", "expected": "valid" if kind == "valid" else "invalid",
               "profile": "conforms" if conforms else "violations", "triples": len(g)}
        if conforms != (kind == "valid"):
            bad += 1
        if kind == "valid":
            if dshapes is not None:
                dc, _, _ = pyshacl.validate(g, shacl_graph=dshapes, inference="none", advanced=True)
                row["dcat_ap_301"] = "conforms" if dc else "violations"
                row["dcat_ap_source"] = "run"
                if not dc:
                    bad += 1
            else:
                row["dcat_ap_301"] = recorded.get(p.name, "not recorded")
                row["dcat_ap_source"] = "recorded"
        print(("OK  " if conforms == (kind == "valid") else "FAIL"), row["file"], row["profile"],
              row.get("dcat_ap_301", ""), f"({row.get('dcat_ap_source', '')})".replace("()", ""))
        results.append(row)
    write_json(DIST / "test_results.json", {"results": results})
    if bad:
        sys.exit(f"{bad} unexpected result(s)")
    print(f"test: {len(results)} examples as expected")


if __name__ == "__main__":
    main(sys.argv[1:])
