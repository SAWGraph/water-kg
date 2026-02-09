# Colorado Aquifers - Colorado Geological Survey (CGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Colorado Alluvial Aquifers |
| **Source agency:** | [Colorado Geological Survey](https://coloradogeologicalsurvey.org/) |
| **Data source location:** | [Groundwater \| Statewide Alluvial Aquifers](https://cdss.colorado.gov/gis-data/gis-data-by-category) |
| **Metadata description**: | [Major Alluvial Aquifers](https://cgsarcimage.mines.edu/arcgis/rest/services/Water/ON_010_Colorado_Groundwater_Atlas/MapServer/49) <br/> Select River Basin then select the Alluvium sublayer for that River Basin |
| **Other metadata** |  |
| **Format of data**: | GeoDatabase (layer exported as a shapefile using QGIS for triplification) |
| **Data Update Interval**: | June 25, 2020 |
| **Location of triples:** |  |

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
| `co_cgs:CGS_Aquifer` | `co_cgs_data:d.CGS_AlluvialAquifer.<OBJECTID>` |
| `geo:Geometry` | `c0_cgs_data:d.CGS_AlluvialAquifer.geometry.<OBJECTID>` |

## Raw Data Attribute List and Mapping with Ontology Concepts

`co_cgs:alluvialAquiferId rdfs:subPropertyOf hyfo:hasPrimarySawgraphAqId`

**Examples of triples from data/metadata sources**


| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID |  | Yes | `co_cgs:alluvialAquiferId` | No other unique identifier present | 
| River_Basi |  | Yes | `co_cgs:riverBasin` |  |
| SHAPE_Leng |  | No |  |  | 
| SHAPE_Area |  | No |  |  | 

**Notes on the data:**
* 

## Controlled Vocabularies

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
