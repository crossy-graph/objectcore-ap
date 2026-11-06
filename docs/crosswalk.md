---
layout: default
title: Crosswalk
---

# Crosswalk

Super-properties from the task-area communities, the profile element that carries them and the DCAT-AP 3.0.1 export slot. The German columns are the working language of the workbook.

| SP | Name | Profile element | Cardinality | DCAT-AP 3.0.1 | Kind |
|---|---|---|---|---|---|
| SP-01 | Title / designation | ObjectCoreDataset.title; PhysicalObject.title; Activity.title | 1..* | dct:title | übernommen aus DCAT-AP |
| SP-02 | Description | ObjectCoreDataset.description; Entity.description; Activity.description | 1..* | dct:description | übernommen aus DCAT-AP |
| SP-03 | Identifier | ObjectCoreDataset.identifier (required); other_identifier on entities and events; source_system (Quellsystem) | 1..* | dct:identifier; adms:identifier | verschärft (NFDI-Pflicht) |
| SP-04 | Type / category | type (DefinedTerm), rdf_type, keyword, theme | 0..* | dct:type; dcat:keyword; dcat:theme | übernommen aus DCAT-AP und DCAT-AP+ |
| SP-05 | Language | language | 0..* | dct:language | übernommen aus DCAT-AP |
| SP-06 | Creator | ObjectCoreDataset.creator (required) | 1..* | dct:creator | verschärft (NFDI-Pflicht) |
| SP-07 | Publisher, keeper, contact | publisher; contact_point; PhysicalObject.current_keeper | 0..* | dct:publisher; dcat:contactPoint (current_keeper nur Erweiterung) | teils Erweiterung |
| SP-08 | Agents with role | participation (AgentInRole: agent + role, both required); qualified_attribution | 0..* | prov:qualifiedAssociation; prov:qualifiedAttribution | Erweiterung |
| SP-09 | Temporal coverage / time span | time_span on events; temporal_coverage on datasets; PhysicalObject.dating (Dating: period, epoch, derived flag) | 0..1 / 0..* | dct:temporal (PeriodOfTime) | übernommen, auf Ereignisse erweitert |
| SP-10 | Issue and modification date | release_date; modification_date | 0..1 | dct:issued; dct:modified | übernommen aus DCAT-AP |
| SP-11 | Spatial reference / place | took_place_at on events (FindEvent required); current_location; geographical_coverage | 0..* | prov:atLocation (Erweiterung); dct:spatial | teils Erweiterung |
| SP-12 | Reference system and accuracy | ObjectGeometry.reference_system (EPSG concept); ObjectGeometry.positional_accuracy; ObjectLocation.geometry (locn:Geometry with WKT) | 0..1 | geodcatap:referenceSystem (Erweiterung auf Geometrie); locn:geometry | Erweiterung (aus GeoDCAT-AP) |
| SP-13 | Material | PhysicalObject.material (DefinedTerm) | 0..* | oc:material (kein DCAT-AP-Slot) | Erweiterung |
| SP-14 | Measures, quantities, units | has_quantitative_attribute (DCAT-AP+) | 0..* | dct:relation (DCAT-AP+) | importiert aus DCAT-AP+ |
| SP-15 | Production / modification | ProductionEvent | 0..* | prov:Activity (crm:E12_Production) | Erweiterung |
| SP-16 | Find / excavation | FindEvent (took_place_at required) | 0..* | prov:Activity (crmsci:S19_Encounter_Event) | Erweiterung |
| SP-17 | Sampling, measurement, analysis | SamplingEvent; MeasurementEvent (DataGeneratingActivity) | 0..* | prov:wasGeneratedBy; prov:Activity | importiert aus DCAT-AP+ und erweitert |
| SP-18 | Entity under study | is_about_entity (required); PhysicalObject; Sample | 1..* | dct:subject | importiert aus DCAT-AP+ und erweitert |
| SP-19 | Instrument, method, plan | carried_out_by (Device); realized_plan (Plan) | 0..* | prov:wasAssociatedWith; prov:used (DCAT-AP+) | importiert aus DCAT-AP+ |
| SP-20 | Conservation, condition | ConservationEvent (treatment); ConditionAssessmentEvent (assessed_condition); HazardAssessmentEvent; MonitoringEvent; PhysicalObject.recommendation | 0..* | prov:Activity (crm:E11_Modification; crm:E14_Condition_Assessment) | Erweiterung |
| SP-21 | Acquisition, custody, move | AcquisitionEvent; CustodyTransferEvent; MoveEvent | 0..* | prov:Activity (crm:E8, E10, E9) | Erweiterung |
| SP-22 | Provenance research, evidence | ProvenanceResearchEvent (finding, evidence) | 0..* | prov:Activity (crminf:I15); dct:source | Erweiterung |
| SP-23 | Digitisation | DigitisationEvent; DigitalRepresentation.represents | 0..* | prov:wasGeneratedBy; dct:subject | importiert aus DCAT-AP+ und erweitert |
| SP-24 | Uncertainty and vagueness | uncertainty (Uncertainty: aspect, level, note) | 0..* | oc:uncertainty (kein DCAT-AP-Slot) | Erweiterung |
| SP-25 | Rights, licence, access | ObjectCoreDistribution.licence (required); rights; access_rights | 1 / 0..1 | dct:license; dct:rights; dct:accessRights | verschärft (NFDI-Pflicht) |
| SP-26 | Distribution, format, access | dataset_distribution (ObjectCoreDistribution: access_URL required) | 1..* | dcat:distribution | verschärft |
| SP-27 | Relations between resources | relation; source; has_part; part_of; evidence | 0..* | dct:relation; dct:source; dct:hasPart | übernommen aus DCAT-AP |
| SP-28 | Version and series | version; has_version; in_series | 0..* | dcat:version; dcat:hasVersion; dcat:inSeries | übernommen aus DCAT-AP |
| SP-29 | Conformance and quality | conforms_to | 0..* | dct:conformsTo | übernommen aus DCAT-AP |
| SP-30 | Software, service, teaching | noch nicht im Profil; Muster EPOS-DCAT-AP, DataService |  | dcat:DataService | offen |
| SP-31 | Catalogue record | record (CatalogueRecord) | 0..* | dcat:CatalogRecord | übernommen aus DCAT-AP |
