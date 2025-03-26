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
- [*Draft* schema]()

**Legend description:** (TO ADD)
- 

## Code (TO ADD)
- il-wells.py
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `il_isgs:ISGS_Well` | `il_isgs_data:d.ISGS_Well.<API_NUMBER>` |
| `geo:Geometry` | `il_isgs_data:d.ISGS_Well.geometry.<API_NUMBER>` |

## Raw Data Attribute List and Mapping with Ontology Concepts
| ISGS Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID     | * | No |  |  |
| API_NUMBER   | * | Yes | `il_isgs:hasPrimaryStateAgencyId` | used as unique identifier |
| ISWSPNUM     |  | Yes | `il_isgs:hasSecondaryStateAgencyId` | present for about 40% of records |
| STATUS       |  | Yes | `is_isgs:hasWellPurpose` | controlled vocabulary (see below) |
| STATUSLONG   | Status description | Yes |  | via controlled vocabulary (see below) |
| LATITUDE     | * | Yes | `geo:Geometry/geo:asWKT` |  |
| LONGITUDE    | * | Yes | `geo:Geometry/geo:asWKT` |  |
| LOCATION     |  | No |  | ?mapsheet |
| OWNER        |  | Yes | `hyfo:hasOwner` | |
| FARM_NAME    | Well Name | No |  |  |
| WELL         |  | No |  | matches FARM_NAME |
| DRILLER      | Drilling company | No |  |  |
| DATE_DRILLED |  | No |  |  |
| ELEVATION    |  | No |  |  |
| ELEVREF      |  | No |  |  |
| ELEVREFLONG  | Elevation reference description | No |  |  |
| TOTAL_DEPTH  |  | Yes | `hyfo:hasTotalDepth` | Integer, includes 0 and NULL |
| WFORMATION   | Formation | Yes | `hyfo:hasAquiferType` | Need to verify this |
| FORM_TOP     | Formation Top | Yes | `hyfo:hasBedrockDepth` | Need to verify this <br/> Integer, includes 0 and NULL (and ~20 negative values?) |
| FORM_BOTTOM  | Formation Bottom | ? |  |  |
| PUMPGPM      | Pumping Rate | Yes | `hyfo:hasWellYield` | Integer, includes 0 and NULL |
| FLAG_LAS     | Digitized Well Log | No |  |  |
| FLAG_LOG     | Scanned Well Log   | No |  |  |
| FLAG_CORE    | Core at ISGS | No |  |  |
| FLAG_SAMPLES | Samples at ISGS | No |  |  |
| DataSummary  | Data summary sheet (url to  pdf) | No |  |  |

**Notes on the data:**
- 

## Controlled Vocabularies
**List 1. STATUS: STATUSLONG** [number of records]
- **WATER: Water Well** [301669]
- ENG: Engineering Test [52943]
- **MONIT: Water Well Monitoring Well** [5804]
- **WTST: Water Well Test Hole** [5576]
- STRAT: Stratigraphic Test [4588]
- MINER: Mineral Test [4160]
- **DRY: Dry Hole (water well)** [2699]
- CROP: Outcrop [1397]
- DRYP: Dry Hole (water well), Plugged [1209]
- **OBS: Observation Well** [831]
- WATERP: Water Well, Plugged [739]
- OBSP: Observation Well, Plugged [576]
- MSFT: Mine Shaft [557]
- **WATRS: Water Supply Well** [530]
- WATRSP: Water Supply Well, Plugged [417]
- SLOPE: Slope Mine [120]
- WTSTP: Water Well Test Hole, Plugged [102]
- MONITP: Water Well Monitoring Well Plugged [77]
- DRIFT: Drift Mine [64]
- STRATP: Stratigraphic Test, Plugged [58]
- STRIP: Strip Mine [51]
- ENGP: Engineering Test, Plugged [24]
- MSERV: Mine Service [20]
- WASTE: Waste Disposal Well [14]
- MSERVP: Mine Service Plugged [12]
- WATOT: Oil Test, left open for a water well [12]
- LUST: Leaking Underground Storage Tank [7]
- OBSO: Observation Well, Oil Shows [7]
- WASTEP: Waste Disposal Well, Plugged [3]
- OBSOP: Observation Well, Oil Shows, Plugged [2]
- MINERP: Mineral Test, Plugged [1]
- OBSG: Observation Well, Gas Shows [1]
- OBSOG: Observation Well, Oil & Gas Shows [1]
- STRIPP: Strip Mine, Plugged [1]

## Sample Data

## Competency Questions 

## Contributors
- Katrina Schweikert
- David Kedrowski
