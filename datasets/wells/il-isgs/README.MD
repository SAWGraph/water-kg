# Illinois Wells - Illinois State Geological Survey (ISGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Water and Related Wells |
| **Source Agency:** | [Illinois State Geological Survey](https://isgs.illinois.edu/) |
| **Data Source Location:** | [Illinois Water Water and Related Wells ESRI Rest server](https://maps.isgs.illinois.edu/arcgis/rest/services/ILWATER/Water_and_Related_Wells2/MapServer) |
| **Metadata description:** | [IL Water map interface](https://prairie-research.maps.arcgis.com/apps/webappviewer/index.html?id=e06b64ae0c814ef3a4e43a191cb57f87) |
| **Format:** | GEOJSON (pulled via il-get-data-geoserver.py script) |
| **Data update interval** | last updated on 11/3/2024 and contains 383413 records |
| **Location of triples:** |  |

## Schema Diagram (TO ADD)
- [*Draft* schema](https://lucid.app/lucidchart/16e658ef-6f61-4ce3-a770-0c410ecb194a/edit?viewport_loc=-1074%2C-511%2C3767%2C1853%2CssMfXgoENRPy&invitationId=inv_ea094a2c-59da-4347-b175-700b91e5623d)

**Legend description:** (TO ADD)
- 

## Code (TO ADD)
- il-wells.py
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `me_mgs:MGS_Well` | `me_mgs_data:d.MGS-Well.<WELLNO>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)

| ISGS Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID     | * | No |  |  |
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

**Notes on the data:**
- 

## Controlled Vocabularies
**List 1. STATUS: STATUSLONG**
- CROP: Outcrop
- DRIFT: Drift Mine
- DRY: Dry Hole (water well)
- DRYP: Dry Hole (water well), Plugged
- ENG: Engineering Test
- ENGP: Engineering Test, Plugged
- LUST: Leaking Underground Storage Tank
- MINER: Mineral Test
- MINERP: Mineral Test, Plugged (1)
- MONIT: Water Well Monitoring Well
- MONITP: Water Well Monitoring Well Plugged
- MSERV: Mine Service
- MSERVP: Mine Service Plugged
- MSFT: Mine Shaft
- OBS: Observation Well
- OBSP: Observation Well, Plugged
- SLOPE: Slope Mine
- STRAT: Stratigraphic Test
- STRATP: Stratigraphic Test, Plugged
- STRIP: Strip Mine
- STRIPP: Strip Mine, Plugged
- WASTE: Waste Disposal Well
- WASTEP: Waste Disposal Well, Plugged
- WATER: Water Well
- WATERP: Water Well, Plugged
- WATOT: Oil Test, left open for a water well
- WATRS: Water Supply Well
- WATRSP: Water Supply Well, Plugged
- WTST: Water Well Test Hole
- WTSTP: Water Well Test Hole, Plugged

## Sample Data

## Competency Questions 

## Contributors
- Katrina Schweikert
- David Kedrowski
