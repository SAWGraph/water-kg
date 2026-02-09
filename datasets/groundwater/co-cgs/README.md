# Colorado Aquifers - Colorado Geological Survey (CGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Colorado Alluvial Aquifers |
| **Source agency:** | [Colorado Geological Survey](https://coloradogeologicalsurvey.org/) |
| **Data source location:** | [Groundwater | Statewide Alluvial Aquifers](https://cdss.colorado.gov/gis-data/gis-data-by-category) |
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
| `ks_kgs:KGS_Aquifer` | `ks_kgs_data:d.KGS_Aquifer.<AquiferName>` |
| `geo:Geometry` | `ks_kgs_data:d.KGS_Aquifer.geometry.<AquiferName>` |

where `<Aquifername>` is 'Ozark', 'Osage', 'HighPlains', 'GlacialDrive', 'FlintHills', 'Dakota', or 'Alluvial' 

## Raw Data Attribute List and Mapping with Ontology Concepts

`ks_kgs:hasSawgraphAqId rdfs:subPropertyOf hyfo:hasPrimarySawgraphAqId`

**Examples of triples from data/metadata sources**
* `ks_kgs:GW_Aquifer hyfo:hasAltName` "Ogalla, Great Bend Prairie, Equus Bed"
* `ks_kgs:GW_Aquifer hyfo:hasNotes` "northern portion not potable"
* `ks_kgs:GW_Aquifer hyfo:hasAquiferTypeDetail` "Cambro-Ordovician"
* `ks_kgs:GW_Aquifer hyfo:hasAquiferMaterial` "dolomite"

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID |  | No |  | Osage & Flint Hills Aquifers only | 
| AREA__SQ_M |  | No |  | Osage & Flint Hills Aquifers only | 
| Shape_Leng |  | No |  | Osage & Flint Hills Aquifers only | 
| NAME |  | Yes | `hyfo:hasName` |  | 
| Shape__Area |  | No |  |  |
| Shape__Length |  | No |  |  |

**Notes on the data:**
* 

## Controlled Vocabularies

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
