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
| Instance Class | IRI Format |
| --- | --- |
<!-- | `me_mgs:MGS_Aquifer` | `me_mgs_data:d.MGS_Aquifer.<OBJECTID>` | -->
<!-- | `geo:Geometry` | `me_mgs_data:d.MGS_Aquifer.geometry.<OBJECTID>` | -->

### Raw Data Attribute List and Mapping with Ontology Concepts

Examples of triples from data/metadata sources
<!-- * `me_mgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel" -->
<!-- * `me_mgs:GW_Aquifer hyfo:hasDescription` "Maine aquifer systems consist of aquifers within 100m of each other" -->

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID_1 | Internal feature number | Yes | TBD | Use as unique identifier | 
| ROCK_NAME | The name of the permeable geologic material that composes the aquifer. | Yes | `rdfs:comment` | Controlled vocabulary |
| ROCK_TYPE | The code number relating to the rock_name. | No |  | Controlled vocabulary |
| AQ_NAME | The aquifer unit name. | Yes | `rdfs:label` | Controlled vocabulary |
| AQ_CODE | The code number relating to the aquifer unit name. | No |  | Controlled Vocabulary |
| Shape_Leng | The perimeter of the shape in file units.  In the distributed file, file units represent decimal degrees. | No |  |  |
| Shape_Area | The size of the shape in file units.  In the distributed file, file units represent square decimal degrees. | No |  |  |

### Notes on the data
- 

### Controlled Vocabularies
List 1. ROCK_TYPE - ROCK_NAME (derived from both datasets)
* 0 - <NULL> (only one row, likely an error)
* 100 - Unconsolidated sand and gravel aquifers
* 200 - Semiconsolidated sand aquifers
* 300 - Sandstone aquifers
* 400 - Carbonate-rock aquifers
* 500 - Sandstone and carbonate-rock aquifers
* 600 - Igneous and metamorphic-rock aquifers
* 999 - <NULL>

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
<!-- | `me_mgs:MGS_Aquifer` | `me_mgs_data:d.MGS_Aquifer.<OBJECTID>` | -->
<!-- | `geo:Geometry` | `me_mgs_data:d.MGS_Aquifer.geometry.<OBJECTID>` | -->

### Raw Data Attribute List and Mapping with Ontology Concepts

Examples of triples from data/metadata sources**
<!-- * `me_mgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel" -->
<!-- * `me_mgs:GW_Aquifer hyfo:hasDescription` "Maine aquifer systems consist of aquifers within 100m of each other" -->

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| AREA | The size of the shape in coverage units. | No |  |  | 
| PERIMETER | The perimeter of the shape in coverage units. | No |  |  |
| ALLUVIAL_ | Internal feature number. | Yes | TBD | Use as unique identifier |
| ALLUVIAL_I | User-assigned feature number. | No |  |  |
| ROCK_TYPE | The code number relating to the rock_name. | No |  | Controlled vocabulary |
| ROCK_NAME | The name of the permeable geologic material that composes the aquifer. | Yes | `rdfs:comment` | Controlled vocabulary |
| AQ_NAME | The aquifer unit name. | Yes | `rdfs:label` | Controlled vocabulary |
| AQ_CODE | The code number relating to the aquifer unit name. | No |  | Controlled vocabulary |

### Notes on the data
- 

### Controlled Vocabularies
List 1. ROCK_TYPE - ROCK_NAME (derived from both datasets)
* 0 - <NULL> (only one row, likely an error)
* 100 - Unconsolidated sand and gravel aquifers
* 200 - Semiconsolidated sand aquifers
* 300 - Sandstone aquifers
* 400 - Carbonate-rock aquifers
* 500 - Sandstone and carbonate-rock aquifers
* 600 - Igneous and metamorphic-rock aquifers
* 999 - <NULL>

List 2. AQ_CODE - AQ_NAME (for just this dataset)
* 0 - <NULL> (only one row, likely an error)
* 113 - Aquifers of Alluvial and Glacial Origin
* 999 - <NULL>

### Sample Data

## Competency Questions 

## Contributors
- David Kedrowski
