# HUC2 (Region), HUC4 (Subregion), HUC6 (Basin), HUC8 (Subbasin), <br/> HUC10 (Watershed), <br/> HUC12 (Subwatershed)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | WBDHU2, WBDHU4, WBDHU6, WBDHU8, WBDHU10, WBDHU12 <br/> Each VPU (HUC2) has a .gpkg with a layer for each HUC level |
| **Source Agency:** | [United States Geological Survey](https://www.usgs.gov/) |
| **Data source location:** | [The National Map](https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/Hydrography/WBD/HU2/GPKG/) <br/> WBD_##_HU2_GPKG.zip files |
| **Metadata description:** | See the .xml file associated with each .gpkg file for each VPU (HUC2) |
| **Other metadata:** | [Federal Standards and Procedures for the National Watershed Boundary Dataset (WBD)](https://pubs.usgs.gov/tm/11/a3/) |
| **Format of data:** | .gpkg layer |
| **Data update interval:** | January 8, 2025 |
| **General comments**: |  |

## Schema Diagram (TO ADD)
* [Link to schema diagram on lucid chart]()

**Legend description:** (TO ADD)
*  

## Code and Triples (TO ADD)
* [Code Directory]()
* [GDrive Output Directory]()

## IRIs
Reuse IRIs from Geoconnex

Define `@prefix wbd_gcx: <https://geoconnex.us/ref/>`
* Geoconnex does not include 12-digit HUCs
* Not all entities exist in the Geoconnex graph, but these IRIs dereference to the Geoconnex Reference Server
* Geoconnex does not include links to geometries in either their KG or their Reference Server

Define `@prefix wbd: <https://wbd.spatialai.org/v1/wbd#>`

Define `@prefix wbd_data: <https://wbd.spatialai.org/v1/wbd-data#>`

| Instance Class | IRI Format |
| --- | --- |
| `wbd:HU02` <br/> `wbd:HU04` <br/> `wbd:HU06` <br/> `wbd:HU08` <br/> `wbd:HU10` <br/> `wbd:HU12` | `wbd_gcx:hu02/<2-digit id>` <br/> `wbd_gcx:hu04/<4-digit id>` <br/> `wbd_gcx:hu06/<6-digit id>` <br/> `wbd_gcx:hu08/<8-digit id>` <br/> `wbd_gcx:hu10/<10-digit id>` <br/> `wbd_gcx:hu12/<12-digit id>` |
| `geo:Geometry` | `wbd_data:d.HU02.<2-digit id>.geometry` <br/> `wbd_data:d.HU04.<4-digit id>.geometry` <br/> `wbd_data:d.HU06.<6-digit id>.geometry` <br/> `wbd_data:d.HU08.<8-digit id>.geometry` <br/> `wbd_data:d.HU10.<10-digit id>.geometry` <br/> `wbd_data:d.HU12.<12-digit id>.geometry` |

## Raw Data Attribute List and Mapping with Ontology Concepts
| Attribute | Description | Lift to graph | Ontology property | Comments |
| --- | --- | :---: | --- | --- |
| objectid | Internal feature number. | No |  |  |
| tnmid | TNMID (short for The National Map Identification) is a unique 40-character field that identifies each element in the database exclusively. | No |  |  |
| metasourceid | MetaSourceID is a unique identifier that links the element to the metadata tables. | No |  |  |
| sourcedatadesc | SourceDataDesc is a space provided for a brief description of the type of base data used to update or change the current WBD. | No |  |  |
| sourceoriginator | SourceOriginator is the description of the agency that created the base data used to improve the WBD. | No |  |  |
| sourcefeatured | SourceFeatureID is a long, unique code. This code identifies the parent of the feature if the feature is the result of a split or merge. | No |  |  |
| loaddate | LoadDate represents the date when the data were loaded into the official USGS WBD ArcSDE database. The field is the effective date for all feature edits. | No |  |  |
| referencegnis_ids | Holds one or more Geographic Names Information System (GNIS) IDs of the feature or features for which the HU is named. Multiple GNIS IDs in the field are organized by listing the GNIS ID of the primary feature followed by the GNIS ID of additional features | No |  | Empty for all HUC levels in New England |
| areaacres | The area of each hydrologic unit including non-contributing areas stored in acres. | No |  |  |
| areasqkm | The area of each hydrologic unit including non-contributing areas stored in square kilometers. | No |  |  |
| states | The States or outlying area attribute identifies the State(s) or outlying areas that the hydrologic unit falls within or touches. | Yes | `wbd:hucState` | Object property connecting to Administrative Region 1 instances |
| huc<#> | The HUC# field is a unique #-digit hydrologic unit code <br> # is 2 (region), 4 (subregion), 6 (basin), 8 (subbasin), 10 (watershed), or 12 (subwatershed) | Yes | `wbd:hucCode` | Use as unique identifier |
| name | Name refers to the GNIS name for the geographic area in which the hydrologic unit is located. | Yes | `schema:name` | This exists in the Geoconnex KG |
| shape_Length | Length of feature in internal units. | No |  |  |
| shape_Area | Area of feature in internal units squared. | No |  |  |
| hutype | The 10-digit hydrologic unit type attribute is the single-letter abbreviation for Watershed type from the list of official names provided in the WBD Standards. | Yes | `wbd:hucType` | HUC10+ only <br/> See controlled vocabulary below |
| humod | Two-character, uppercase abbreviation used to track either a modification to natural overland flow that alters the location of the hydrologic unit boundary or special conditions that are applied to a specific boundary line segment. The value identifies the type of modification, from the list provided, that has been applied to the boundary segment. If more than one abbreviation is used, the list is separated by commas without spaces and organized from most to least predominant. | No |  | HUC10+ only <br/> See controlled vocabulary below |
| hutype_description |  | Yes | `wbd:hucTypeDescription` | HUC10+ only <br/> See controlled vocabulary below |
| tohuc | The 12-digit hydrologic unit ToHUC code attribute is the code for the 12-digit hydrologic unit that is downstream from and naturally receives the majority of the flow from another 12-digit hydrologic unit. | Yes | `wbd:toHUC` | HUC12+ only |
| noncontributingareaacres | The noncontributing area attribute represents the area, in acres, of hydrologic units that do not contribute to downstream accumulation of streamflow under normal flow conditions. | No |  | HUC12+ only |
| noncontributingareasqkm | The noncontributing area attribute represents the area, in square kilometers, of hydrologic units that do not contribute to downstream accumulation of streamflow under normal flow conditions. | No |  | HUC12+ only |

**Notes on the data:**
* Need to add Canada and Mexico as Administrative Region 1 entity to fully capture `states` attribute
* Geoconnex uses `hyf:containingCatchment` to capture the nesting of HUs; for example, every HU12 is within a HU10, HU08, HU06, HU04, and HU02. Geoconnex declares all of these explicitly but transitivity could be used as well to reduce the number of explicit triples.

## Controlled Vocabularies 
List 1. humod
| “HUMod” code | “HUMod” description | “HUMod” definition |
| :---: | --- | --- |
| AW | Artificial waterway | A canal, ditch, or drain used to transport surface water that alters the natural flow out of the hydrologic unit. Withdrawing and receiving hydrologic units should carry this designation, as well as all hydrologic units in which the flow is altered by an artificial waterway. <br> *Retired codes AD (Aqueduct), DD (Drainage Ditch), GC (General Canal/Ditch), ID (Irrigation Ditch), IT (Interbasin Transfer), SD (Stormwater Ditch), SC (Stormwater Canal), and BC (Barge Canal) are grouped into this single modification code.* |
| GF | Groundwater or shallow subsurface flow | Hydrologic unit in which most of the runoff drains underground. |
| GL | Glacier | The hydrologic unit crosses or includes a body or stream of ice moving outward and downslope from an area of accumulation; area of relatively permanent snow or ice on the top or side of a mountain or mountainous area. |
| IF | Ice field | The hydrologic unit crosses or includes a field of ice, formed in regions of perennial frost. |
| KA | Karst | The hydrologic unit is within an area of, or includes an area of, geologic formations of irregular limestone deposits with sinks, underground streams, or caverns. |
| LA | Lava field | The hydrologic unit contains or crosses nearly flat-lying lava flows. |
| MA | Mining activity | Topographic modification by surface mining that alters the natural flow in or out of the hydrologic unit. |
| NC | Noncontributing area | A naturally formed area that does not contribute surface-water runoff to a hydrologic unit outlet under normal conditions, for example, a playa. This does not include groundwater flow. |
| NM | No modifications | No modifications are present. Use if no other options with the modification domain have been cited. |
| OC | Overflow channel or flume | An artificial channel built to control excess high flow from a natural channel; alters the natural flow out of the hydrologic unit. |
| OF | Overbank flow | A natural condition in which a stream surpasses bankfull stage and the excess flows into a nearby channel draining to a different hydrologic unit. The losing and receiving hydrologic units should both carry the HUMod code “OF”. An example of overbank flow is shown in figure 3. |
| PD | Pipe diversion | A redirection of surface water by a pipeline from one hydrologic unit to another, which alters the natural flow into or out of the hydrologic unit. |
| PS | Pumping station | A facility along a stream or other water body used to move water over a levee or other obstruction that alters the natural boundary location. |
| RC | Receiving | A hydrologic unit that receives diverted water. |
| RS | Reservoir | A constructed basin formed to contain and store water for future use in an artificial lake; alters the natural flow out of the hydrologic unit. |
| SI | Siphon | An artificial diversion, which is usually named “siphon” on maps, to move surface water from one stream channel to another; alters the natural boundary location. |
| UA | Urban area | Heavy modification of hydrologic unit topography by urban development. |
| WD | Withdrawal | A hydrologic unit from which water is diverted. |

List 2. Hydrologic unit type (Note: *"HUType" description* values populate both `hutype` and `hutype_description` attributes in the shapefiles)
| "HUType" code | "HUType" description | "HUType" definition |
| :---: | :---: | --- |
| C | Closed Basin | An HU where no surface flow leaves through an outlet point. |
| D | Indeterminant Flow | An HU in areas of complex terrain or hydrology where flow within and connections between hydrologic units are uncertain or have the potential to change. |
| F | Frontal | An HU that has more than one hydrologic feature discharging along the coastline of a lake, ocean, bay, playa, or other receiving feature. |
| I | Island | An HU composed of one or more islands and adjacent water. |
| M | Multiple Outlet | An HU with more than one natural outlet; for example, an outlet located on a stream with multiple channels. This HUType classification does not include frontal or water hydrologic units, hydrologic units with artificial interbasin transfers, or drainage outlets through karst or shallow subsurface flow. |
| S | Standard | An HU with drainage flowing to a single outlet point, excluding noncontributing areas. |
| U | Urban | An HU in urban areas that are altered by engineered surface and subsurface drainage systems. |
| W | Water | An HU that is predominantly water but may include small land areas, for example, a lake, estuary, or harbor. |

## Sample Data

## Competency Questions

# Contributors
* [David Kedrowski](https://github.com/dkedrowski)
