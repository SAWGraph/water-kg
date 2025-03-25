# Ohio Wells - Ohio Department of Natural Resources (ODNR)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Water Wells of Ohio |
| **Source agency:** | [Ohio Department of Natural Resources](https://ohiodnr.gov/home) |
| **Data source location:** | [Ohio Geology Interactive Map](https://gis.ohiodnr.gov/website/dgs/geologyviewer/#) <br/> [Groundwater Maps & Publications (safety-conservation/about-ODNR/geologic-survey)](https://ohiodnr.gov/discover-and-learn/safety-conservation/about-ODNR/geologic-survey/groundwater-resources/groundwater-maps-publications) <br/> [Groundwater Maps & Publications (land-water/ohio-river-watershed)](https://ohiodnr.gov/discover-and-learn/land-water/ohio-river-watershed/groundwater-maps-publications) |
| **Metadata description**: | [Descriptions of Geologic Map Units (pdf)](https://dam.assets.ohio.gov/image/upload/ohiodnr.gov/documents/geology/OFR98_1_Shrake_2011.pdf) |
| **Other metadata** | See the XML file included with each Shapefile |
| **Format of data**: | Shapefile |
| **Data Update Interval**: | January 12, 2021 |
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
| `oh_odnr:ODNR-Aquifer` | `oh_odnr_data:d.ODNR-Aquifer.<AQUA><fid>` |
| `geo:Geometry` | `oh_odnr_data:d.ODNR-Aquifer.geometry.<AQUA><fid>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)
### Consolidated/Bedrock Aquifers
| OHDNR Aquifer | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| fid | Internal feature number | Yes | `hyfo:hasPrimarySawgraphId` |  |
| AQUA | Abbreviation of the aquifer name | Yes | `hyfo:hasPrimarySawgraphId` | records with "na" are ignored |
| THICK | Relative thickness of the aquifer | Yes | `hyfo:hasThickness` | controlled vocabulary |
| YIELD | Yield of the aquifer | Yes | `hyfo:hasAquiferYield` | controlled vocabularly |
| created_by |  | No |  |  |
| created_date |  | No |  |  |
| edit_by |  | No |  |  |
| edit_date |  | No |  |  |
| Shape_STAr |  | No |  |  |
| Shape_STLe |  | No |  |  |

**Notes on the data:**

31 consolidated/bedrock aquifer shapefiles are organized as follows:

| Shapefile | Geologic Era | Principal Bedrock Type | Yield |
| --- | --- | --- | --- |
| dvnn_antrim | Devonian | carbonate | \< 5 gpm |
| dvnn_columbus_lucas | Devonian | carbonate | \>= 5 gpm |
| dvnn_delaware_columbus | Devonian | carbonate | \>= 5 gpm |
| dvnn_ohio_olentangy | Devonian | carbonate | \< 5 gpm |
| dvnn_trav_dun_detroitriver | Devonian | carbonate | \>= 5 gpm |
| mssp_bedford | Mississippian | sandstone | \< 5 gpm |
| mssp_bedford_cussewago | Mississippian | sandstone | \>= 5 gpm |
| mssp_berea | Mississippian | sandstone | \>= 5 gpm |
| mssp_berea_bedford | Mississippian | sandstone | \< 5 gpm |
| mssp_cold_sun_berea_bed | Mississippian | sandstone | \< 5 gpm |
| mssp_cuyahoga_group | Mississippian | sandstone | \>= 5 gpm |
| mssp_logan_blackhand | Mississippian | sandstone | \>= 5 gpm |
| mssp_logan_cuyahoga | Mississippian | sandstone | \>= 5 gpm |
| mssp_sun_berea_bed | Mississippian | sandstone | \< 5 gpm |
| mssp_sunbury | Mississippian | sandstone | \< 5 gpm |
| mssp_undivided | Mississippian | sandstone | \< 5 gpm |
| odvc_undivided | Ordovician | carbonate | \< 5 gpm |
| pnlv_allgny_lower_pttsvll | Pennsylvanian | sandstone | \>= 5 gpm |
| pnlv_allgny_pttsvll | Pennsylvanian | sandstone | \>= 5 gpm |
| pnlv_allgny_upper_pttsvll | Pennsylvanian | sandstone | \>= 5 gpm |
| pnlv_mnnghla_cnmgh | Pennsylvanian | sandstone | \< 5 gpm |
| pnlv_undivided | Pennsylvanian | sandstone | \< 5 gpm |
| prmn_dunkard | Permian | sandstone | \< 5 gpm |
| slrn_cedar_spring_euph | Silurian | carbonate | \>= 5 gpm |
| slrn_lockport_sublockport | Silurian | carbonate | \>= 5 gpm |
| slrn_massie_laurel_osg_day_brass | Silurian | carbonate | \>= 5 gpm |
| slrn_peeb_lilly_bish | Silurian | carbonate | \< 5 gpm |
| slrn_salina | Silurian | carbonate | \>= 5 gpm |
| slrn_salina_group | Silurian | carbonate | \>= 5 gpm |
| slrn_tym_green | Silurian | carbonate | \>= 5 gpm |
| slrn_tym_green_peeb_lilly_bish | Silurian | carbonate | \< 5 gpm |

### Unconsolidated/Glacial Aquifers
| OHDNR Aquifer | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| LITH | Abbreviation of the aquifer name | Yes | `hyfo:hasPrimarySawgraphId` | records with "na" are ignored |
| THICK | Relative thickness of the aquifer | Yes | `hyfo:hasThickness` | controlled vocabulary |
| THICKCODE | Relative thickness of the aquifer | Yes | `hyfo:hasThickness` | controlled vocabulary |
| YIELD | Yield of the aquifer | Yes | `hyfo:hasAquiferYield` | controlled vocabularly |
| YIELDCODE | Yield of the aquifer | Yes | `hyfo:hasAquiferYield` | controlled vocabularly |
| LOCAL |  |  |  |  |
| SETCODE |  |  |  |  |
| SETTING |  |  |  |  |
| NAME |  |  |  |  |
| created_by |  | No |  |  |
| created_date |  | No |  |  |
| edit_by |  | No |  |  |
| edit_date |  | No |  |  |
| Shape_Length |  | No |  |  |
| Shape_Area |  | No |  |  |
| fid |  |  |  |  |

## Controlled Vocabularies
**List 1. THICK** (consolidated/bedrock aquifers)
* \< 100 ft
* \> 100 ft
* ~ 100 ft (NOTE: this indicate the aquifer thickness was not rated)

**List 2. YIELD** (consolidated/bedrock aquifers)
* 0 - 5 gpm
* 5 - 25 gpm
* 25 - 100 gpm
* \> 100 gpm

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
