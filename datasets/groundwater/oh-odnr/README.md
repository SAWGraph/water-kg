# Ohio Wells - Ohio Department of Natural Resources (ODNR)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Water Wells of Ohio |
| **Source agency:** | [Ohio Department of Natural Resources](https://ohiodnr.gov/home) |
| **Data source location:** | [Ohio Geology Interactive Map](https://gis.ohiodnr.gov/website/dgs/geologyviewer/#) <br/> [Groundwater Maps & Publications (safety-conservation/about-ODNR/geologic-survey)](https://ohiodnr.gov/discover-and-learn/safety-conservation/about-ODNR/geologic-survey/groundwater-resources/groundwater-maps-publications) <br/> [Groundwater Maps & Publications (land-water/ohio-river-watershed)](https://ohiodnr.gov/discover-and-learn/land-water/ohio-river-watershed/groundwater-maps-publications) |
| **Metadata description**: | [Descriptions of Geologic Map Units (pdf)](https://dam.assets.ohio.gov/image/upload/ohiodnr.gov/documents/geology/OFR98_1_Shrake_2011.pdf) |
| **Other metadata** | See the XML file included with each Shapefile |
| **Format of data**: | Bedrock (Consolidated): shapefiles <br/> Glacial (Unconsolidated): gdb |
| **Data Update Interval**: | Bedrock (Consolidated): January 12, 2021 <br/> Glacial (Unconsolidated): March 4, 2021 |
| **Location of triples:** |  |

## Schema Diagram (TO ADD)
* [*Draft* schema]()

**Legend description:** (TO ADD)
* 

## Code (TO ADD)
* ?.py
* [Code Directory]()
* [GDrive Output Directory]()

## Bedrock (Consolidated) Aquifers
### IRIs
| Instance Class | IRI Format |
| --- | --- |
| `oh_odnr:ODNR-Aquifer` | `oh_odnr_data:d.ODNR-Aquifer.<AQUA>-<fid>` |
| `geo:Geometry` | `oh_odnr_data:d.ODNR-Aquifer.geometry.<AQUA>-<fid>` |

### Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)
| OHDNR Aquifer | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| fid | Internal feature number | Yes | `hyfo:hasPrimarySawgraphId` |  |
| AQUA | Abbreviation of the aquifer name | Yes | `hyfo:hasPrimarySawgraphId` <br/> `hyfo:hasName`| records with "na" are ignored |
| THICK | Relative thickness of the aquifer | Yes | `hyfo:hasThickness` | controlled vocabulary |
| YIELD | Yield of the aquifer | Yes | `hyfo:hasAquiferYield` | controlled vocabularly |
| created_by |  | No |  |  |
| created_date |  | No |  |  |
| edit_by |  | No |  |  |
| edit_date |  | No |  |  |
| Shape_STAr |  | No |  |  |
| Shape_STLe |  | No |  |  |

**Notes on the data:**

31 bedrock (unconsolidated) aquifer shapefiles are organized as follows:

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

### Controlled Vocabularies
**List 1. THICK**
* \< 100 ft
* \> 100 ft
* ~ 100 ft (NOTE: this indicate the aquifer thickness was not rated)

**List 2. YIELD**
* 0 - 5 gpm
* 5 - 25 gpm
* 25 - 100 gpm
* \> 100 gpm

## Glacial (Unconsolidated) Aquifers
### IRIs
| Instance Class | IRI Format |
| --- | --- |
| `oh_odnr:ODNR-Aquifer` | `oh_odnr_data:d.ODNR-Aquifer.glacial-<OBJECTID>` |
| `geo:Geometry` | `oh_odnr_data:d.ODNR-Aquifer.geometry.glacial-<OBJECTID>` |

### Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)
| OHDNR Aquifer | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID |  | Yes | `hyfo:hasPrimarySawgraphId` |  |
| LITH | lithology | No |  | controlled vocabulary |
| THICK | thickness | Yes | `hyfo:hasThickness` | controlled vocabulary |
| THICKCODE |  | No |  | controlled vocabulary |
| YIELD | yield | Yes | `hyfo:hasAquiferYield` | controlled vocabularly |
| YIELDCODE |  | No |  | controlled vocabulary |
| LOCAL | local aquifer name | No |  |  |
| SETCODE |  | No |  | controlled vocabulary |
| SETTING | hydrogeologic setting | No |  | controlled vocabulary |
| NAME | complete aquifer name <br/> a concatenation of LOCAL and SETTING | Yes | `hyfo:hasName` |  |
| created_by |  | No |  |  |
| created_date |  | No |  |  |
| edit_by |  | No |  |  |
| edit_date |  | No |  |  |
| Shape_Length |  | No |  |  |
| Shape_Area |  | No |  |  |

### Controlled Vocabularies
**List 3. LITH** (definition)
* F (fines)
* Fsg (predominantly fines with sand and gravel lenses
* SG (sand and gravel)
* SGc (predominantly sand and gravel with clay lenses
* SGf (predominantly sand and gravel with fines lenses
* SGt (predominantly sand and gravel with till lenses
* T (till)
* Tsg (predominantly till with sand and gravel lenses)

**List 4. SETTINGCODE & SETTING**
* 1 = Buried Valley
* 2 = Ground Moiraine
* 3 = End Moiraine
* 4 = Lacustrine
* 5 = Thin Upland
* 6 = Alluvial
* 7 = Beach Ridge
* 8 = Outwash/Kame
* 9 = Complex
* 10 = Valley Fill
* 99 = NA

**List 5. THICKCODE & THICK**
* 0 = <_empty_>
* 1 = \< 25 ft
* 2 = 25 - 100 ft
* 3 = \> 100 ft
* 4 = NA

**List 6. YIELDCODE & YIELD**
* 0 = <_empty_>
* 1 = \< 5
* 2 = 5 - 25
* 3 = 25 - 100
* 4 = 100 - 500
* 5 = \> 500
* 99 = NA

## Sample Data

## Competency Questions 

## Contributors
* David Kedrowski
