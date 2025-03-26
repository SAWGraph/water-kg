# Maine Aquifers - Maine Geological Survey (MGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Significant Sand And Gravel Aquifers |
| **Source agency:** | [Maine Geological Survey](https://www.maine.gov/dacf/mgs/) |
| **Data source location:** | [MGS Significant Sand and Gravel Aquifer Maps Digital Data](https://www.maine.gov/dacf/mgs/pubs/digital/aquifers.htm) <br/> [Maine Aquifers](https://mgs-maine.opendata.arcgis.com/datasets/maine-aquifers/explore) |
| **Metadata description**: | [Maine Aquifers \| About](https://mgs-maine.opendata.arcgis.com/datasets/maine::maine-aquifers/about) <br/> [Maine Aquifers \| About](https://maine.hub.arcgis.com/datasets/maine::maine-aquifers/about) |
| **Other metadata** |  |
| **Format of data**: |  |
| **Data Update Interval**: | Last updated April 22, 2020 |
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
| `me_mgs:MGS_Aquifer` | `me_mgs_data:d.MGS_Aquifer.<OBJECTID>` |
| `geo:Geometry` | `me_mgs_data:d.MGS_Aquifer.geometry.<OBJECTID>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)

| MGS Aquifer | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID |  | Yes | `me_mgs:hasSawgraphId` | `rdfs:subPropertyOf hyfo:hasPrimarySawgraphId` | 
| QUADNAME |  | No |  |  |
| COMPID |  | No |  |  |
| ATYPE |  | No |  | integer IDs for SYMBOLOGY categories |
| SYMBOLOGY |  | Yes | `hyfo:hasAquiferYield hyfo:AquiferFieldMin` <br/> `hyfo:hasAquiferYield hyfo:hasAquiferYieldMax` | Values are intervals |
| DRAW |  | No |  |  |
| SOURCE |  | No |  | 12 records (of 9253) |
| COMMENTS |  | No |  | 32 records (of 9253) |
| AQUIFERID |  | Yes | `me_mgs:hasAquiferId` | `rdfs:subPropertyOf hyfo:hasSecondaryStateAgencyId` <br/> 9188 of 9253 values unique |
| AQUIFERHISTORY |  | No |  |  |
| PUBLISH_DATA |  | No |  |  |
| created_user |  | No |  |  |
| created_date |  | No |  |  |
| last_edited_user |  | No |  |  |
| last_edited_date |  | No |  |  |
| Shape_Area |  | No |  |  |
| Shape_Length |  | No |  |  |

**Notes on the data:**
- 

## Controlled Vocabularies
**List 1. ATYPE** [count]
- 0: area not mapped as aquifer [275]
- 1: 10-50 gallons-per-minute [4668]
- 2: greater than 50 gallons-per-minute [297]
- 3: island of non-aquifer material within an area mapped as aquifer [3931]
- 4: *no definition found* [17]
- *No value*: [65]

**List 2. SYMBOLOGY** [count]
- \>50 GPM [298]
- 10-50 GPM [4691]
- Non-plotting water [4264]

## Sample Data

## Competency Questions 

## Contributors
- David Kedrowski
