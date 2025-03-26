# Kansas Aquifers - Kansas Geological Survey (KGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Kansas Aquifer Extents |
| **Source agency:** | [Kansas Geological Survey](https://kgs.ku.edu/) |
| **Data source location:** | [Aquifer Extents](https://hub.kansasgis.org/maps/7684344eb6854fa3a6d0b567d470fd9e/about) |
| **Metadata description**: | [Ozark Aquifer Extent](https://hub.kansasgis.org/datasets/KU::aquifer-extents/about?layer=0) <br/> [Osage Aquifer Extent](https://hub.kansasgis.org/datasets/KU::aquifer-extents/about?layer=1) <br/> [High Plains Aquifer Extent](https://hub.kansasgis.org/datasets/KU::aquifer-extents/about?layer=2) <br/> [Glacial Drift Aquifer Extent](https://hub.kansasgis.org/datasets/KU::aquifer-extents/about?layer=3) <br/> [Flint Hills Aquifer Extent](https://hub.kansasgis.org/datasets/KU::aquifer-extents/about?layer=4) <br/> [Dakota Aquifer Extent](https://hub.kansasgis.org/datasets/KU::aquifer-extents/about?layer=5) <br/> [Alluvial Aquifer Extent](https://hub.kansasgis.org/datasets/KU::aquifer-extents/about?layer=6) |
| **Other metadata** | [Aquifer Types and Terminology (2000/11/21)](https://www.kgs.ku.edu/HighPlains/atlas/aptyp.htm) <br/> [Kansas Ground Water \| Ground-water occurrence](https://www.kgs.ku.edu/Publications/Bulletins/ED10/04_occur.html) <br/> [Water Primer: Part 3 - Groundwater (pdf)](https://bookstore.ksre.ksu.edu/pubs/water-primer-part-3-groundwater_MF3022.pdf) |
| **Format of data**: | Shapefile |
| **Data Update Interval**: | February 2, 2024 |
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
| `ks_kgs:KGS-Aquifer` | `ks_kgs_data:d.KGS-Aquifer.<AquiferName>` |
| `geo:Geometry` | `ks_kgs_data:d.KGS-Aquifer.geometry.<AquiferName>` |

where `<Aquifername>` is 'Ozark', 'Osage', 'HighPlains', 'GlacialDrive', 'FlintHills', 'Dakota', or 'Alluvial' 

## Raw Data Attribute List and Mapping with Ontology Concepts

`ks_kgs:hasPrimarySawgraphId rdfs:subPropertyOf hyfo:hasPrimarySawgraphId`

| KGS Aquifer | Description | Lift to graph | Ontology Property | Comments |
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
