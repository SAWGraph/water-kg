# Principal Aquifers & Alluvial and Glacial Aquifers of the US - United States Geological Survey (USGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Principal Aquifers of the United States <br> Alluvial and Glacial Aquifers |
| **Source agency:** | [United States Geological Survey](https://www.usgs.gov/) |
| **Data source location:** | [Principal Aquifers of the 48 Conterminous United States, Hawaii, Puerto Rico, and the U.S. Virgin Islands](https://www.sciencebase.gov/catalog/item/63140610d34e36012efa385d) <br> [Alluvial and Glacial Aquifers](https://www.sciencebase.gov/catalog/item/63140610d34e36012efa3859) |
| **Metadata description**: | [Principal Aquifers metadata](https://www.sciencebase.gov/catalog/file/get/63140610d34e36012efa385d?f=__disk__77%2F4c%2F7d%2F774c7d2a6f3083f01530581c537ed1c1e9ae4a70&transform=1&allowOpen=true) <br> [Alluvial and Glacial Aquifers metadata](https://www.sciencebase.gov/catalog/file/get/63140610d34e36012efa3859?f=__disk__47%2Fe8%2Fe2%2F47e8e2a43b623e89b0183cd54c44031e8895f9eb&transform=1&allowOpen=true) |
| **Other metadata** |  |
| **Format of data**: | .shp files |
| **Data Update Interval**: | Last updated September 15, 2023 |
| **Location of triples:** |  |

## Principal Aquifers

### Schema Diagram (TO ADD)
- [*Draft* schema]()

### Legend description (TO ADD)
- 

### Code (TO ADD)
- ?.py
- [Code Directory]()
- [GDrive Output Directory]()

### IRIs
Reuse IRIs from Geoconnex ?

Define `@prefix gcx_paq: <https://geoconnex.us/ref/principal_aq/`
* Geoconnex does not include links to geometries in either their KG or their Reference Server

Define `@prefix usgs: <https://usgs.spatialai.org/v1/usgs#>`

Define `@prefix usgs_data: <https://usgs.spatialai.org/v1/usgs-data#>`

| Instance Class | IRI Format | Note |
| --- | --- | --- |
| `gwml2:GW_Aquifer` | `gcx_paq:<AQ_CODE>` | Geometries for each code must be merged to align with Geoconnex </br> Possibly use our own IRI and then link to Geoconnex via `schema:sameAs`? |
| `geo:Geometry` | `usgs_data:d.USGS_PrincipalAquifer_<AQ_CODE>.geometry` | Geoconnex `geo:Geometry` is a blank node |

### Raw Data Attribute List and Mapping with Ontology Concepts

Examples of triples from data/metadata sources
<!-- * `me_mgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel" -->
<!-- * `me_mgs:GW_Aquifer hyfo:hasDescription` "Maine aquifer systems consist of aquifers within 100m of each other" -->

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID_1 | Internal feature number | ? | `usgs:hasAqId` | This is difficult to align with Geoconnex, which treats every feature with the same AQ_CODE as a single feature | 
| ROCK_NAME | The name of the permeable geologic material that composes the aquifer. | Yes | `usgs:hasLithology` | Controlled vocabulary |
| ROCK_TYPE | The code number relating to the rock_name. | No |  | Controlled vocabulary |
| AQ_NAME | The aquifer unit name. | Yes | `usgs:hasAqName` | capture as text (62 distinct values) <br/> This exists in the Geoconnex KG |
| AQ_CODE | The code number relating to the aquifer unit name. | Yes |  | Part of Geoconnex IRI |
| Shape_Leng | The perimeter of the shape in file units.  In the distributed file, file units represent decimal degrees. | No |  |  |
| Shape_Area | The size of the shape in file units.  In the distributed file, file units represent square decimal degrees. | No |  |  |

### Notes on the data
* Geoconnex provides `ROCK_NAME` as text in their Reference Server

### Controlled Vocabularies
List 1. ROCK_TYPE - ROCK_NAME (derived from both datasets)
| ROCK_TYPE | ROCK_NAME | controlled vocab instance |
| --- | --- | --- |
| 0 | `NULL` (only one row, likely an error) | `usgs:Lithology.Unspecified` |
| 100 | Unconsolidated sand and gravel aquifers | `usgs:Lithology.UnconsolidatedSandGravel` |
| 200 | Semiconsolidated sand aquifers | `usgs:Lithology.SemiconsolidatedSand` |
| 300 | Sandstone aquifers | `usgs:Lithology.Sandstone` |
| 400 | Carbonate-rock aquifers | `usgs:Lithology.CarbonateRock` |
| 500 | Sandstone and carbonate-rock aquifers | `usgs:Lithology.SandstoneCarbonateRock` |
| 600 | Igneous and metamorphic-rock aquifers | `usgs:Lithology.IgneousMetamorphic` |
| 999 | `NULL` | `usgs:Lithology..Unspecified` |

List 2. AQ_CODE - AQ_NAME (for just this dataset)
62 pairs of values

### Sample Data

## Alluvial and Glacial Aquifers

### Schema Diagram (TO ADD)
- [*Draft* schema]()

### Legend description (TO ADD)
- 

### Code (TO ADD)
- ?.py
- [Code Directory]()
- [GDrive Output Directory]()

### IRIs
| Instance Class | IRI Format |
| --- | --- |
| `gwml2:GW_Aquifer` | `usgs_data:d.USGS_AlluvialGlacialAquifer_<OBJECTID_1>` |
| `geo:Geometry` | `usgs_data:d.USGS_AlluvialGlacialAquifer_<OBJECTID_1>.geometry` |

### Raw Data Attribute List and Mapping with Ontology Concepts

Examples of triples from data/metadata sources**
<!-- * `me_mgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel" -->
<!-- * `me_mgs:GW_Aquifer hyfo:hasDescription` "Maine aquifer systems consist of aquifers within 100m of each other" -->

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| AREA | The size of the shape in coverage units. | No |  |  | 
| PERIMETER | The perimeter of the shape in coverage units. | No |  |  |
| ALLUVIAL_ | Internal feature number. | Yes | `usgs:hasAqId` | Use as unique identifier |
| ALLUVIAL_I | User-assigned feature number. | No |  |  |
| ROCK_TYPE | The code number relating to the rock_name. | No |  | Controlled vocabulary |
| ROCK_NAME | The name of the permeable geologic material that composes the aquifer. | Yes | `usgs:hasLithology.` | Controlled vocabulary |
| AQ_NAME | The aquifer unit name. | Yes | `usgs:hasAqName` | capture as text |
| AQ_CODE | The code number relating to the aquifer unit name. | No |  | Controlled vocabulary |

### Notes on the data
- 

### Controlled Vocabularies
List 1. ROCK_TYPE - ROCK_NAME (derived from both datasets)
| ROCK_TYPE | ROCK_NAME | controlled vocab instance |
| --- | --- | ---
| 0 | `NULL` (only one row, likely an error) | `usgs:Lithology..Unspecified` |
| 100 | Unconsolidated sand and gravel aquifers | `usgs:Lithology..UnconsolidatedSandGravel` |
| 200 | Semiconsolidated sand aquifers | `usgs:Lithology..SemiconsolidatedSand` |
| 300 | Sandstone aquifers | `usgs:Lithology..Sandstone` |
| 400 | Carbonate-rock aquifers | `usgs:Lithology..CarbonateRock` |
| 500 | Sandstone and carbonate-rock aquifers | `usgs:Lithology..SandstoneCarbonateRock` |
| 600 | Igneous and metamorphic-rock aquifers | `usgs:Lithology..IgneousMetamorphic` |
| 999 | `NULL` | `usgs:Lithology..Unspecified` |

List 2. AQ_CODE - AQ_NAME (for just this dataset)
* 0 - `NULL` (only one row, likely an error)
* 113 - Aquifers of Alluvial and Glacial Origin
* 999 - `NULL`

### Sample Data

## Competency Questions 

## Contributors
- David Kedrowski
