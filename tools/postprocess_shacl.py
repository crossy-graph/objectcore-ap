"""Merge property shapes that share a path inside one node shape.

DCAT-AP+ reuses some predicates for different slots (for example dcterms:subject for is_about_entity and
is_about_activity, prov:used for had_input_entity and realized_plan). LinkML emits one property shape per slot,
and SHACL treats them as a conjunction, so valid data fails. This script merges such shapes into one shape per
path: sh:class alternatives become sh:or, minCount becomes the minimum, maxCount becomes the maximum (or is dropped).
Shapes of vendored classes are dropped. Property shapes on rdf:type are removed (see above).
Usage: python postprocess_shacl.py IN.ttl OUT.ttl
"""
import sys
from rdflib import Graph, BNode, Namespace, RDF, Literal, URIRef
from rdflib.collection import Collection
SH = Namespace("http://www.w3.org/ns/shacl#")
g = Graph().parse(sys.argv[1])
KEEP = ("https://w3id.org/nfdi4objects/objectcore-ap/", "http://www.cidoc-crm.org/", "http://www.w3.org/ns/prov#Association")
# Keep only the shapes of ObjectCore-AP classes. The vendored DCAT-AP+ schema gives several classes the same class_uri
# (prov:Entity, prov:Activity, prov:Agent, dcat:Dataset), so their shapes would apply to every instance of that class.
# DCAT-AP 3.0.1 conformance is checked separately with the official SHACL (see tests/).
for ns in set(g.subjects(RDF.type, SH.NodeShape)):
    targets = [str(t) for t in g.objects(ns, SH.targetClass)]
    if not any(t.startswith(KEEP) for t in targets):
        for p_, o_ in list(g.predicate_objects(ns)):
            g.remove((ns, p_, o_))
merged = 0
# DCAT-AP+ models rdf_type as a slot with range DefinedTerm; as a SHACL path rdf:type that rejects every ordinary type.
for ns in set(g.subjects(RDF.type, SH.NodeShape)):
    for ps in list(g.objects(ns, SH.property)):
        if g.value(ps, SH.path) == RDF.type:
            g.remove((ns, SH.property, ps))
for ns in set(g.subjects(RDF.type, SH.NodeShape)):
    groups = {}
    for ps in g.objects(ns, SH.property):
        path = g.value(ps, SH.path)
        if path is not None and not isinstance(path, BNode):
            groups.setdefault(path, []).append(ps)
    for path, members in groups.items():
        if len(members) < 2:
            continue
        classes = [g.value(m, SH["class"]) for m in members]
        mins = [int(g.value(m, SH.minCount) or 0) for m in members]
        maxs = [g.value(m, SH.maxCount) for m in members]
        kinds = {g.value(m, SH.nodeKind) for m in members}
        new = BNode()
        g.add((new, SH.path, path))
        if min(mins) > 0:
            g.add((new, SH.minCount, Literal(min(mins))))
        if all(x is not None for x in maxs):
            g.add((new, SH.maxCount, Literal(max(int(x) for x in maxs))))
        if len(kinds) == 1 and None not in kinds:
            g.add((new, SH.nodeKind, next(iter(kinds))))
        elif kinds:
            g.add((new, SH.nodeKind, SH.BlankNodeOrIRI))
        if all(c is not None for c in classes):
            alts = []
            for c in dict.fromkeys(classes):
                a = BNode(); g.add((a, SH["class"], c)); alts.append(a)
            head = BNode(); Collection(g, head, alts)
            g.add((new, SH["or"], head))
        for m in members:
            g.remove((ns, SH.property, m))
            for p, o in list(g.predicate_objects(m)):
                g.remove((m, p, o))
        g.add((ns, SH.property, new))
        merged += 1
# Free-text slots are generated with sh:datatype xsd:string, which rejects language-tagged literals ("Titel"@de).
# DCAT-AP and the MDSE need language tags, so accept both xsd:string and rdf:langString.
XSD_STRING = URIRef("http://www.w3.org/2001/XMLSchema#string")
widened = 0
for ps in set(g.subjects(SH.datatype, XSD_STRING)):
    if (ps, SH["or"], None) in g:
        continue
    g.remove((ps, SH.datatype, XSD_STRING))
    alts = []
    for dt in (XSD_STRING, RDF.langString):
        a = BNode(); g.add((a, SH.datatype, dt)); alts.append(a)
    head = BNode(); Collection(g, head, alts)
    g.add((ps, SH["or"], head))
    widened += 1
print(f"widened {widened} string shapes to accept language tags")
# Deterministic output: every blank node is renamed to an id derived from its content and its position (parent id and
# predicate), so two runs write byte-identical files. Identical siblings under one parent and predicate collapse into one,
# which is harmless for shapes and lists.
import hashlib
from rdflib import BNode as _B


def _h(*parts):
    return hashlib.sha1("\x1f".join(parts).encode("utf-8")).hexdigest()[:16]


_struct = {}


def struct(n):
    if n not in _struct:
        items = sorted((str(p), struct(o) if isinstance(o, _B) else o.n3()) for p, o in g.predicate_objects(n))
        _struct[n] = _h(repr(items))
    return _struct[n]


names = {}


def name(n, parent_id, pred):
    if n in names:
        return
    names[n] = _B("b" + _h(parent_id, str(pred), struct(n)))
    for p, o in g.predicate_objects(n):
        if isinstance(o, _B):
            name(o, str(names[n]), p)


for sub, pred, obj in sorted(g, key=lambda t: (t[0].n3(), t[1].n3(), t[2].n3())):
    if isinstance(obj, _B) and not isinstance(sub, _B):
        name(obj, sub.n3(), pred)
orphans = {t for tr in g for t in tr if isinstance(t, _B)} - set(names)
# Blank nodes that no named shape reaches are leftovers of the merge; they are dropped.
out = Graph()
for pfx, ns in g.namespaces():
    out.bind(pfx, ns)
for sub, pred, obj in g:
    if sub in orphans:
        continue
    out.add((names.get(sub, sub), pred, names.get(obj, obj)))
out.serialize(sys.argv[2], format="turtle", encoding="utf-8")
print(f"merged {merged} overloaded property shapes")
