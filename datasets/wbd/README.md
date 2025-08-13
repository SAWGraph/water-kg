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
| Instance Class | IRI Format |
| --- | --- |
| `wbd:HUC2` <br/> `wbd:HUC4` <br/> `wbd:HUC6` <br/> `wbd:HUC8` <br/> `wbd:HUC10` <br/> `wbd:HUC12` | `wbd_data:d.HUC2.<huc2>` <br/> `wbd_data:d.HUC4.<huc4>` <br/> `wbd_data:d.HUC6.<huc6>` <br/> `wbd_data:d.HUC8.<huc8>` <br/> `wbd_data:d.HUC10.<huc10>` <br/> `wbd_data:d.HUC12.<huc12>` |
| `geo:Geometry` | `wbd_data:d.HUC2.<huc2>.geometry` <br/> `wbd_data:d.HUC4.<huc4>.geometry` <br/> `wbd_data:d.HUC6.<huc6>.geometry` <br/> `wbd_data:d.HUC8.<huc8>.geometry` <br/> `wbd_data:d.HUC10.<huc10>.geometry` <br/> `wbd_data:d.HUC12.<huc12>.geometry` |

## Raw Data Attribute List and Mapping with Ontology Concepts
| Attribute | Description | Lift to graph | Ontology property | Comments |
| --- | --- | --- |--- | --- |
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
| name | Name refers to the GNIS name for the geographic area in which the hydrologic unit is located. | Yes | `schema:name` |  |
| shape_Length | Length of feature in internal units. | No |  |  |
| shape_Area | Area of feature in internal units squared. | No |  |  |
| hutype | The 12-digit hydrologic unit type attribute is the single-letter abbreviation for Watershed type from the list of official names provided in the WBD Standards. | Yes | `wbd:hucType` | HUC10 & HUC12 only <br/> See controlled vocabulary below |
| humod | Two-character, uppercase abbreviation used to track either a modification to natural overland flow that alters the location of the hydrologic unit boundary or special conditions that are applied to a specific boundary line segment. The value identifies the type of modification, from the list provided, that has been applied to the boundary segment. If more than one abbreviation is used, the list is separated by commas without spaces and organized from most to least predominant. | No |  | HUC10 & HUC12 only <br/> See controlled vocabulary below |
| hutype_description |  | Yes | `wbd:hucTypeDescription` | HUC10 & HUC12 only <br/> See controlled vocabulary below |
| tohuc | The 12-digit hydrologic unit ToHUC code attribute is the code for the 12-digit hydrologic unit that is downstream from and naturally receives the majority of the flow from another 12-digit hydrologic unit. | Yes | `wbd:toHUC` | HUC12 only |
| noncontributingareaacres | The noncontributing area attribute represents the area, in acres, of hydrologic units that do not contribute to downstream accumulation of streamflow under normal flow conditions. | No |  | HUC12 only |
| noncontributingareasqkm | The noncontributing area attribute represents the area, in square kilometers, of hydrologic units that do not contribute to downstream accumulation of streamflow under normal flow conditions. | No |  | HUC12 only |

**Notes on the data:**
* Need to add Canada as an Administrative Region 0 to fully capture `states` attribute

## Controlled Vocabularies 
List 1. humod
* GL - glacier
* IF - ice field
* KA - karst
* NC - non-contributing area

List 2. hutype - hutype_description
* S - Standard (An HU with drainage flowing to a single outlet point, excluding noncontributing areas.)
* F - Frontal (An HU that has more than one hydrologic feature discharging along the coastline of a lake, ocean, bay, playa, or other receiving feature.)
* C - Closed (An HU where no surface flow leaves through an outlet point.)
* M - Multiple outlet (An HU with more than one natural outlet; for example, an outlet located on a stream with multiple channels. This HUType classification does not include frontal or water hydrologic units, hydrologic units with artificial interbasin transfers, or drainage outlets through karst or shallow subsurface flow.)
* W - Water (An HU that is predominantly water but may include small land areas, for example, a lake, estuary, or harbor.)
* I - Island (An HU composed of one or more islands and adjacent water.)
* U - Urban (An HU in urban areas that are altered by engineered surface and subsurface drainage systems.)
* D - Indeterminant flow (An HU in areas of complex terrain or hydrology where flow within and connections between hydrologic units are uncertain or have the potential to change.)

## Sample Data

## Competency Questions

# Contributors
* [David Kedrowski](https://github.com/dkedrowski)
