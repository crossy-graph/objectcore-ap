# Draft issues for nfdi-de/dcat-ap-plus

Observed against commit 198ac22210c9b3f5ab22621c8971a9c0347b4b9f (2026-11-01) while building an application profile
(ObjectCore-AP) on top of `dcat_ap_plus.yaml` and generating SHACL with `gen-shacl --non-closed`.

## 1. Several classes share the same `class_uri`, so generated SHACL targets one class with conflicting shapes

`Dataset` and `AnalysisDataset` both declare `class_uri: dcat:Dataset`. `Entity`, `EvaluatedEntity`,
`AnalysisSourceData` and `QualitativeAttribute` all declare `class_uri: prov:Entity`. `gen-shacl` emits one node shape
per class with the same `sh:targetClass`, so a valid `dcat:Dataset` is validated against the constraints of every
class sharing the URI (for example the `was_generated_by` requirement of `Dataset`). Expected: distinct class URIs
for subclasses, or documented `rdf:type` discrimination.

Workaround in ObjectCore-AP: own `class_uri` (`oc:ObjectCoreDataset`) and a post-processing step that keeps only the
profile shapes.

## 2. Overloaded predicates carry conflicting ranges

Slots with the same `slot_uri` but different ranges in different classes (for example `dcterms:type` with `Concept` and `DefinedTerm`, `dcterms:source` with
`CatalogueRecord` and `Dataset`, `dcterms:relation`, `dcterms:hasPart`, `prov:wasGeneratedBy`) produce property shapes with the same `sh:path` and incompatible `sh:class` on one target, which
makes valid data fail. Expected: either `sh:or` over the ranges or distinct predicates.

Workaround: merge property shapes with the same path (`sh:or` over `sh:class`, minimum of `minCount`, maximum of `maxCount`).

## 3. `rdf_type` is generated as a class constraint on `DefinedTerm`

`rdf_type` has `slot_uri: rdf:type` and `range: DefinedTerm`. The generated shape demands `sh:class DefinedTerm` for the
`rdf:type` values of every instance, so ordinary typing (`a dcat:Dataset`) violates the shape. Expected: model the
classifier as a separate predicate, or exclude `rdf:type` from SHACL generation.

Workaround: remove all `rdf:type` property shapes in post-processing.

## 4. `Dataset.was_generated_by` is required, stricter than DCAT-AP 3.0.1

The slot carries the note "stricter than DCAT-AP" and `required: true`. A dataset without a generating activity is
valid DCAT-AP 3.0.1, so profiles that claim DCAT-AP conformance cannot reuse `Dataset` unchanged. Expected: optional in
the generic `Dataset`, required only in the analysis-specific subclass.

Workaround: `slot_usage: was_generated_by: required: false, recommended: true`.
