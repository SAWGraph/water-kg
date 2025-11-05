# United States Aquifer Database

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | United States Aquifer Database |
| **Source agency:** | [Widespread and increased drilling of wells into fossil aquifers in the USA](https://www.nature.com/articles/s41467-022-29678-7) |
| **Data source location:** | [United States Aquifer Database](https://www.hydroshare.org/resource/d2260651b51044d0b5cb2d293d21af08/) |
| **Metadata description**: | [United States Aquifer Database](https://www.hydroshare.org/resource/d2260651b51044d0b5cb2d293d21af08/) |
| **Other metadata** |  |
| **Format of data**: | .shp file |
| **Data Update Interval**: | Last updated April 19, 2022 |
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
| Instance Class | IRI Format | Note |
| --- | --- | --- |
| `gwml2:GW_AquiferSystem` | `usad:d.USAD_<Aquifer>` | Remove spaces |
| `geo:Geometry` | `usad:d.USAD_<Aquifer>.geometry` |  |

### Raw Data Attribute List and Mapping with Ontology Concepts

Examples of triples from data/metadata sources
<!-- * `me_mgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel" -->
<!-- * `me_mgs:GW_Aquifer hyfo:hasDescription` "Maine aquifer systems consist of aquifers within 100m of each other" -->

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| Aquifer | unique aquifer name | Yes |  | Use as part of IRI | 
| BroaderSys | broader, regional-scale aquifer system | Yes | `gwml2:gwAquiferSystem` |  |

### Notes on the data
* 

### Controlled Vocabularies
List 1. 

### Sample Data

## Competency Questions 

## Contributors
- David Kedrowski

