# Ohio Wells - Ohio Department of Natural Resources (ODNR)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Water Wells of Ohio |
| **Source agency:** | [Ohio Department of Natural Resources](https://ohiodnr.gov/home) |
| **Data source location:** | [Water Wells](https://gis.ohiodnr.gov/arcgis/rest/services/DSW_Services/waterwells/MapServer/0) |
| **Metadata description**: | [Water Wells](https://gis.ohiodnr.gov/arcgis/rest/services/DSW_Services/waterwells/MapServer/0) |
| **Other metadata** | [Water Well Database System Help Library](https://waterwells.ohiodnr.gov/assets/Help_Water_Wells.pdf) |
| **Format of data**: | ArcGIS REST Service |
| **Data Update Interval**: |  |
| **Location of triples:** | [Ohio](https://drive.google.com/drive/folders/1BrLBm2pTZFd0YA6I5YitlQ5TMWW0NhKw?usp=drive_link) |

## Schema Diagram (TO ADD)
* [*Draft* schema]()

**Legend description:** (TO ADD)
* 

## Code (TO ADD)
* ?.py
* [Code Directory]()
* [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `oh_odnr:ODNR_Well` | `oh_odnr_data:d.ODNR_Well.<WELL_NO>` |
| `geo:Geometry` | `oh_odnr_data:d.ODNR_Well.geometry.<WELL_NO>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)

| MGS Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID |  | No |  |  |
| WELL_NO | ODNR Well Log Number (?) | Yes | `oh_odnr:hasWellNo` | `rdfs:subPropertyOf hyfo:hasPrimaryStateWellId` |
| TYPE |  | No |  | Always W |
| WELL_USE | Primary well use. DOMESTIC includes residential and private wells. AGRIC/IRRIG includes livestock watering, lawn watering, agricultural, golf course, and barn wells. MUNICIPAL is for city, village, or town wells, and PUBLIC/SEMI-PUB is for schools, restaurants, gas stations, and rest areas | Yes | `oh_odnr:hasWellUse` | `rdfs:subPropertyOf hyfo:hasWellPurpose` <br/> controlled vocabulary |
| LONG83 |  | Yes | `geo:hasGeometry/geo:asWKT` |  |
| LAT83 |  | Yes | `geo:hasGeometry/geo:asWKT` |  |
| SOURCE_OF_COORD |  | No |  | controlled vocabulary |
| COUNTY | County in which the well was drilled | No |  |  |
| TOWNSHIP | Township in which the well was drilled | Yes | `kwg-ont:sfWithin` |  |
| OWNER |  | Yes | `hyfo:hasOwner` | Last, First or Business / Entity name |
| LAST_NAME | If owner is a company, association, church, etc., include its full name here | No |  |  |
| COMPLETION_DATE | The date drilling was completed | No |  |  |
| TOTAL_DEPTH | Completed depth of the well measured in feet | Yes | `hyfo:hasTotalDepth` | Decimal values, including 0 and NULL |
| BEDROCK_DEPTH | Depth to bedrock measured in feet | Yes | `hyfo:hasBedrockDepth` | Integer values, including 0 and NULL |
| DEM_ELEV |  | No |  |  |
| AQUIFER_TYPE | Formation producing the most water. If multiple formations produce similar yields, aquifer type specifies the formation best representing the character of the well | Yes | `oh_odnr:hasAquiferType` | controlled vocabulary |
| DRILL_TYPE |  | No |  | controlled vocabulary |
| TEST_RATE_GPM | Rate in gallons per minute | Yes | `hyfo:hasWellYield` | Decimal values, including 0 and NULL |
| STATIC_WATER_LEVEL_FT | Pre-pumping depth to water once well has stabilized from any pumping, drilling, or bailing  | Yes | `hyfo:hasStaticWaterDepth` | Decimal values, including 0 and NULL |
| ELEV |  | No |  |  |
| CASE_LENGTH | Length of casing, NOT its depth | Yes | `hyfo:hasCasingDepth` | Decimal values, including 0 and NULL |
| STR_COMP_DATE |  | No |  | Typically one day after COMPLETION_DATE |
| HOUSE_NO | House or business address number on street (e.g., the 123 in 123 North Main St.) | No |  |  |
| STREETNAME | Street name (e.g., the Main in 123 North Main St.). For state routes, county roads, township roads, US routes, enter the route or road number (e.g., the 423 in 123 County Road 423) | No |  |  |

**Notes on the data:**
- 

## Controlled Vocabularies
**List 1. WELL_USE**
| WELL_USE | `gwml2` |
| ABANDONED | `:WellStatusType` |
| AGRIC/IRRIG | `:WellWaterUseType` |
| ALIGNMENT HOLE | `:WellPurposeType` |
| CATHODE PROTECT | `:WellPurposeType` |
| COMMERCIAL | `:WellWaterUseType` |
| CONSTRUCTION | `:WellPurposeType` |
| DEWATERING WELL | `:WellPurposeType` |
| DOMESTIC | `:WellWaterUseType` |
| DRAINAGE | `:WellPurposeType` |
| DRY/NO WATER | `:WellStatusType` |
| FIRE PROTECTION | `:WellPurposeType` |
| FRACK WATER | `:WellPurposeType` |
| GAS | `:WellPurposeType` |
| GAS PROB | `:WellPurposeType` |
| HTG/COOLING | `:WellPurposeType` |
| INCLINOMETER | `:WellPurposeType` |
| INDUSTRIAL | `:WellWaterUseType` |
| INJECTION/DISPO | `:WellPurposeType` |
| MONITOR | `:WellPurposeType` |
| MUNICIPAL | `:WellWaterUseType` |
| `NULL` |  |
| OBSERVATION | `:WellPurposeType` |
| OTHER |  |
| PIEZOMETER | `:WellPurposeType` |
| PRESSURE RELIEF | `:WellPurposeType` |
| PUBLIC/SEMI-PUB | `:WellWaterUseType` |
| RECOVERY WELL | `:WellPurposeType` |
| SEALED | `:WellStatusType` |
| SOIL BORING | `:WellPurposeType` |
| TEST BORING | `:WellPurposeType` |
| TEST WELL | `:WellPurposeType` |
| VAPOR EXTRACTIO | `:WellPurposeType` |

**List 2. AQUIFER_TYPE**
* ASPHALT
* BEDROCK
* BEREA
* BIG INJUN SANDSTONE
* BOULDERS
* CLAY
* CLAY & BOULDERS
* CLAY & GRAVEL
* CLAY & GUMBO
* CLAY & HARDPAN
* CLAY & QUICKSAND
* CLAY & ROCK
* CLAY & SAND
* CLAY & SANDSTONE
* CLAY & SHALE
* CLAY & SILT
* CLAY/GRAVEL/BOULDERS
* CLAY/GRAVEL/ROCK
* CLAY/GRAVEL/SHALE
* CLAY/GRAVEL/SILT
* CLAY/SAND/BOULDERS
* CLAY/SAND/GRAVEL
* CLAY/SAND/SHALE
* CLAY/SAND/SILT
* CLAY/SILT/SAND
* CLAYSTONE
* CLEANOUT
* COAL
* COAL & CLAY
* COBBLES
* CONCRETE
* CONGLOMERATE
* CORED
* CREVICE
* DOLOMITE
* DRIFT
* DUG WELL
* EXISTING WELL
* FILL MATERIAL
* FIRE CLAY
* FLAGSTONE
* FLINT
* FORMATION
* FREESTONE
* GLACIAL TILL
* GRAVEL
* GRAVEL & BOULDERS
* GRAVEL & CLAY
* GRAVEL & LIMESTONE
* GRAVEL & QUICKSAND
* GRAVEL & SAND
* GRAVEL & SHALE
* GRAVEL & SILT
* GRAVEL & SLAG
* GRAVEL/ROCK/CLAY
* GRAVEL/SAND/CLAY
* GRAVEL/SAND/ROCK
* GRIT
* GYPSUM
* HARDPAN
* HARDPAN & GRAVEL
* INJUN SANDSTONE
* INJUN SS & SHALE
* LIME & CLAY
* LIMESTONE
* LIMESTONE & CLAY
* LIMESTONE & GRAVEL
* LIMESTONE & ROCK
* LIMESTONE & SHALE
* LOAM
* MARL
* MINE
* MUCK
* MUD
* MUD & CLAY
* MUD & GRAVEL
* MUD & ROCK
* MUD & SAND
* MUD & SHALE
* NIAGARA FORMATION
* OLD WELL
* PEAT
* QUICKSAND
* ROCK
* ROCK & CLAY
* ROCK & GRAVEL
* ROCK & SHALE
* SAND
* SAND & BOULDERS
* SAND & CLAY
* SAND & DIRT
* SAND & GAS
* SAND & GRAVEL
* SAND & ROCK
* SAND & SILT
* SAND/CLAY/GRAVEL
* SAND/GRAVEL/BOULDERS
* SAND/GRAVEL/CLAY
* SAND/GRAVEL/MUD
* SAND/GRAVEL/SHALE
* SANDSTONE
* SANDSTONE & COAL
* SANDSTONE & LIMEST
* SANDSTONE & ROCK
* SANDSTONE & SHALE
* SANDSTONE/SHALE/LIME
* SHALE
* SHALE & CLAY
* SHALE & COAL
* SHALE & LIMEST
* SHALE & LIMESTONE
* SHALE & SANDSTONE
* SHALE & SILTSTONE
* SHALE W SS STREAKS
* SHELL
* SILICA
* SILT
* SILT & CLAY
* SILT & GRAVEL
* SILT & SAND
* SILT/SAND/GRAVEL
* SILTSTONE
* SOAPSTONE
* SOIL
* SPOIL
* STONE
* STREAK
* SULPHUR
* SURFACE
* TRASH
* TRAVERSE GROUP
* UNDIFFERENTIATED
* UNKNOWN
* VOID
* WASH
* `<empty>`

**List 3. DRILL_TYPE**
* AIR HAMMER
* AIR ROTARY
* AUGER
* BUCKET AUGER
* CABLE TOOL
* DIRECT PUSH
* DRIVEN
* DUG
* GEOPROBE
* JETTED
* MUD ROTARY
* MUD/AIR ROTARY
* OTHER
* REVERSE ROTARY
* ROTARY
* ROTARY/AIRHAMR
* ROTOSONIC
* `<empty>`

**List 4. SOURCE_OF_COORD**
* DGS SURFICIAL MAPPING
* DIGITAL MAP
* DIGITIZED
* Geocode
* GEOCODE
* GEOCODE 2021
* GLOBAL POSITIONING SYSTEM
* MAP-OTHERS
* MAP-USGS 1:24000
* OSIP 2.5FT DEM
* TERRESTRIAL SURVEY
* `<empty>`

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
