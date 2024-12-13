# Illinois Wells - Illinois State Geological Survey

## Overview

* **Name of dataset:** ISGS Wells
* **Source Agency:** Illinois State Geological Survey
* **Data Source Location:** [Illinois Water Water and Related Wells ESRI Rest server](https://maps.isgs.illinois.edu/arcgis/rest/services/ILWATER/Water_and_Related_Wells2/MapServer)
* **Metadata description:** [IL Water map interface](https://prairie-research.maps.arcgis.com/apps/webappviewer/index.html?id=e06b64ae0c814ef3a4e43a191cb57f87)
* **Format:** GEOJSON (pulled via il-get-data-geoserver.py script)
* **Data update interval** last updated on 11/3/2024 and contains 383413 records.
* **Location of triples:** 

## Raw Data Attributes

### Water and Related Wells

**code:** il-wells.py

| Attributes   | Description    | Lift to graph | Ontology Property|
|--------------|----------------|---------------|------------------|
| OBJECTID     | *              |               |                  |
| API_NUMBER   | * - used as unique identifier  | Yes           | il_isgs:ISGS-Well iri|
| ISWSPNUM     | 152051 of 379496     | Yes     | il_isgs:hasISWSId xsd:string |
| STATUS       |                | Yes           | il_isgs:ISGS-Well il_isgs:wellPurpose il_isgs:WellPurpose   |
| STATUSLONG   | Status description   | Yes     | il_isgs:wellPurpose rdfs:label   |
| LATITUDE     | *              | Yes           | geo:Geometry geo:asWKT     |
| LONGITUDE    | *              | Yes           | geo:Geometry geo:asWKT       |
| LOCATION     | ?mapsheet      |   |      |
| OWNER        |                | Yes           |  il_isgs:ISGS-Well il_isgs:hasOwner xsd:string    |
| FARM_NAME    | Well Name      | Yes           |      |
| WELL         | matches FARM_NAME    |   |      |
| DRILLER      | Drilling company     |   |      |
| DATE_DRILLED |                | ? |      |
| ELEVATION    |                | ? |      |
| ELEVREF      |                | ? |      |
| ELEVREFLONG  | Elevation reference description  | ? |      |
| TOTAL_DEPTH  |                | Yes           |      |
| WFORMATION   | Formation      | ? |      |
| FORM_TOP     | Formation Top  | ? |      |
| FORM_BOTTOM  | Formation Bottom  | ? |      |
| PUMPGPM      | Pumping Rate    | Yes           |      |
| FLAG_LAS     | Digitized Well Log   |   |      |
| FLAG_LOG     | Scanned Well Log     |   |      |
| FLAG_CORE    | Core at ISGS         | ? |      |
| FLAG_SAMPLES | Samples at ISGS      | ? |      |
| DataSummary  | Data summary sheet (url to  pdf) | ? |      |
