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
| `nhdplusv2:FlowLine` | `gcx_cid:<COMID>` |
| `geo:Geometry` | `gcx_cid:<COMID>.geometry` |
| `nhdplusv2:FlowPathLength` | `gcx_cid:<COMID>.flowPathLength` |
| `qudt:QuantityValue` | `gcx_cid:<COMID>.flowPathLength.quantityValue` |

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

---

# Reference Flowlines from the National Hydrologic Geospatial Fabric Reference Hydrofabric

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | National Hydrologic Geospatial Fabric Reference Hydrofabric |
| **Source Agency:** | [United States Geological Survey](https://www.usgs.gov/) |
| **Data source location:** | [1. National Hydrologic Geospatial Fabric Reference Hydrofabric](https://www.sciencebase.gov/catalog/item/61295190d34e40dd9c06bcd7) |
| **Metadata description:** | [reference_CONUS.xml](https://www.sciencebase.gov/catalog/file/get/61295190d34e40dd9c06bcd7?f=__disk__85%2Fe8%2Fc0%2F85e8c0d053c499da6e1fec6e9ade3134d9eb20b6&transform=1&allowOpen=true) |
| **Other metadata:** |  |
| **Format of data:** | .gpkg |
| **Data update interval:** |  |
| **General comments**: |  |

## Schema Diagram (TO ADD)
- [**Link to schema diagram on lucid chart**]()

## Code (TO ADD)
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `nhdplusv2:FlowLine` | `gcx_cid:<COMID>` |
| `geo:Geometry` | `gcx_cid:<COMID>.geometry` |
| `nhdplusv2:FlowPathLength` | `gcx_cid:<COMID>.flowPathLength` |
| `qudt:QuantityValue` | `gcx_cid:<COMID>.flowPathLength.quantityValue` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)
| reference_flowline | Description | Lift to graph | Ontology property | Notes |
| --- | --- | --- | --- | --- |
| fid | Internal feature identifier | No |  |  |
| COMID | NHDPlus version 2 comid (NHDPlusV2) or permanent identifier (NHDPlus HR) common identifier | Yes |  |  |
| FromNode | Unique node identifier (number) of flowline's fromnode (inlet) | No |  |  |
| ToNode | Unique node identifier (number) of flowline's tonode (outlet) | No |  |  |
| StartFlag | Flag denoting a flowline is a headwater | No |  | 0 = not a headwater <br> 1 = is a headwater |
| StreamCalc | Stream in NHDPlus is a modified version of stream order as defined by Strahler. The Strahler stream order algorithm does not account for flow splits in the  network. The NHDPlus algorithm for stream order does take flow splits into consideration. StreamCalc stands for stream calculator and is computed along with StreamOrder. | No |  |  |
| Divergence | Divergence field, routes a fraction of 1 to the main path (i.e. Divergence = 1) and a fraction of 0 to all other paths (i.e. Divergence = 2) | Yes |  | 0 = not part of a divergence <br> 1 = main path of a divergence <br> 2 = minor path of a divergence |
| DnMinorHyd | Downstream minor hydrologic sequence number | No |  |  |
| toCOMID | Common identifier for the downstream flowline feature | Yes |  |  |
| FCODE | Numeric codes for various feature attributes. Definitions correspond to the attribute 'ftype' in the flowline table | Yes |  |  |
| LENGTHKM | Length of flowline in kilometers | Yes |  |  |
| REACHCODE | Unique reach identifier from the source hydrographic dataset | Yes |  |  |
| FromMeas | ReachCode route measure (m-value) at bottom of flowline feature derived from NHDPlusV2 | No |  |  |
| ToMeas | ReachCode route measure (m-value) at top of flowline feature derived from NHDPlusV2 | No |  |  |
| AreaSqKM | Feature area in square kilometers | No |  |  |
| ArbolateSu | Kilometers of stream upstream of the bottom of the flowline feature | No |  | arbolate sum |
| TerminalPa | Hydrologic sequence number of terminal flowline feature | No |  |  |
| Hydroseq | Hydrologic sequence number; places flowlines in hydrologic order; processing flowline features in ascending order, encounters the features from downstream to upstream; processing the flowline features in descending order, encounters the features from upstream to downstream | No |  |  |
| LevelPathI | Hydrologic sequence number of most downstream flowline feature in the level path | Yes |  |  |
| Pathlength | Distance to the terminal flowline feature downstream along the mainpath | No |  |  |
| DnLevelPat | Downstream mainstem level path identifier | No |  |  |
| DnHydroseq | Downstream mainstem hydrologic sequence number | No |  |  |
| TotDASqKM | Total upstream area in square kilometer for each flowline catchment | No |  |  |
| TerminalFl | Flag denoting if flowline is a terminal reach. For example, flowline ends at the ocean or international boundary or of if tocomid is 0 | No |  | 0 = not terminal <br> 1 = terminal |
| streamleve | StreamLevel is a numeric code that traces main paths of water flow upstream through the drainage network. StreamLevel is assigned starting at the terminus of a drainage
network. If the terminus stopped at a coastline flowline feature (i.e. at the Atlantic Ocean, the Pacific Ocean, the Gulf of Mexico, or one of the Great Lakes), a stream level of 1 is assigned to the terminus and all the flowline features in the main path upstream to the headwater of the stream. If the terminus drains into the ground or stops at the Canadian or Mexican border, a stream level of 4 is assigned to the terminus and all the flowline features in the main path upstream to the headwater of the stream. After the initial stream level of 1 or 4 is assigned to the terminus and its upstream path, all tributaries to that path are assigned a stream level incremented by 1. Then the tributaries to those stream paths are assigned a stream level incremented by 1. This continues until the entire stream network has been assigned stream levels | No |  |  |
| StreamOrde | A modified version of stream order as defined by Strahler. The Strahler stream order algorithm does not account for flow splits in the network. The algorithm for stream order here does take flow splits into consideration. | No |  |  |
| vpuin | Integer 0 or 1 indicates if flowline is an inflow to a Vector Processing Unit  (vpu), as defined in vpuid | No |  | 0 = not an inflow to a VPU <br> 1 = inflow to a VPU |
| vpuout | Integer 0 or 1 indicates if flowline is an outflow to a Vector Processing Unit  (vpu), as defined in vpuid | No |  | 0 = not an outflow to a VPU <br> 1 = outflow to a VPU |
| wbareatype | Character field that indicates the type of the waterbody a flowline is related to. Flowlines not related to a waterbody are NA | Yes |  | controlled vocabulary |
| slope | Numeric average slope of flowline | Yes |  |  |
| slopelenkm | Numeric length of flowline  used for slope calculation | No |  |  |
| FTYPE | Type of feature each flowline is designated as | Yes |  | controlled vocabulary |
| gnis_name | Feature Name from the Geographic Names Information System | Yes |  |  |
| gnis_id | Geographic Names Information System ID for the value in GNIS_Name | No |  |  |
| WBAREACOMI | comid of water body the flowline associates to | Yes |  |  |
| hwnodesqkm | Drainage area at the upstream node of a first order flowline | No |  |  |
| RPUID | Character identifier for raster processing unit flowline belongs to. nulls are null in source data | No |  |  |
| VPUID | Character identifier for vector processing unit flowline belongs to | No |  |  |
| roughness | Manning's N estimate for flowline | No |  |  |


**Notes on the data:**
- 

## Schema Diagram (TO ADD)
![Schema Diagram]()

**Legend description:** (TO ADD)
- 

## Controlled Vocabularies
- wbareatype
  - <<empty cell>>: not a waterbody
  - LakePond: Lake or pond
  - StreamRiver: Stream or river
  - Reservoir: Reservoir

- ftype
  - StreamRiver: stream or river
  - Connector: Connector
  - ArtificialPath: artificial path
  - CanalDitch: canal or ditch
  - LakePond: lake or pond

## Sample Data
- 

## Competency Questions
- 

## Contributors
- [David Kedrowski](https://github.com/dkedrowski)
