# NHDFlowline

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | NHDFlowline.shp and PlusFlow.dbf <br/> There is one pair of files for each Vector Processing Unit (VPU)/2-digit Hydrologic Unit (HUC2) |
| **Source Agency:** | [United States Geological Survey](https://www.usgs.gov/) |
| **Data source location:** | [Get NHDPlus (National Hydrography Dataset Plus) Data](https://www.epa.gov/waterdata/get-nhdplus-national-hydrography-dataset-plus-data#v2datamap) |
| **Metadata description:** | [NHD*Plus Version2*: User Guide](https://www.epa.gov/system/files/documents/2023-04/NHDPlusV2_User_Guide.pdf) |
| **Other metadata:** |  |
| **Format of data:** | .shp & .dbf files |
| **Data update interval:** | no longer maintained but still available and widely used |
| **General comments**: | NHDFlowline.shp has the individual flowlines (*HY_ElementaryFlowPath*) <br/> PlusFlow.dbf details how they are networked |

## Schema Diagram (TO ADD)
- [**Link to schema diagram on lucid chart**]()

## Code (TO ADD)
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `hyf:HY_ElementaryFlowPath` | `gcx-cid:<COMID>` |
| `geo:Geometry` | `gcx-cid:<COMID>.geometry` |
| `nhdplusv2:FlowPathLength` | `gcx-cid:<COMID>.flowPathLength` |
| `qudt:QuantityValue` | `gcx-cid:<COMID>.flowPathLength.quantityValue` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)
| NHDFLowline | Description | Lift to graph | Ontology property |
| --- | --- | --- |--- |
| COMID | Common identifier | Yes | nhdplusv2:hasCOMID |
| FDATE | Feature currency date | No |  |
| RESOLUTION | high, medium, local | No |  |
| GNIS_ID | GNIS ID for GNIS_NAME | No |  |
| GNIS_NAME | Name from GNIS | Yes | schema:name |
| LENGTHKM | Length | Yes | nhdplusv2:hasFlowPathLength |
| REACHCODE | Reach code | Yes | nhdplusv2:hasReachCode |
| FLOWDIR | with digitized, uninitialized | No |  |
| WBAREACOMI | ComID of the NHD polygonal water feature through which an "artificial path" flows | No |  |
| FTYPE | [NHD feature type](https://files.hawaii.gov/dbedt/op/gis/data/NHD%20Complete%20FCode%20Attribute%20Value%20List.pdf) | Yes | nhdplusv2:hasFTYPE |
| FCODE | [NHD feature type code](https://files.hawaii.gov/dbedt/op/gis/data/NHD%20Complete%20FCode%20Attribute%20Value%20List.pdf) | Yes | nhdplusv2:hasFCODE |
| SHAPE_LENG | length in decimal degrees | No |  |
| ENABLED | Always "True" | No |  |
| GNIS_NBR | ?? | No |  |
| geometry | LineString | Yes | geo:hasGeometry/geo:asWKT |

| PlusFlow | Description | Lift to graph | Ontology property |
| --- | --- | --- | --- |
| FROMCOMID | Common identifier for upstream flowline | Yes | hyf:downstreamWaterBody |
| FROMHYDSEQ | HydroSeq of FromComID | No |  |
| FROM LVLPAT | LevelPathID of FromComID | No |  |
| TOCOMID | Common identifier for downstream flowline | Yes | hyf:downstreamWaterBody |
| TOHYDSEQ | HydroSeq of ToComID | No |  |
| TOLVLPAT | LevelPathID of ToComID | No |  |
| NODENUMBER | at the bottom of FromComID and top of ToComID | No |  |
| DELTALEVEL | Numerical difference between StreamLevel of FromComID and ToComID | No |  |
| DIRECTION | flowing connection, network start, network end, coastal connection | No |  |
| GAPDISTKM | Distance between downstream end of FromComID and upstream end of ToComID | No |  |
| HasGeo | Yes if GapDistKm is 0 else No | No |  |
| TotDASqKM | Total upstream cumulative drainage area | No |  |
| DivDASqKM | Divergence-routed cumulative drainage area | No |  |

**Notes on the data:**
- 

## Schema Diagram (TO ADD)
![Schema Diagram]()

**Legend description:** (TO ADD)
- 

## Controlled Vocabularies
- 

## Sample Data
- 

## Competency Questions
- 

## Contributors
- [David Kedrowski](https://github.com/dkedrowski)
