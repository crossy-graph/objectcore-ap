---
layout: default
title: Profile
---

# Profile

Generated from `src/objectcore_ap/schema/objectcore_ap.yaml`.

## Classes

| Class | RDF class | Parent | Description |
|---|---|---|---|
| AcquisitionEvent | crm:E8_Acquisition | ObjectEvent | Change of ownership (CRM E8 Acquisition). |
| AgentInRole | prov:Association |  | An agent together with the role in which it took part in an event. |
| ConditionAssessmentEvent | crm:E14_Condition_Assessment | ObjectEvent | Assessing the condition of an object (CRM E14 Condition Assessment). |
| ConservationEvent | crm:E11_Modification | ObjectEvent | Conservation or restoration treatment (CRM E11 Modification, E87 Curation Activity). |
| CustodyTransferEvent | crm:E10_Transfer_of_Custody | ObjectEvent | Change of custody without change of ownership (CRM E10 Transfer of Custody). |
| Dating | oc:Dating |  | Dating of an object without a single production event. |
| DigitalRepresentation | crmdig:D1_Digital_Object | EvaluatedEntity | A digital object (image, 3D model, scan) that represents a physical object. |
| DigitisationEvent | crmdig:D2_Digitization_Process | DataGeneratingActivity | Digitising an object (CRMdig D2 Digitization Process, DCAT-AP+ DataGeneratingActivity). |
| FindEvent | crmsci:S19_Encounter_Event | ObjectEvent | Finding or excavating an object (CRMsci S19 Encounter Event, CRMarchaeo A9). |
| HazardAssessmentEvent | oc:HazardAssessmentEvent | ObjectEvent | Assessing hazards to an object and the protective measures taken (KuR-MDS 4.7). |
| MeasurementEvent | crmsci:S21_Measurement | DataGeneratingActivity | Measurement or analysis that produces a dataset (CRMsci S21 Measurement, DCAT-AP+ DataGeneratingActivity). |
| MonitoringEvent | oc:MonitoringEvent | ObjectEvent | Monitoring of conditions around an object, with measured values (KuR-MDS 4.8). Values go into has_quantitative_attribute. |
| MoveEvent | crm:E9_Move | ObjectEvent | Change of physical location (CRM E9 Move). |
| ObjectCoreDataset | oc:ObjectCoreDataset | Dataset | A dcat:Dataset (DCAT-AP 3.0.1) that describes an object, a sample or events of an object biography. Adds the mandatory elements of the NFDI Core Metadata Profile (identifier, title, creator, resource type, licence via the distribution) on top of DCAT-AP. |
| ObjectCoreDistribution | oc:ObjectCoreDistribution | Distribution | A distribution that always carries a licence (NFDI Core Metadata Profile, MUST). |
| ObjectEvent | crm:E5_Event | Activity | An event in the biography of an object. Concrete subclasses fix the kind of event; the optional type slot refines it with a term from a controlled vocabulary. |
| ObjectEventMixin |  |  | Slots shared by all events of an object biography. |
| ObjectGeometry | oc:ObjectGeometry | Geometry | A geometry resource (locn:Geometry) with WKT, coordinate reference system and positional accuracy. |
| ObjectLocation | oc:ObjectLocation | Location | A dcterms:Location whose geometry is an ObjectGeometry. |
| PhysicalObject | crm:E18_Physical_Thing | EvaluatedEntity | The physical object, specimen or monument that datasets and events are about. |
| ProductionEvent | crm:E12_Production | ObjectEvent | Making or changing an object (CRM E12 Production, E11 Modification). |
| ProvenanceResearchEvent | crminf:I15_Provenance_Assessment | ObjectEvent | Research that establishes or revises provenance statements (CRM E13 Attribute Assignment, CRMinf I15). |
| PublicationExhibitionEvent | crm:E7_Activity | ObjectEvent | Publication or exhibition of an object (CRM E65 Creation, E7 Activity). |
| Sample | crmsci:S13_Sample | PhysicalObject | A sample taken from a physical object, for example for an analysis. |
| SamplingEvent | crmsci:S2_Sample_Taking | ObjectEvent | Taking a sample from an object (CRMsci S2 Sample Taking). |
| Uncertainty | oc:Uncertainty |  | A qualified statement of uncertainty about one aspect of an event or object description. |

## Slots

| Slot | Predicate | Range | Description |
|---|---|---|---|
| agent | prov:agent | Agent | The agent in a participation. |
| aspect |  | UncertaintyAspectEnum | Which aspect of the description is uncertain. |
| assessed_condition | oc:assessedCondition | DefinedTerm | The condition state found in a condition assessment. |
| biography | oc:biography | Activity | The events in the life of an object (production, find, conservation, transfer, move, provenance research, and so on). Range is Activity so that both ObjectEvent subclasses and the DCAT-AP+ data-generating events (MeasurementEvent, DigitisationEvent) can be listed in one biography. |
| completeness | oc:completeness | DefinedTerm | Completeness of the object found in a condition assessment. |
| current_keeper | oc:currentKeeper | Agent | The agent that currently has custody of the object. |
| current_location | oc:currentLocation | ObjectLocation | Where the object is now. |
| damage_degree | oc:damageDegree | DefinedTerm | Degree of damage found in a condition assessment. |
| dated_period | dcterms:temporal | PeriodOfTime | Earliest and latest date of the dating (ISO 8601-2 / EDTF where the source uses it). |
| dating | oc:dating | Dating | The dating of an object that has no single production event (for example a monument): absolute period, epoch and whether the absolute dates were derived from the epoch. Use a ProductionEvent where the making is documented. |
| derived_from_epoch | oc:derivedFromEpoch | boolean | True if the absolute dates were derived automatically from the epoch. |
| epoch | oc:epoch | DefinedTerm | Relative dating as an epoch, taken from a controlled vocabulary. |
| event_type | dcterms:type | DefinedTerm | Refines the kind of event with a term from a controlled vocabulary (for example translocation for a move). |
| evidence | dcterms:source | Entity | The source or document on which an event statement is based. |
| finding | oc:finding | string | The conclusion of a provenance research event. |
| hazard_type | oc:hazardType | DefinedTerm | The kind of hazard found in a hazard assessment. |
| level |  | UncertaintyLevelEnum | Degree of certainty. |
| material | oc:material | DefinedTerm | Material of a physical object or sample, taken from a controlled vocabulary. |
| monitored_condition | oc:monitoredCondition | DefinedTerm | A condition that is checked in a monitoring event (for example humidity). |
| moved_from | oc:movedFrom | Location | The place the object was moved from. |
| moved_to | oc:movedTo | Location | The place the object was moved to. |
| no_further_findings_expected | oc:noFurtherFindingsExpected | boolean | True if no further findings are to be expected at the site of the object. |
| note | skos:note |  | Free-text explanation of the uncertainty. |
| participation | prov:qualifiedAssociation | AgentInRole | An agent taking part in an event, with the role in which it acted. |
| positional_accuracy | oc:positionalAccuracy |  | How exactly the geometry locates the object (for example "exact", "municipality level"). Free text; use uncertainty for a qualified statement. |
| protective_measure | oc:protectiveMeasure | DefinedTerm | A protective measure taken against a hazard. |
| recommendation | oc:recommendation |  | Handling, presentation, packaging, transport or storage recommendations for the object. |
| reference_system | geodcatap:referenceSystem | Concept | The coordinate reference system of the geometry, as a concept from the EPSG register (for example EPSG:25832). GeoDCAT-AP 3.1.0 defines geodcatap:referenceSystem on datasets, distributions, catalogues and data services; the use on a geometry is an extension. |
| represents | dcterms:subject | PhysicalObject | The physical object that a digital representation stands for. |
| role | dcat:hadRole | DefinedTerm | The role in which the agent acted, taken from a controlled vocabulary. |
| sampled_from | oc:sampledFrom | PhysicalObject | The object from which a sample was taken. |
| source_system | oc:sourceSystem |  | Name of the system from which the record was exported. |
| stability | oc:stability | DefinedTerm | Stability of the object found in a condition assessment. |
| time_span | dcterms:temporal | PeriodOfTime | The period during which an event took place (CRM P4 has time-span). |
| took_place_at | prov:atLocation | ObjectLocation | The place where an event happened (CRM P7 took place at). Not the spatial coverage of a dataset. |
| transferred_from | oc:transferredFrom | Agent | The agent that gave up title or custody. |
| transferred_to | oc:transferredTo | Agent | The agent that received title or custody. |
| treatment | oc:treatment | DefinedTerm | Treatment carried out in a conservation or restoration event. |
| uncertainty | oc:uncertainty | Uncertainty | A statement about how certain or vague an aspect of the event or object description is. |
| wkt | geo:asWKT | wktLiteral | The geometry as well-known text (point, line or polygon, also multi-geometries). |
