## Dataset Overview
* **Name of dataset:** NHDWaterbody.shp (there is one file for each Vector Processing Unit (VPU)/2-digit Hydrologic Unit (HUC2))
* **Source Agency:** [United States Geological Survey](https://www.usgs.gov/)
* **Data source location:** [Get NHDPlus (National Hydrography Dataset Plus) Data](https://www.epa.gov/waterdata/get-nhdplus-national-hydrography-dataset-plus-data#v2datamap)
* **Metadata description:** [NHD*Plus Version2*: User Guide](https://www.epa.gov/system/files/documents/2023-04/NHDPlusV2_User_Guide.pdf)
* **Other metadata:** 
* **Format of data:** .shp file
* **Data update interval:** no longer maintained but still available and widely used
* **General comments**:

## Schema Diagram (TO ADD)
[**Link to schema diagram on lucid chart**]()

## Code (TO ADD)
* [Code Directory]()
* [GDrive Output Directory]()

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)
| NHDWaterbody | Description | Lift to graph | Ontology property |
| --- | --- | --- |--- |
| COMID | Common identifier | Yes | nhdplusv2:hasCOMID |
| FDATE | Feature currency date | No |  |
| RESOLUTION | high, medium, local | No |  |
| GNIS_ID | GNIS ID for GNIS_NAME | No |  |
| GNIS_NAME | Name from GNIS | Yes | schema:name |
| AREASQKM | Area in square kilometers | No |  |
| ELEVATION | Elevation in ft | No |  |
| REACHCODE | Reach code | Yes | nhdplusv2:hasReachCode |
| FTYPE | [NHD feature type](https://files.hawaii.gov/dbedt/op/gis/data/NHD%20Complete%20FCode%20Attribute%20Value%20List.pdf) | Yes | nhdplusv2:hasFTYPE |
| FCODE | [NHD feature type code](https://files.hawaii.gov/dbedt/op/gis/data/NHD%20Complete%20FCode%20Attribute%20Value%20List.pdf) | Yes | nhdplusv2:hasFCODE |
| SHAPE_LENG | length in decimal degrees | No |  |
| SHAPE_AREA | area in square decimal degrees | No |  |
| geometry | Polygon | Yes | geo:hasGeometry/geo:asWKT |

**Notes on the data:**
- 

## Schema Diagram (TO ADD)
![Schema Diagram]()

**Legend description:** (TO ADD)
- 

## Controlled Vocabularies 

## Sample Data

## Competency Questions 

## Contributors
* [David Kedrowski](https://github.com/dkedrowski)
