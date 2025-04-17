# Illinois Aquifers - Illinois State Geological Survey (ISGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Major Aquifers |
| **Source Agency:** | [Illinois State Geological Survey](https://isgs.illinois.edu/) |
| **Data Source Location:** | Combined data sets (zipped) <br/> - [Major Aquifers](https://clearinghouse.isgs.illinois.edu/data/hydrology/major-aquifers) <br/> Individual Datasets <br/> - [Major Bedrock Aquifers at Depths Greater Than 500 Feet Below Ground Surface](https://clearinghouse.isgs.illinois.edu/data/hydrology/major-bedrock-aquifers-depths-greater-500-feet-below-ground-surface) <br/> - [Major Bedrock Aquifers Within 300 Feet of Ground Surface](https://clearinghouse.isgs.illinois.edu/data/hydrology/major-bedrock-aquifers-within-300-feet-ground-surface) <br/> - [Major Bedrock Aquifers Within 500 Feet of Ground Surface](https://clearinghouse.isgs.illinois.edu/data/hydrology/major-bedrock-aquifers-within-500-feet-ground-surface) <br/> - [Major Sand and Gravel Aquifers](https://clearinghouse.isgs.illinois.edu/data/hydrology/major-sand-and-gravel-aquifers) <br/> - [Coarse-grained Materials Within 50 Feet of the Ground Surface in Illinois](https://clearinghouse.isgs.illinois.edu/data/hydrology/coarse-grained-materials-within-50-feet-ground-surface-illinois) |
| **Metadata description:** | see *Metadata* tabs at **Data Source Locations** |
| **Format:** | Shape files |
| **Data update interval** | Updated April 1, 2004 |
| **Location of triples:** |  |

## Schema Diagram (TO ADD)
- [*Draft* schema]()

**Legend description:** (TO ADD)
- 

## Code (TO ADD)
- ?.py
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `il_isgs:ISGS_Aquifer` | `il_isgs_data:d.ISGS_Aquifer.<SAWGraphId>` |
| `geo:Geometry` | `il_isgs_data:d.ISGS_Aquifer.geometry.<SAWGraphId>` |

where `<SAWGraphId>` = `<type>-<integer>` with `<type>` = 'BedrockGT500', 'BedrockLT300', 'BedrockLt500', 'SandGravel', or 'ShallowCoarseMatls'

## Raw Data Attribute Lists and Mapping with Ontology Concepts

`il_isgs:hasSawgraphAqId rdfs:subPropertyOf hyfo:hasPrimarySawgraphAqId`

**Examples of triples from data/metadata sources**
* `il_isgs:GW_Aquifer hyfo:hasNotes` "may not yield potable water"
* `il_isgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel: quaternary deposits within pre-glacial bedrock valleys or along modern streams and rivers"
* `il_isgs:GW_Aquifer hyfo:hasDescription` "Illinois aquifer systems consist of adjacent potential aquifers in coarse-grained materials within 50ft of the ground surface"

### Major Bedrock Aquifers Greater Than 500 Ft
| ISGS Aquifer | Description | Lift to graph | Comments |
| --- | --- | --- | --- |
| CODE | 0 - Major bedrock aquifers containing more than 10,000 mg/L total dissolved solids <br/> 1 - Major bedrock aquifers containing from 2,500 to 10,000 mg/L total dissolved solids <br/> 2 - Major bedrock aquifers containing less than 2,500 mg/L total dissolved solids | No | only CODE = 2 lifted to graph |

### Major Bedrock Aquifers Less Than 300 Ft
| ISGS Aquifer | Description | Lift to graph | Comments |
| --- | --- | --- | --- |
| CODE | 0 - Major bedrock aquifer absent <br/> 1 - Major bedrock aquifer present | No | only CODE = 1 lifted to graph |

### Major Bedrock Aquifers Less Than 500 Ft
| ISGS Aquifer | Description | Lift to graph | Comments |
| --- | --- | --- | --- |
| CODE | 0 - Major bedrock aquifer absent <br/> 1 - Major bedrock aquifer present | No | only CODE = 1 lifted to graph |

### Major Sand and Gravel Aquifers
| ISGS Aquifer | Description | Lift to graph | Comments |
| --- | --- | --- | --- |
| CODE | 0 - Major sand and gravel aquifer absent <br/> 1 - Major sand and gravel aquifer present | No | only CODE = 1 lifted to graph |

### Shallow Coarse Materials
| ISGS Aquifer | Description | Lift to graph | Comments |
| --- | --- | --- | --- |
| CODE | 0 - Not a potential aquifer <br/> 1 - Potential aquifer (only potential aquifers are instantiated in SAWGraph) | No | Only CODE = 1 lifted to graph |
| MS | Item MS is the map symbol for each polygon.  It is an alphanumeric character set that describes up to five geologic units present, their order occurrence, and general thickness and depth.  Item MS is directly related to item STACK-UNIT in that STACK-UNIT is a strictly numeric designator that represents the same information as item MS.  MS consists of five concatenated (redefined) items called MS1, MS2, MS3, MS4, MS5.  Each redefined MSx(where x is 1, 2, 3, 4, 5) item represents a single geologic unit, MS1 being the uppermost and MS5 being the lowermost.  Uppercase letters indicate nonlithified a semilithified units greater than 6m (19.7 ft.) thick. Lowercase letters accompanied by asterisk indicatenonlithified and semilithified units less than 6m (19.7 ft.) thick.  Numbers unaccompanied by an asterisk indicatelithified units where the top occurs between depths of 6 to 15m (19.7-49.3 ft.) below ground surface.  Numbers accompanied by an asterisk indicate lithified units where the top occurs between depths of 0 to 6m (0-19.7 ft.) below ground surface. | No |
| STACK_UNIT | This item is a 15 digit numeric code that indicates up to five geologic units present, their order of occurrence, and general thickness and depth.  It is directly related to item MS in that MS is an alphanumeric designator that represents the same information as STACK-UNIT.  STACK-UNIT consists of ten concatenated (redefined) items called (and in this order) UNIT1, QUAL1, UNIT2, QUAL2, UNIT3, QUAL3, UNIT4, QUAL4, UNIT5, QUAL5.  UNITx (where x is 1, 2, 3, 4, or 5) is a two digit identifier for unit name (see the table below).  QUALx is a single digit qualifier for each UNITx, giving thickness, depth and continuity information for the corresponding UNITx.  For example, QUAL1 contains a code that gives descriptive information for UNIT1.  UNIT1 is the uppermost unit, UNIT5 is the lowermost unit. | No |  |
| MS1 | see MS | No |  |
| MS2 | see MS | No |  |
| MS3 | see MS | No |  |
| MS4 | see MS | No |  |
| MS5 | see MS | No |  |
| UNIT1 | see STACK_UNIT | No |  |
| QUAL1 | see STACK_UNIT | No |  |
| UNIT2 | see STACK_UNIT | No |  |
| QUAL2 | see STACK_UNIT | No |  |
| UNIT3 | see STACK_UNIT | No |  |
| QUAL3 | see STACK_UNIT | No |  |
| UNIT4 | see STACK_UNIT | No |  |
| QUAL4 | see STACK_UNIT | No |  |
| UNIT5 | see STACK_UNIT | No |  |
| QUAL5 | see STACK_UNIT | No |  |

**Notes on the Shallow Coarse Materials data:**

      UNITx   MSx             Corresponding Geologic Unit
      (MAP-SYMBOL)

      (nonlithified and semilithified materials)
      1         A   a*          Cahokia Alluvium
      2         Y   y*          Peyton Colluvium
      3         B   b*          Richland Loess
      4         C   c*          Peoria and Roxana Loess
      5         D   d*          Parkland Sand
      6         E   e*          Grayslake Peat
      7         F   f*          Equality Formation, Carmi Member
      8         G   g*          Equality Formation, Dolton Member
      9         H   h*          Henry Formation
      10         I   i*          Wedron Formation, silty and clayey diamictons
      11         J   j*          Wedron Formation, loamy and sandy diamictons
      12         K               Sand and gravel within Wedron Formation:
      12             k*          within 6 m (19.7 ft.) of surface
      26             z*          between 6-15 m (19.7-49.3 ft.) of surface
      13         L   l*          Winnebago Formation, mainly sandy diamictons
      14         M               Sand and gravel within Winnebago Formation:
      14             m*          within 6 m (19.7 ft.) of surface
      26             z*          between 6-15 m (19.7-49.3 ft.) of surface
      15         N   n*          Teneriffe Silt
      16         O   o*          Pearl Formation (includes Hagarstown Member)
      17         P   p*          Glasford Formation, silty and clayey diamictons
      18         Q   q*          Glasford Formation, loamy and sandy diamictons
      19         R               Sand and gravel within Glasford Formation
      19             r*          within 6 m (19.7 ft.) of surface
      26             z*          between 6-15 m (19.7-49.3 ft.) of surface
      22         U   u*          Wolf Creek Formation (mainly diamictons)
      23         V   v*          Mounds gravel and related units
      24         W   w*          Cretaceous sediments, silts, sands, etc.
      25         X               Surface mines/man-made land

      (lithified materials)
      41         1   1*          Pennsylvanian rocks, mainly shales
      42         2   2*          Pennsylvanian rocks, mainly sandstones
      43         3   3*          Mississippian rocks, mainly shales
      44         4   4*          Mississippian rocks, mainly limestones, some sandstones
      45         5   5*          Silurian and some Devonian rocks, mainly dolomite
      46         6   6*          Ordovician rocks, mainly shale (Maquoketa Group)
      47         7   7*          Ordovician and Cambrian rocks, mainly dolomite, some sandstone

      other
      98      water              body of water

      QUALx
      1 - Drift unit 6m thick, continuous throughout polygon area
      2 - Drift unit 6m thick, locally less than 6m thick
      3 - Drift unit < 6m thick, continuous throughout polygon area
      4 - Drift unit < 6m thick, not continuous throughout polygon area

      6 - Bedrock unit present between 6 and 15 meters below surface
      7 - Bedrock unit not present continuously between 6 and 15 meters below surface; locally present at or just below 15 meters
      8 - Bedrock unit present within 6 meters of surface
      9 - Bedrock unit not present continuously above 6 meters below surface; but then is present between 6-15 meters

## Controlled Vocabularies

## Sample Data

## Competency Questions 

## Contributors
- David Kedrowski
