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
| STATUS | # wells | Proposed Upper Level Class |
| --- | ---: | --- |
| CONSTRUCTED | 240,629 | `gwml2:WellStatusType` |
| PLUGGED | 63,415 | `gwml2:WellStatusType` |
| RECONSTRUCTED | 2287 | `gwml2:WellStatusType` |
| unknown | 3 | `gwml2:WellStatusType` |

**List 2. WELL_USE** There are a few shallow hierarchies here. Some entries contain history we don't need. 142 of the 176 entries are some form of *Other* (they account for 0.5% of values overall).
| WELL_USE | enumerated | # wells | Proposed Upper Level Class |
| --- | :---: | ---: | --- |
| Monitoring well/observation/piezometer | 10 | 83,905 | `gwml2:WellPurposeType` |
| Domestic | 1 | 76,220 | `gwml2:WellWaterUseType` |
| Domestic, Lawn and Garden | 7 | 52,552 | `gwml2:WellWaterUseType` |
| Irrigation | 2 | 23,809 | `gwml2:WellWaterUseType` |
| Oil Field Water Supply | 6 | 18,406 |  |
| Domestic, Livestock |  | 15,936 | `gwml2:WellWaterUseType` |
| Dewatering | 9 | 6117 | `gwml2:WellPurposeType` |
| Environmental Remediation, Air Sparge |  | 4446 | `gwml2:WellPurposeType` |
| Environmental Remediation, Soil Vapor Extraction |  | 3579 | `gwml2:WellPurposeType` |
| Public Water Supply | 5 | 2673 | `gwml2:WellWaterUseType` |
| (unstated)/abandoned | 183 | 2621 | `gwml2:WellStatusType` |
| Geothermal, Closed Loop, Vertical |  | 1886 | `gwml2:WellPurposeType` |
| Environmental Remediation, Injection |  | 1789 | `gwml2:WellPurposeType` |
| Test hole/well | 107 | 1614 | `gwml2:WellPurposeType` |
| Heat Pump (Closed Loop/Disposal), Geothermal | 245 | 1570 | `gwml2:WellPurposeType` |
| Industrial | 4 | 1433 | `gwml2:WellWaterUseType` |
| Feedlot | 3 | 1283 | `gwml2:WellWaterUseType` |
| Environmental Remediation, Recovery |  | 1209 | `gwml2:WellPurposeType` |
| Air Conditioning | 8 | 872 |  |
| Other | 12 | 870 |  |
| Recovery/Soil Vapor Extraction/Soil Vent | 122 | 428 |  |
| Domestic, changed from Oil Field Water Supply |  | 394 |  |
| Pond/Swimming Pool/Recreation | 237 | 348 |  |
| Injection well/air sparge (AS)/shallow | 11 | 298 |  |
| Test Hole, Geotechnical |  | 276 |  |
| Test Hole, Uncased |  | 268 |  |
| Test Hole, Cased |  | 258 |  |
| Feedlot/Livestock/Windmill | 116 | 245 |  |
| Other (gas vent well) |  | 159 |  |
| Geothermal, Open Loop, Surface Discharge |  | 141 |  |
| Cathodic Protection Borehole | 240 | 125 |  |
| Geothermal, Open Loop, Inj. of Water |  | 94 |  |
| Other (Levee Pressure Relief Well) |  | 42 |  |
| Road Construction | 189 | 38 |  |
| Other (Soil Boring) |  | 32 |  |
| Other (Relief Well) |  | 30 |  |
| Recharge Well | 242 | 25 |  |
| Geothermal, Closed Loop, Horizontal |  | 21 |  |
| Other (gas probe well) |  | 17 |  |
| Other (supply well) |  | 16 |  |
| Domestic, changed from Irrigation |  | 15 |  |
| Other (Fire Protection) |  | 12 |  |
| Other (gas vapor monitoring) |  | 11 |  |
| Other (IRRIGATION TEST) |  | 8 |  |
| Other (fire protection) |  | 7 |  |
| Other (Lysimeters) |  | 7 |  |
| Other (Pond) |  | 7 |  |
| Other (pond) |  | 7 |  |
| Other (Supply) |  | 7 |  |
| Other (Pressure Relief) |  | 6 |  |
| Other (cistern) |  | 5 |  |
| Other (construction well) |  | 5 |  |
| Other (exploratory) |  | 5 |  |
| Other (SOIL BORINGS) |  | 5 |  |
| Other (Supply well) |  | 5 |  |
| Other (car wash) |  | 4 |  |
| Other (Disposal) |  | 4 |  |
| Other (dry hole) |  | 4 |  |
| Other (irrigation test well) |  | 4 |  |
| Other (Monitor well for environmental compliance) |  | 4 |  |
| Other (Test Boring) |  | 4 |  |
| Other (cathodic protection) |  | 3 |  |
| Other (rock washing at quarry) |  | 3 |  |
| Other (Shop) |  | 3 |  |
| Other (small pond) |  | 3 |  |
| Other (soil boring) |  | 3 |  |
| Other (Test Hole) |  | 3 |  |
| Other (Test Well) |  | 3 |  |
| Other (Water Coolers) |  | 3 |  |
| Other (Wildlife) |  | 3 |  |
| Other (Windmill Farm) |  | 3 |  |
| Other (Airport Fire Rescue) |  | 2 |  |
| Other (Barn Well) |  | 2 |  |
| Other (concrete plant) |  | 2 |  |
| Other (Depressure) |  | 2 |  |
| Other (drilling supply) |  | 2 |  |
| Other (fill sprayer tanks) |  | 2 |  |
| Other (fish farming) |  | 2 |  |
| Other (fresh water withdrawl) |  | 2 |  |
| Other (Geotechnical Test Hole) |  | 2 |  |
| Other (interceptor) |  | 2 |  |
| Other (Irrigation Test Well) |  | 2 |  |
| Other (irrigation test) |  | 2 |  |
| Other (Not Used) |  | 2 |  |
| Other (Remediation) |  | 2 |  |
| Other (Temp Supply Concrete Plant) |  | 2 |  |
| Other (Water supply for dam) |  | 2 |  |
| Other (wildlife) |  | 2 |  |
| Other (WINDMILL) |  | 2 |  |
| Other ( Abandoned water well) |  | 1 |  |
| Other ( Control water in basement) |  | 1 |  |
| Other (abandoned hand dug well) |  | 1 |  |
| Other (adding water to dry soil to change plasticity for compaction as road bed) |  | 1 |  |
| Other (Air Sparge) |  | 1 |  |
| Other (Check Water Level) |  | 1 |  |
| Other (CO2 Pilot Flood) |  | 1 |  |
| Other (construction supply) |  | 1 |  |
| Other (Construction Water Supply) |  | 1 |  |
| Other (cooling) |  | 1 |  |
| Other (creek supply) |  | 1 |  |
| Other (dam building) |  | 1 |  |
| Other (disposal) |  | 1 |  |
| Other (Dog Kennel) |  | 1 |  |
| Other (Draw down tube) |  | 1 |  |
| Other (Dry Hole) |  | 1 |  |
| Other (Duck Marsh) |  | 1 |  |
| Other (Dump Well) |  | 1 |  |
| Other (dust control) |  | 1 |  |
| Other (fill fire trucks) |  | 1 |  |
| Other (fill water tanks) |  | 1 |  |
| Other (Fire Well) |  | 1 |  |
| Other (fish pond) |  | 1 |  |
| Other (fish tanks) |  | 1 |  |
| Other (Floor Heat) |  | 1 |  |
| Other (For cooling towers only) |  | 1 |  |
| Other (Formation Test) |  | 1 |  |
| Other (Geothermal Dump Well) |  | 1 |  |
| Other (grain elevator) |  | 1 |  |
| Other (gravel pit well) |  | 1 |  |
| Other (hand dug) |  | 1 |  |
| Other (hand pump) |  | 1 |  |
| Other (Highway Dept Water Supply Well) |  | 1 |  |
| Other (Hwy project approved by State) |  | 1 |  |
| Other (Hwy project water supply) |  | 1 |  |
| Other (IRRIGATION TEST HOLE) |  | 1 |  |
| Other (IRRIGATION TEST WELL) |  | 1 |  |
| Other (Irrigation Test well) |  | 1 |  |
| Other (Irrigation test well) |  | 1 |  |
| Other (Landfill well) |  | 1 |  |
| Other (Levee Flood Relief Well) |  | 1 |  |
| Other (livestock, pasture, oil field) |  | 1 |  |
| Other (locker cooler) |  | 1 |  |
| Other (makeup water for sewer plant) |  | 1 |  |
| Other (making brine for streets) |  | 1 |  |
| Other (Methane gas vent) |  | 1 |  |
| Other (never used) |  | 1 |  |
| Other (non potable) |  | 1 |  |
| Other (Personal Safety) |  | 1 |  |
| Other (Pond Well) |  | 1 |  |
| Other (Portable Cement Plant) |  | 1 |  |
| Other (Pump Test) |  | 1 |  |
| Other (Recreation) |  | 1 |  |
| Other (Recreational) |  | 1 |  |
| Other (Road construction) |  | 1 |  |
| Other (rural fire protection) |  | 1 |  |
| Other (salt water disposal) |  | 1 |  |
| Other (sand pit well) |  | 1 |  |
| Other (Sand Pit) |  | 1 |  |
| Other (sand pit) |  | 1 |  |
| Other (sewage plant) |  | 1 |  |
| Other (shop use) |  | 1 |  |
| Other (spill clean up) |  | 1 |  |
| Other (Spray waterer) |  | 1 |  |
| Other (standby well) |  | 1 |  |
| Other (Supply Well) |  | 1 |  |
| Other (SUPPLY WELL) |  | 1 |  |
| Other (supply) |  | 1 |  |
| Other (Tailwater Well) |  | 1 |  |
| Other (Temp water for batch plant) |  | 1 |  |
| Other (temp. construction) |  | 1 |  |
| Other (Temp. Irrigation Well Supply) |  | 1 |  |
| Other (temporary job trailer) |  | 1 |  |
| Other (test well for irrigation drilling) |  | 1 |  |
| Other (treatment well) |  | 1 |  |
| Other (Tree conservation) |  | 1 |  |
| Other (Truck and trailer washing) |  | 1 |  |
| Other (truck wash) |  | 1 |  |
| Other (Truck Wash) |  | 1 |  |
| Other (Unknown hand dug well) |  | 1 |  |
| Other (ventilation shaft) |  | 1 |  |
| Other (Wash Bay) |  | 1 |  |
| Other (wash bay) |  | 1 |  |
| Other (wash cement slab) |  | 1 |  |
| Other (water flood operation) |  | 1 |  |
| Other (waterflood project) |  | 1 |  |
| Other (Windmill) |  | 1 |  |

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
