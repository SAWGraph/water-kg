# Kansas Wells - Kansas Geological Survey (KGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Water Well Completion Records (WWC5) Database |
| **Source agency:** | [Kansas Geological Survey](https://kgs.ku.edu/) |
| **Data source location:** | [KGS--Water Well Completion Records (WWC5) Database](https://www.kgs.ku.edu/Magellan/WaterWell/index.html) |
| **Metadata description**: | [File Format](https://www.kgs.ku.edu/Magellan/WaterWell/file_format.html) |
| **Other metadata** | [Metadata](https://www.kgs.ku.edu/Magellan/WaterWell/wwc5_fgdc.html) |
| **Format of data**: | comma-delimited text file (zipped) |
| **Data Update Interval**: |  |
| **Location of triples:** | [SAWGraph Kansas](https://drive.google.com/drive/folders/1A699-COUqopuCIBzESBFEUf7GQvNHz23?usp=drive_link) |

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
| `ks_kgs:KGS_Well` | `ks_kgs_data:d.KGS_Well.<WELL_ID>` |
| `geo:Geometry` | `ks_kgs_data:d.KGS_Well.geometry.<WELL_ID>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)

| KGS Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| WELL_ID | Unique ID assigned by the Survey for each record | Yes | `ks_kgs:hasWellId` | `rdfs:subPropertyOf hyfo:hasPrimaryStateWellId` | 
| COUNTY | Name of the county where well is located | No |  |  |
| TOWNSHIP | Public Land Survey System township number, 1-35 in Kansas | No |  | Civil townships and PLSS townships do not coincide |
| TWN_DIR | Township direction. S (south) or N (north), Always south in Kansas | No |  |  |
| RANGE | Public Land Survey System range number, 1-43 in west and 1-25 in east | No |  |  |
| RANGE_DIR | Range direction. E (east) or W (west) | No |  |  |
| SECTION | The PLSS section the site is located in: 1-36 | No |  |  |
| SPOT | The legal quarter description qualifiers list as NE, NW, SE, and SW, etc. Ordered from smallest to largest. | No  |  |   |
| LONGITUDE | NAD 1927, generated from the legal location or entered by GPS | Yes | `geo:hasGeometry/geo:asWKT` |  |
| LATITUDE | NAD 1927, generated from the legal location or entered by GPS | Yes | `geo:hasGeometry/geo:asWKT` |  |
| LONG_LAT_TYPE | Either "GPS" or "From PLSS." If calculated from PLSS, then good to the maximum quarter calls supplied. | No |  |  |
| OWNER | Name of owner on WWC5 form | Yes | `hyfo:hasOwner` |  |
| WELL_USE | Description of how the well is being used | Yes | `ks_kgs:hasWellUse` | `rdfs:subPropertyOf hyfo:hasWellPurpose` <br/> controlled vocabulary |
| COMPLE_DATE | Date the well was completed | No |  |  |
| STATUS | As of the completion date, Constructed, Reconstructed, or plugged | Yes | `ks_kgs:hasStatus` | `rdsf:subPropertyOf hyfo:hasWellStatus` <br/> controlled vocabulary |
| OTHER_ID | Useful ID from WWC5 such as monitoring well number or oil well name | ? |  | 3rd ID ? |
| DWR_NUMBER | Water right number if known | No |  |  |
| DIRECTIONS | Written instructions on how to find the well | No |  |  |
| WELL_DEPTH | Depth the well is completed, feet | Yes | `hyfo:hasTotalDepth` | Decimal, includes 0 and NULL |
| ELEV | Land surface elevation, feet | No |  |  |
| STATIC_DEPTH | Depth to water at time of completion, feet | Yes | `hyfo:hasStaticWaterDepth` | Decimal, includes 0 and NULL (including a few negative values?) |
| EST_YIELD | Yield of well at time of completion, gallons per minute | Yes | `hyfo:hasWellYield` | Decimal, includes 0 and NULL |
| DRILLER | Name of driller | No |  |  |
| CASING_TYPE |  | No |  | Not defined in either metadata source |
| CASING_JOINTS |  | No |  | Not defined in either metadata source |
| CASING_DIAM_1 |  | No |  | Not defined in either metadata source |
| CASING_DEPTH_1 |  | Yes | `hyfo:hasCasingDepth` | Not defined in either metadata source <br/> Decimal, includes 0 and NULL |
| CASING_DIAM_2 |  | No |  | Not defined in either metadata source |
| CASING_DEPTH_2 |  | No |  | Not defined in either metadata source |
| CASING_DIAM_3 |  | No |  | Not defined in either metadata source |
| CASING_DEPTH_3 |  | No |  | Not defined in either metadata source |
| CASING_HEIGHT |  | No |  | Not defined in either metadata source |
| CASING_WEIGHT |  | No |  | Not defined in either metadata source |
| CASING_THICKNESS |  | No |  | Not defined in either metadata source |
| SCREEN_PERFORATION_MATERIAL |  | No |  | Not defined in either metadata source |
| SCREEN_OPENINGS_TYPE |  | No |  | Not defined in either metadata source |
| SCREEN_FROM_1 |  | No |  | Not defined in either metadata source |
| SCREEN_TO_1 |  | No |  | Not defined in either metadata source |
| SCREEN_FROM_2 |  | No |  | Not defined in either metadata source |
| SCREEN_TO_2 |  | No |  | Not defined in either metadata source |
| SCREEN_FROM_3 |  | No |  | Not defined in either metadata source |
| SCREEN_TO_3 |  | No |  | Not defined in either metadata source |
| SCREEN_FROM_4 |  | No |  | Not defined in either metadata source |
| SCREEN_TO_4 |  | No |  | Not defined in either metadata source |
| GRAVELPACK_1_FROM |  | No |  | Not defined in either metadata source |
| GRAVELPACK_1_TO |  | No |  | Not defined in either metadata source |
| GRAVELPACK_2_FROM |  | No |  | Not defined in either metadata source |
| GRAVELPACK_2_TO |  | No |  | Not defined in either metadata source |
| GRAVELPACK_3_FROM |  | No |  | Not defined in either metadata source |
| GRAVELPACK_3_TO |  | No |  | Not defined in either metadata source |
| GROUT_TYPE |  | No |  | Not defined in either metadata source |
| GROUT_FROM_1 |  | No |  | Not defined in either metadata source |
| GROUT_TO_1 |  | No |  | Not defined in either metadata source |
| GROUT_FROM_2 |  | No |  | Not defined in either metadata source |
| GROUT_TO_2 |  | No |  | Not defined in either metadata source |
| GROUT_FROM_3 |  | No |  | Not defined in either metadata source |
| GROUT_TO_3 |  | No |  | Not defined in either metadata source |
| CONTAMINATION_SOURCE_TYPE |  | ? |  | Not defined in either metadata source |
| CONTAM_SOURCE_DIRECTION |  | ? |  | Not defined in either metadata source |
| CONTAM_SOURCE_DISTANCE |  | ? |  | Not defined in either metadata source |
| WELL_KID | Well ID from Master List of Water Wells | Yes | `ks_kgs:hasWellKid` | `rdfs:subPropertyOf hyfo:hasSecondaryStateWellId` |
| SCANNED | Y if the form has been scanned; N if it is not scanned yet | No |  |  |
| URL | Link to web page for this record | ? |  | Could this be of value to users ? |
| NAD83_LONGITUDE | NAD 1983, generated from the legal location or entered by GPS | No |  |  |
| NAD83_LATITUDE | NAD 1983, generated from the legal location or entered by GPS | No |  |  |
| CONTRACTORS_LICENSE_NUMBER | KDHE Licence Number of the well driller | No |  |  |

**Notes on the data:**
* 

## Controlled Vocabularies
**List 1. STATUS**
* CONSTRUCTED
* RECONSTRUCTED
* PLUGGED
* unknown

**List 2. WELL_USE**
* (unstated)/abandoned
* Air Conditioning
* Cathodic Protection Borehole
* Dewatering
* Domestic
* Domestic, changed from Irrigation
* Domestic, changed from Oil Field Water Supply
* Domestic, Lawn and Garden
* Domestic, Livestock
* Environmental Remediation, Air Sparge
* Environmental Remediation, Injection
* Environmental Remediation, Recovery
* Environmental Remediation, Soil Vapor Extraction
* Feedlot
* Feedlot/Livestock/Windmill
* Geothermal, Closed Loop, Horizontal
* Geothermal, Closed Loop, Vertical
* Geothermal, Open Loop, Inj. of Water
* Geothermal, Open Loop, Surface Discharge
* Heat Pump (Closed Loop/Disposal), Geothermal
* Industrial
* Injection well/air sparge (AS)/shallow
* Irrigation
* Monitoring well/observation/piezometer
* Oil Field Water Supply
* Other
* Other ( Abandoned water well)
* Other ( Control water in basement)
* Other (abandoned hand dug well)
* Other (adding water to dry soil to change plasticity for compaction as road bed)
* Other (Air Sparge)
* Other (Airport Fire Rescue)
* Other (Barn Well)
* Other (car wash)
* Other (cathodic protection)
* Other (Check Water Level)
* Other (cistern)
* Other (CO2 Pilot Flood)
* Other (concrete plant)
* Other (construction supply)
* Other (Construction Water Supply)
* Other (construction well)
* Other (cooling)
* Other (creek supply)
* Other (dam building)
* Other (Depressure)
* Other (Disposal)
* Other (disposal)
* Other (Dog Kennel)
* Other (Draw down tube)
* Other (drilling supply)
* Other (dry hole)
* Other (Dry Hole)
* Other (Duck Marsh)
* Other (Dump Well)
* Other (dust control)
* Other (exploratory)
* Other (fill fire trucks)
* Other (fill sprayer tanks)
* Other (fill water tanks)
* Other (Fire Protection)
* Other (fire protection)
* Other (Fire Well)
* Other (fish farming)
* Other (fish pond)
* Other (fish tanks)
* Other (Floor Heat)
* Other (For cooling towers only)
* Other (Formation Test)
* Other (fresh water withdrawl)
* Other (gas probe well)
* Other (gas vapor monitoring)
* Other (gas vent well)
* Other (Geotechnical Test Hole)
* Other (Geothermal Dump Well)
* Other (grain elevator)
* Other (gravel pit well)
* Other (hand dug)
* Other (hand pump)
* Other (Highway Dept Water Supply Well)
* Other (Hwy project approved by State)
* Other (Hwy project water supply)
* Other (interceptor)
* Other (IRRIGATION TEST HOLE)
* Other (irrigation test well)
* Other (Irrigation Test Well)
* Other (IRRIGATION TEST WELL)
* Other (Irrigation Test well)
* Other (Irrigation test well)
* Other (IRRIGATION TEST)
* Other (irrigation test)
* Other (Landfill well)
* Other (Levee Flood Relief Well)
* Other (Levee Pressure Relief Well)
* Other (livestock, pasture, oil field)
* Other (locker cooler)
* Other (Lysimeters)
* Other (makeup water for sewer plant)
* Other (making brine for streets)
* Other (Methane gas vent)
* Other (Monitor well for environmental compliance)
* Other (never used)
* Other (non potable)
* Other (Not Used)
* Other (Personal Safety)
* Other (Pond Well)
* Other (Pond)
* Other (pond)
* Other (Portable Cement Plant)
* Other (Pressure Relief)
* Other (Pump Test)
* Other (Recreation)
* Other (Recreational)
* Other (Relief Well)
* Other (Remediation)
* Other (Road construction)
* Other (rock washing at quarry)
* Other (rural fire protection)
* Other (salt water disposal)
* Other (sand pit well)
* Other (Sand Pit)
* Other (sand pit)
* Other (sewage plant)
* Other (shop use)
* Other (Shop)
* Other (small pond)
* Other (Soil Boring)
* Other (soil boring)
* Other (SOIL BORINGS)
* Other (spill clean up)
* Other (Spray waterer)
* Other (standby well)
* Other (supply well)
* Other (Supply well)
* Other (Supply Well)
* Other (SUPPLY WELL)
* Other (Supply)
* Other (supply)
* Other (Tailwater Well)
* Other (Temp Supply Concrete Plant)
* Other (Temp water for batch plant)
* Other (temp. construction)
* Other (Temp. Irrigation Well Supply)
* Other (temporary job trailer)
* Other (Test Boring)
* Other (Test Hole)
* Other (test well for irrigation drilling)
* Other (Test Well)
* Other (treatment well)
* Other (Tree conservation)
* Other (Truck and trailer washing)
* Other (truck wash)
* Other (Truck Wash)
* Other (Unknown hand dug well)
* Other (ventilation shaft)
* Other (Wash Bay)
* Other (wash bay)
* Other (wash cement slab)
* Other (Water Coolers)
* Other (water flood operation)
* Other (Water supply for dam)
* Other (waterflood project)
* Other (Wildlife)
* Other (wildlife)
* Other (Windmill Farm)
* Other (WINDMILL)
* Other (Windmill)
* Pond/Swimming Pool/Recreation
* Public Water Supply
* Recharge Well
* Recovery/Soil Vapor Extraction/Soil Vent
* Road Construction
* Test Hole, Cased
* Test Hole, Geotechnical
* Test Hole, Uncased
* Test hole/well

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
