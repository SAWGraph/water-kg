# Ohio Wells - Ohio Department of Natural Resources (ODNR)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Water Wells of Ohio |
| **Source agency:** | [Ohio Department of Natural Resources](https://ohiodnr.gov/home) |
| **Data source location:** | [Ohio Geology Interactive Map](https://gis.ohiodnr.gov/website/dgs/geologyviewer/#) <br/> [Groundwater Maps & Publications (safety-conservation/about-ODNR/geologic-survey)](https://ohiodnr.gov/discover-and-learn/safety-conservation/about-ODNR/geologic-survey/groundwater-resources/groundwater-maps-publications) <br/> [Groundwater Maps & Publications (land-water/ohio-river-watershed)](https://ohiodnr.gov/discover-and-learn/land-water/ohio-river-watershed/groundwater-maps-publications) |
| **Metadata description**: | [Descriptions of Geologic Map Units (pdf)](https://dam.assets.ohio.gov/image/upload/ohiodnr.gov/documents/geology/OFR98_1_Shrake_2011.pdf) |
| **Other metadata** |  |
| **Format of data**: |  |
| **Data Update Interval**: |  |
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
| `oh_odnr:ODNR-Aquifer` | `oh_odnr_data:d.ODNR-Aquifer.?` |
| `geo:Geometry` | `oh_odnr_data:d.ODNR-Aquifer.geometry.?` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)

| MGS Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| WELL_NO | ODNR Well Log Number (?) | Yes | `oh_odnr:hasWellNo` | `rdfs:subPropertyOf hyfo:hasPrimaryStateAgencyId` |
|  |  |  |  |  |

**Notes on the data:**
- 

## Controlled Vocabularies
**List 1. WELL_USE**
* ABANDONED

**List 2. AQUIFER_TYPE**
* ASPHALT

**List 4. SOURCE_OF_COORD**
* DGS SURFICIAL MAPPING

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
