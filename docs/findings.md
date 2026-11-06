---
layout: default
title: Findings
---

# Findings from the example datasets

Examples: `examples/rdf/valid/mdse-coin-001.ttl` (TA2), `kur-restoration-002.ttl` (TA4), `denkmal-001.ttl` (TA1).
All three conform to the profile shapes and to the official DCAT-AP 3.0.1 SHACL. They cover only part of each
source standard; they test the model, they do not replace the field-by-field mapping in the workbook.

## Resolved in this round

- KuR-MDS 4.7 and 4.8: `HazardAssessmentEvent`, `MonitoringEvent` and `recommendation` on the object.
- Heritage K23, K24 and K19 to K22: `ObjectGeometry` (`locn:Geometry` with WKT, reference system, positional accuracy),
  used through `ObjectLocation`. Locations now carry `oc:ObjectLocation` as an additional type.
- Heritage K08 to K14: `dating` on the object (`Dating`: period, epoch, derived flag, note, uncertainty). K37: `source_system` on the dataset. K33: `no_further_findings_expected`. K26/K27: translocation as a `MoveEvent` with `event_type`.
- KuR-MDS damage grade, completeness, stability: `damage_degree`, `completeness`, `stability` on the condition assessment. Environmental values: `has_quantitative_attribute` on the monitoring event.
- Language-tagged literals were rejected by the generated SHACL; fixed in `tools/postprocess_shacl.py`.

## Still not in the profile

| Source fields | Gap |
|---|---|
| Units of measured values | the DCAT-AP+ `QuantitativeAttribute` does have a unit (`qudt:unit`, a `DefinedTerm` bound to the QUDT unit vocabulary); the unit must be a typed node, not a bare IRI. Tested with weight (coin) and humidity (monitoring) |
| `geodcatap:referenceSystem` | checked against GeoDCAT-AP 3.1.0 SHACL (2026-11-06): defined on `dcat:Dataset`, `Distribution`, `DatasetSeries`, `Catalog` and `DataService` (range `skos:Concept`), not on `locn:Geometry`. Use on `ObjectGeometry` is a marked extension; a dataset-level `referenceSystem` is the conformant export |
| LinkML/JSON Schema validation of BCE dates | `PeriodOfTime.start_date` has range `date` in DCAT-AP+; the RDF examples use `xsd:gYear` for BCE years and pass the SHACL, but the YAML instances would not |

## Tooling

- Negative years (BCE) in `xsd:date` or `xsd:gYear` are valid XSD 1.1, but rdflib and owlrl cannot convert them.
  The checks pass; the warnings are silenced in the test scripts.
