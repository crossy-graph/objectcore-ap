# PRIMER — ObjectCore-AP

Arbeitsplan für das Repository `crossy-graph/objectcore-ap`. Dieses Dokument wird zu Beginn jedes Chats hochgeladen und am Ende zurückgeschrieben. Es ist deutsch; alles andere im Repository ist britisches Englisch.

## Teil A — Immer gültig

### A1 Ausgangslage

| Was | Wo | Rolle |
|---|---|---|
| Profil (LinkML) | `src/objectcore_ap/schema/objectcore_ap.yaml` | einzige Quelle der Wahrheit für das Profil |
| DCAT-AP+ (nfdi-de) | `src/objectcore_ap/schema/vendor/` | gepinnt auf Commit 198ac222 (2026-11-01), kein offizielles Release |
| Beispiele RDF | `examples/rdf/valid`, `examples/rdf/invalid` | 5 gültige, 5 ungültige; Testgrundlage |
| Crosswalk | `data/crosswalk.csv` | SP-01..SP-31 → Profilelement → DCAT-AP-Export |
| Arbeitsmatrix | Google Sheet „ObjectCore-AP Arbeitsmatrix“ (Drive N4O) | Communities, Register, Core_Vorschlag, Beschlüsse |
| Wissensbasis | Google Doc im Drive-Ordner | Stand für die AG |

**Befunde (geprüft 2026-11-06)**

- DCAT-AP+ teilt `class_uri` zwischen Klassen (`Dataset`/`AnalysisDataset` → `dcat:Dataset`; `Entity`, `EvaluatedEntity` u. a. → `prov:Entity`). `gen-shacl` erzeugt dadurch widersprüchliche Shapes auf demselben Ziel. Workaround: eigene `class_uri` (`oc:ObjectCoreDataset`) und `tools/postprocess_shacl.py`, das nur Profil-Shapes behält und Property-Shapes gleichen Pfads per `sh:or` zusammenführt.
- `rdf_type` wird als `sh:class DefinedTerm` auf `rdf:type` erzeugt und lehnt gewöhnliche Typisierung ab; die Shapes werden im Postprocessing entfernt.
- `Dataset.was_generated_by` ist in DCAT-AP+ Pflicht, strenger als DCAT-AP 3.0.1; im Profil nur empfohlen.
- Sprach-Literale (`"…"@de`) fielen durch `xsd:string`; das Postprocessing erweitert auf `xsd:string | rdf:langString`.
- `geodcatap:referenceSystem` ist in GeoDCAT-AP 3.1.0 auf Dataset, Distribution, DatasetSeries, Catalog und DataService definiert, nicht auf `locn:Geometry`. Die Verwendung auf `ObjectGeometry` ist eine markierte Erweiterung.
- BCE-Jahre sind als `xsd:gYear` gültig (XSD 1.1), rdflib/owlrl können sie nicht umrechnen; Warnungen sind unterdrückt. In DCAT-AP+ hat `PeriodOfTime.start_date` den Bereich `date`, die YAML-Instanzen vertragen BCE daher nicht.
- CRM-Erweiterungen geprüft: CRMsci 3.2, CRMdig 5.0, CRMinf 1.0 (Namensraum `http://www.cidoc-crm.org/extensions/crminf/`), CRM-Kern gegen 7.1.3.
- **Korrektur:** Früher hieß es, `QuantitativeAttribute` habe keine Einheit. Falsch: DCAT-AP+ bindet `qudt:unit` (getypter Knoten) bereits.

### A2 Zielbild

```
Communities (TA1..TA4) -> Super-Properties (31) -> Core (A/B/C) -> Profil (LinkML)
   -> dist/ (JSON Schema, SHACL, OWL) -> Tests (SHACL) -> Export als DCAT-AP 3.0.1
                                      -> docs/ (Visualisierung, Doku)
```

Eigenschaften, deren Verletzung erkennbar ist:

1. Jede Instanz mit `oc:ObjectCoreDataset` ist zugleich ein gültiges `dcat:Dataset` nach offiziellem DCAT-AP-3.0.1-SHACL.
2. Der Core stammt ausschließlich aus der DCAT-AP-Familie; alles andere ist als Erweiterung gekennzeichnet und auf CRM abgebildet.
3. Ein zweiter Lauf von `python main.py` ändert keine Datei (`git status` sauber).
4. Jede Zahl auf den Seiten unter `docs/` stammt aus `dist/model.json`.

### A3 Querschnittsregeln

- Rohdaten (Beispiele, Crosswalk, Vendor) werden nicht von Skripten verändert; Erzeugtes liegt in `dist/` und `docs/`.
- Kein `datetime.now()` in Generatoren; Datum kommt aus `RELEASE`/`RELEASE_DATE` in `py/objectcore_utils.py`.
- Zwei Läufe hintereinander, `git status` bleibt sauber.
- Netzwerkzugriff nur in Schritten, die explizit holen (derzeit keiner); alles andere läuft offline.
- Core nur aus der DCAT-AP-Familie; Erweiterungen mit eigenem Präfix `oc:` und `*_mappings` auf CRM.
- Ein Thema pro Chat, ein Repository pro Chat. Windows `cmd`, zusammengehörige Befehle in einer Zeile mit `&&`.
- Offene Entscheidungen als interaktives Formular mit Freitextfeld.

### A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Core | ausschließlich DCAT-AP-Familie, alles andere Erweiterung/Mapping | 2026-11-06 |
| Exportziel | DCAT-AP 3.0.1, als „ObjectCore-AP extension“ | 2026-11-06 |
| Task Areas | 2 Task Areas je Super-Property als Schwelle (B-03) | 2026-11-06 |
| Vorarbeit (ChatGPT-Items) | verworfen; `Core_Vorschlag` ersetzt sie (B-04) | 2026-11-06 |
| Erweiterungsschicht | ja (B-05) | 2026-11-06 |
| Datensatz | Katalogeintrag zum Objekt (B-08) | 2026-11-06 |
| Core-Ebenen | A Datensatz, B Objekt, C Ereignis | 2026-11-06 |
| Ereignisklassen | 14 eigene Klassen | 2026-11-06 |
| Geometrie | `locn:Geometry` als Ressource mit WKT, CRS beibehalten | 2026-11-06 |
| Zustandsbegriffe | Begriffe plus Messwerte (`QuantitativeAttribute`) | 2026-11-06 |
| SP-30 (Software, Dienst, Lehrmaterial) | zurückgestellt, bis eine Community es braucht | 2026-11-06 |
| Weitere Minimalschemata (TA3 u. a.) | vorerst nicht | 2026-11-06 |
| Upstream-Issues an DCAT-AP+ | nicht einstellen; Entwürfe in `content/` | 2026-11-06 |
| Namensraum w3id.org | Registrierung per PR durch Flo/N4O; bis dahin provisorisch | offen |
| Lizenz Repository | MIT (Vorlage der Familie), Profil CC-BY-4.0 laut Schema | Vorschlag |

### A5 Was in welchem Chat hochgeladen wird

Dieses `PRIMER.md` plus ein Bundle ohne Erzeugtes:

```
robocopy . %TEMP%\oc-bundle /E /XD .git .venv __pycache__ dist docs && powershell Compress-Archive -Path %TEMP%\oc-bundle\* -DestinationPath oc-bundle.zip -Force
```

Nicht hochladen: `.venv/`, `.git/`, `dist/`, `docs/` (alles reproduzierbar), Zugangsdaten.

### A6 IRI-Landkarte

| Pfad | Inhalt | Ziel des Redirects | Status |
|---|---|---|---|
| `https://w3id.org/nfdi4objects/objectcore-ap/` | Namensraum `oc:` | GitHub Pages `https://crossy-graph.github.io/objectcore-ap/` | geplant |

Offen: w3id-PR, Content Negotiation (Turtle/OWL/SHACL aus `dist/`).

## Teil B — Schrittübersicht

| ID | Schritt | Repo | hängt ab von | Status |
|---|---|---|---|---|
| S0 | Festlegungen (Core, Export, Lizenz, Namensraum) | objectcore-ap | – | erledigt 2026-11-06 (Lizenz und w3id offen) |
| S1 | Skelett: `main.py`, Utils, Schritte, Orchestrator | objectcore-ap | S0 | erledigt 2026-11-06 |
| S2 | Profil und Beispiele (generate, test) | objectcore-ap | S1 | erledigt 2026-11-06 |
| S3 | Visualisierung und Seiten (model, figures, site) | objectcore-ap | S2 | erledigt 2026-11-06 |
| S4 | Push, GitHub Pages aktivieren, CI | objectcore-ap | S3 | offen |
| S5 | YAML-Beispiele auf neue Slots; BCE in YAML | objectcore-ap | S2 | offen |
| S6 | Dataset-weites `referenceSystem` im Export | objectcore-ap | S2 | offen |
| S7 | w3id-Registrierung | N4O | S4 | offen |
| S8 | SP-30 und weitere Minimalschemata | objectcore-ap | Bedarf einer Community | offen |

S5, S6 und S8 sind voneinander unabhängig und laufen in beliebiger Reihenfolge; S7 braucht nur die Pages-URL aus S4.

## Teil C — Die Schritte

## S1 — Skelett

**Ziel:** Das Repository wird von genau einem Befehl getrieben: `python main.py`.

**Uploads:** keine.

`main.py` mit `--list`, `--only`, `--from`, `--skip`, `--dry-run`, `--strict`, `--dcatap`; Schritte als Module in `py/step_*.py`, jedes einzeln lauffähig; Konstanten in `py/objectcore_utils.py`.

**Abnahme:** `python main.py --list` nennt fünf Schritte; `python main.py` läuft durch.

### Erledigt 2026-11-06

Fünf Schritte: generate, test, model, figures, site. Das SHACL-Postprocessing erzeugte zufällige Blank-Node-Ids; behoben mit kanonischem Graphen (siehe S2).

## S2 — Profil und Beispiele

**Ziel:** Profil bauen, Beispiele testen.

**Abnahme:** `python main.py --only generate` und `--only test`: 5 gültige Beispiele konform, 5 ungültige abgelehnt. Mit `--dcatap <Pfad>` zusätzlich offizielles DCAT-AP-3.0.1-SHACL für die gültigen.

### Erledigt 2026-11-06

26 Klassen, 40 Slots, 14 Ereignisklassen. Offizielles SHACL: alle 5 gültigen konform (festgehalten in `data/dcatap_results.json`, ohne `--dcatap` als „recorded“ markiert).

## S3 — Visualisierung und Seiten

**Ziel:** Ende-zu-Ende-Darstellung von der Community bis zum Export, aus den aktuellen Daten, als GitHub-Pages-Seite.

**Abnahme:** zwei Läufe, `git status` sauber; `docs/visuals/index.html` zeigt 9 Abbildungen; jede Abbildung per Auge geprüft (kein Text läuft über, keine Pfeilspitze verdeckt).

### Erledigt 2026-11-06

Abbildungen: Pipeline, Profilmodell, Crosswalk, Tests, fünf Objektbiografien. Text wird mit Fira-Sans-Metrik gemessen; zu langer Text bricht den Lauf ab.

## S4 — Push, Pages, CI

**Ziel:** Repository veröffentlicht, Pages aus `docs/`, CI mit `python main.py --strict`.

**Uploads:** keine. **Voraussetzung:** Claude-GitHub-App für die Organisation `crossy-graph` installiert (https://github.com/apps/claude/installations/select_target) oder Push durch Flo.

**Abnahme:** Pages-URL liefert die Übersichtsseite; CI grün; zweiter CI-Lauf ohne Diff.

## Teil D — Offene Punkte

- Lizenzfrage: MIT für Code (Familienvorlage) und CC-BY-4.0 für das Profil: in einem Formular klären.
- Zählung der Core-Elemente (22 im Sheet `Core_Vorschlag`) ist noch nicht im Repository abgebildet; die Pipeline-Abbildung nennt nur die Ebenen A, B, C.
- Verifikation DCAT-3.0-Registerzeilen R-0151..R-0195 im Sheet; Spalte L (Lücken).
- MDSE und KuR-MDS sind nur teilweise Feld für Feld abgedeckt.
