# Illinois Wells - Illinois State Geological Survey (ISGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | ISGS Wells |
| **Source Agency:** | [Illinois State Geological Survey](https://isgs.illinois.edu/) |
| **Data Source Location:** | [Illinois Water Water and Related Wells ESRI Rest server](https://maps.isgs.illinois.edu/arcgis/rest/services/ILWATER/Water_and_Related_Wells2/MapServer) |
| **Metadata description:** | [IL Water map interface](https://prairie-research.maps.arcgis.com/apps/webappviewer/index.html?id=e06b64ae0c814ef3a4e43a191cb57f87) |
| **Format:** | GEOJSON (pulled via il-get-data-geoserver.py script) |
| **Data update interval** | last updated on 11/3/2024 and contains 383413 records |
| **Location of triples:** |  |

## Raw Data Attributes

### Water and Related Wells

**code:** il-wells.py

| ISGS Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID     | * |  |  |  |
| API_NUMBER   | * | Yes | il_isgs:hasPrimaryStateAgencyId | used as unique identifier |
| ISWSPNUM     |  | Yes | il_isgs:hasSecondaryStateAgencyId | present for about 40% of records |
| STATUS       |  | Yes | is_isgs:hasWellPurpose | controlled vocabulary (see below) |
| STATUSLONG   | Status description | Yes |  | via controlled vocabulary (see below) |
| LATITUDE     | * | Yes | geo:Geometry/geo:asWKT |  |
| LONGITUDE    | * | Yes | geo:Geometry/geo:asWKT |  |
| LOCATION     |  | No |  | ?mapsheet |
| OWNER        |  | Yes | hyfo:hasOwner | |
| FARM_NAME    | Well Name | No |  |  |
| WELL         |  | No |  | matches FARM_NAME |
| DRILLER      | Drilling company | No |  |  |
| DATE_DRILLED |  | No |  |  |
| ELEVATION    |  | No |  |  |
| ELEVREF      |  | No |  |  |
| ELEVREFLONG  | Elevation reference description | No |  |  |
| TOTAL_DEPTH  |  | Yes | hyfo:hasTotalDepth | |
| WFORMATION   | Formation | Yes | hyfo:hasAquiferType | Need to verify this |
| FORM_TOP     | Formation Top | Yes | hyfo:hasBedrockDepth | Need to verify this |
| FORM_BOTTOM  | Formation Bottom | ? |  |  |
| PUMPGPM      | Pumping Rate | Yes | hyfo:hasYield |  |
| FLAG_LAS     | Digitized Well Log | No |  |  |
| FLAG_LOG     | Scanned Well Log   | No |  |  |
| FLAG_CORE    | Core at ISGS | No |  |  |
| FLAG_SAMPLES | Samples at ISGS | No |  |  |
| DataSummary  | Data summary sheet (url to  pdf) | No |  |  |
