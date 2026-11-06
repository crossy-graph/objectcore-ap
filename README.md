# ObjectCore-AP

LinkML application profile for the **Object Core Metadata Profile (OCMDP)** of NFDI4Objects. It is a formal
**extension of DCAT-AP 3.0.1**, built on the DCAT-AP+ schema (nfdi-de, pinned commit, see
`src/objectcore_ap/schema/vendor/README.md`). The core comes exclusively from the DCAT-AP family; everything else is declared
as an extension and mapped to CIDOC CRM and its extensions.

Focus: events and object biography (production, find, sampling, measurement, digitisation, condition assessment, hazard
assessment, monitoring, conservation, acquisition, custody transfer, move, provenance research, publication or exhibition),
each with time span, place, participants with roles, uncertainty and evidence.

Documentation and visualisation of the whole chain, from the task-area communities to the DCAT-AP export, are generated into
[`docs/`](docs/) (GitHub Pages) from the current data of every build.

## Quick start (Windows cmd)

```
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && python main.py
```

`python main.py` is the only entry point. Useful options: `--list`, `--only figures`, `--from model`, `--skip test`,
`--dry-run`, `--strict`. To also run the official DCAT-AP 3.0.1 shapes, clone SEMICeu/DCAT-AP and add
`--dcatap C:\path\to\DCAT-AP\releases\3.0.1\shacl`.

| Step | What it does | Writes |
|---|---|---|
| `generate` | LinkML profile to JSON Schema, SHACL, OWL; SHACL post-processing | `dist/` |
| `test` | validates the RDF examples against the profile shapes (and optionally the official DCAT-AP shapes) | `dist/test_results.json` |
| `model` | condenses profile, crosswalk, examples and test results | `dist/model.json` |
| `figures` | draws the figures (SVG and PNG, Fira Sans) | `docs/visuals/img/` |
| `site` | writes the documentation and figure pages | `docs/` |

The output is deterministic: two runs in a row leave `git status` clean.

## Status

| Item | State |
|---|---|
| Namespace `https://w3id.org/nfdi4objects/objectcore-ap/` | **provisional**, not yet registered at w3id.org |
| CIDOC CRM / CRMsci / CRMdig / CRMinf | checked 2026-11-06: CRM 7.1.3, CRMsci 3.2, CRMdig 5.0, CRMinf 1.0 |
| `geodcatap:referenceSystem` | defined by GeoDCAT-AP 3.1.0 on datasets, distributions, catalogues and data services; its use on a geometry is an extension |
| DCAT-AP+ | no official release; pinned commit 198ac222 (2026-11-01) |
| Super-property SP-30 | not in the profile; to be added when a community needs it |

Open work and decisions are tracked in [`PRIMER.md`](PRIMER.md) (German working plan).

## Layout

| Path | Content |
|---|---|
| `src/objectcore_ap/schema/objectcore_ap.yaml` | the profile (single source of truth) |
| `src/objectcore_ap/schema/vendor/` | pinned DCAT-AP+ import |
| `examples/rdf/valid`, `examples/rdf/invalid` | RDF instances used by the tests |
| `examples/valid`, `examples/invalid` | YAML instances |
| `data/crosswalk.csv` | super-property to profile element to DCAT-AP export slot |
| `data/dcatap_results.json` | recorded result of the official DCAT-AP 3.0.1 shapes |
| `content/` | prose that goes onto the site (findings) and internal drafts |
| `py/` | step modules, `objectcore_utils.py`, `svgkit.py`, `site_kit.py` |
| `tools/postprocess_shacl.py` | workaround for DCAT-AP+ SHACL weaknesses (see below) |
| `assets/fonts/` | Fira Sans (SIL OFL) for the figures and the site |
| `dist/` | generated: JSON Schema, SHACL, OWL, model, test results |
| `docs/` | generated: GitHub Pages site |

## Export to DCAT-AP 3.0.1

Instances are typed with both `oc:ObjectCoreDataset` and `dcat:Dataset` (likewise for distributions). The valid RDF examples
conform to the official DCAT-AP 3.0.1 SHACL shapes; extension properties (events, biography, uncertainty) are not constrained
by DCAT-AP and pass through.

## Known findings on DCAT-AP+

Several classes share a `class_uri`; overloaded predicates carry conflicting ranges; the `rdf_type` slot is rendered as
`sh:class DefinedTerm`; `was_generated_by` is required, which is stricter than DCAT-AP. `tools/postprocess_shacl.py` keeps
only profile shapes, merges property shapes that share a path, accepts language-tagged strings and writes blank nodes with
content-derived ids so that the output is byte-stable. Drafts of the upstream issues are in `content/`; they are not filed.

## Licence

Code: MIT, see `LICENSE`. Vendored DCAT-AP+: see `src/objectcore_ap/schema/vendor/LICENSE_dcat-ap-plus`. Fira Sans: SIL OFL 1.1
(`assets/fonts/OFL.txt`).
