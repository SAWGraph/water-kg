# United States Groundwater Well Database (USGWD)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | United States Groundwater Well Database (USGWD) |
| **Source agency:** | [A database of groundwater wells in the United States](https://www.nature.com/articles/s41597-024-03186-3) |
| **Data source location:** | [A Database of Groundwater Wells in the United States](https://www.hydroshare.org/resource/8b02895f02c14dd1a749bcc5584a5c55/) |
| **Metadata description**: | [A Database of Groundwater Wells in the United States](https://www.hydroshare.org/resource/8b02895f02c14dd1a749bcc5584a5c55/)|
| **Other metadata** |  |
| **Format of data**: | State-by-state shapefiles </br> State-by-state CSV files |
| **Data Update Interval**: | March 25, 2024 |
| **Location of triples:** | []() |

## Schema Diagram (TO ADD)
- [*Draft* schema]()

**Legend description:** (TO ADD)
- 

## Code (TO ADD)
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `usgwd:USGWD_Well` | `usgwd_data:d.USGWD_Well.<Well ID>` |
| `geo:Geometry` | `usgwd_data:d.USGWD_Well.geometry.<Well ID>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| Well ID | Unique well identifier assigned within USGWD | Yes | `usgwd:hasUSGWDID` | also used in IRI | 
| Well ID (State) | Unique well identifier given by the state | Yes | `usgwd:hasStateID` | Some of these values are in scientific notation | 
| Longitude | Longitude of well location in decimal degrees (NAD83) | Yes | `geo:hasGeometry/geo:asWKT` |  | 
| Latitude | Latitude of well location in decimal degrees (NAD83) | Yes | `geo:hasGeometry/geo:asWKT` |  | 
| County | County where well is located, as provided by state | No |  | Available via AR3 integration | 
| State | State where well is located | No |  | Available via AR3 integration | 
| FIPS | Federal Information Processing Standards state and county code for each well according to state-provided coordinates | No |  | Available via AR3 integration | 
| Aquifer-Specific | Specific aquifer, or aquifers, that the well overlays (assigned within this study) | Yes | `gwml2:gwWellUnit` | GebreEgziabher, M., Jasechko, S. & Perrone, D. Widespread and increased drilling of wells into fossil aquifers in the USA. Nat. Commun. 13, 2129 (2022). |
| Aquifer-Broad | General aquifer, or aquifer systems, that the well overlays (assigned within this study) | No |  | Available via Aquifer-Specific | 
| Subwatershed-HUC12 | 12-digit Hydrologic Unit Code (HUC12) subwatershed that the well is located (assigned within this study) | Yes | `kwg-ont:sfWithin` |  | 
| Subwatershed-Name | Name of the subwatershed that the well is located (assigned within this study) | No |  | Available via WBD data | 
| Location Verified | The location of the well was determined by GPS or field checked (Yes, No, Unknown) | Yes | `usgwd:locationVerified` | controlled vocabulary | 
| Flag County | Well outside its state-agency reported county (0: complete and consistent; 1: inconsistent; 2: incomparable due to missing coordinates or state-reported county) | Yes | `usgwd:flagCounty` | controlled vocabulary | 
| Flag State | Well outside its state-agency reported state (0: complete and consistent; 1: inconsistent; 2: incomparable due to missing coordinates) | Yes | `usgwd:flagState` | controlled vocabulary | 
| Flag US | Well’s coordinate outside of the US border (0: within the US border; 1: outside of the US border; 2: unknown due to missing coordinate) | Yes | `usgwd:flagUS` | controlled vocabulary | 
| Well Depth (Feet) | Total depth of well, measured in feet below land surface | Yes | `gwml2:gwWellTotalLength` |  | 
| Screen Depth (Feet) | Distance from land surface to the top of the well screen, measured in feet | Yes | `gwml2:gwWellConstructedDepth` |  | 
| Length of Screen (Feet) | Length of the well screen from the screen opening to the end of the screen, measured in feet | ? |  | Available via arithmetic | 
| Well Capacity (GPM) | Estimated amount of water the well can withdrawal, measured in gallons per minute | Yes | `gwml2:gwWellYield` |  | 
| Lithological Data | Known existence of lithological records (Yes, No) | No |  | controlled vocabulary | 
| Surface Elevation (Feet) | Elevation of the ground surface at the well head, in feet above sea level | No |  |  | 
| Status | Status of the well (Active, Inactive, Unknown) | Yes | `gwml2:gwWellStatus` | controlled vocabulary | 
| Year Well was Constructed | Year well was constructed; otherwise “Unknown” | Yes | `usgwd:constructedDuring` |  | 
| Year Reported | Year well was reported to the overseeing organization or the year in which it was entered into their system; otherwise “Unknown.” Often these two instances are the same. | Yes | `usgwd:reportedDuring` |  | 
| USGS Water Use Category | Primary use of the well identified by state, mapped to United States Geological Survey (USGS) definitions of sectoral water uses. Unknown is assigned if the value is blank or unclear (e.g., unused, destroyed, abandoned, or decommission). | Yes | `usgwd:hasUSGSWaterUse` | controlled vocabulary | 
| Irrigation Subcategory (State) | Subcategory for well records with irrigation water use in the USGS Water Use Category. The subcategories include Irrigation-Crop (IR-C), Irrigation-Golf Courses (IR-G), and Irrigation-Unknown (IR-U), which are derived from the state's original water use data. Everything not belonging to IR-C or IR-G will be classified into IR-U. | Yes |  | controlled vocabulary </br> Merge with water use | 
| Irrigation Subcategory (Land Use) | Subcategory for well records with irrigation water use in the USGS Water Use Category. The subcategories include Irrigation-Crop (IR-C), Irrigation-Golf Courses (IR-G), and Irrigation-Unknown (IR-U), which are assigned by this study using the well's coordination and Regrid land parcel data and Open Street Map. Everything not belonging to IR-C or IR-G will be classified into IR-U. | Yes |  | controlled vocabulary </br> Merge with water use | 
| Water Quality (Potable/Non-Potable) | Distinction between potable and non-potable water (Yes, No) | Yes | `usgwd:potable` | controlled vocabulary | 
| Flag Duplicate | Indicate potential duplicated records based on Well ID (State), Longitude, and Latitude (0: unique; 1: incomparable due to missing state-assigned well id; 2: shares identical values with one or more other records; 3: Well ID (State), Longitude, and Latitude are identical but differ in some other attributes) | Yes | `usgwd:flagDuplicate` | controlled vocabulary | 


**Notes on the data:**
- 

## Controlled Vocabularies - See Descriptions above
**List 1. Flag County
| Code | Description | Vocabulary |
| --- | --- | --- |
| 0 | complete and consistent | `usgwd:FlagCounty.CompleteConsistent` |
| 1 | inconsistent | `usgwd:FlagCounty.Inconsistent` |
| 2 | incomparable due to missing coordinates or state-reported county | `usgwd:FlagCounty.IncomparableMissingInfo` |

**List 2. Flag State
| Code | Description | Vocabulary |
| --- | --- | --- |
| 0 | complete and consistent | `usgwd:FlagState.CompleteConsistent` |
| 1 | inconsistent | `usgwd:FlagState.Inconsistent` |
| 2 | incomparable due to missing coordinates | `usgwd:FlagState.IncomparableMissingInfo` |

**List 3. Flag US
| Code | Description | Vocabulary |
| --- | --- | --- |
| 0 | within the US border | `usgwd:FlagUS.WithinBorder` |
| 1 | outside of the US border | `usgwd:FlagUS.OutsideBorder` |
| 2 | unknown due to missing coordinate | `usgwd:FlagUS.UnknownMissingInfo` |

**List 4. Flag Duplicate
| Code | Description | Vocabulary |
| --- | --- | --- |
| 0 | unique | `usgwd:FlagDuplicate.Unique` |
| 1 | incomparable due to missing state-assigned well id | `usgwd:FlagDuplicate.IncomparableMissingInfo` |
| 2 | shares identical values with one or more other records | `usgwd:FlagDuplicate.SharesIdenticalValues` |
| 3 | Well ID (State), Longitude, and Latitude are identical but differ in some other attributes | `usgwd:FlagDuplicate.SharesIdentifyingValues` |

## Sample Data

## Competency Questions 

## Contributors
- David Kedrowski

