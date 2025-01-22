# Maine Wells - Maine Geological Survey (MGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Maine Well Database - Well Depth (located wells) <br/> Maine Well Database - Unlocated Wells |
| **Source agency:** | [Maine Geological Survey](https://www.maine.gov/dacf/mgs/) |
| **Data source location:** | [Located Wells](https://mgs-maine.opendata.arcgis.com/datasets/maine-well-database-well-depth/explore) <br/> [Unlocated wells](https://mgs-maine.opendata.arcgis.com/datasets/maine-well-database-unlocated-wells/explore) <br/> [Maine Geological Survey Rest Server](https://services1.arcgis.com/RbMX0mRVOFNTdLzd/ArcGIS/rest/services/MGS_Wells_Database/FeatureServer/0) |
| **Metadata description**: | [Located wells](https://mgs-maine.opendata.arcgis.com/datasets/maine::maine-well-database-well-depth/about) <br/> [Unlocated wells](https://mgs-maine.opendata.arcgis.com/datasets/maine::maine-well-database-unlocated-wells/about) <br/> [Maine Geological Survey Water Well Database Main Page](https://www.maine.gov/dacf/mgs/pubs/digital/well.htm) |
| **Other metadata** |  |
| **Format of data**: | ArcGIS REST Service (also with download options including CSV) |
| **Data Update Interval**: |  |
| **Location of triples:** | [SAWGraph me_mgs](https://drive.google.com/drive/u/0/folders/1Krihr-fqwLHb5d660EAgtSl0v1xz98dZ ) |

## Schema Diagram (TO ADD)
- [**Link to schema diagram on lucid chart**]()

## Code (TO ADD)
- mgs_wells.py
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `me_mgs:MGS_Well` | `me_mgs_data:d.MGS-Well.<WELLNO>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (TO ADD)

| MGS Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| *X* |  | Yes | geo:hasGeometry/geo:asWKT | *In located wells table only* | 
| *Y* |  | Yes | geo:hasGeometry/geo:asWKT | *In located wells table only* |
| WELLNO | Well Number | Yes | me_mgs:hasPrimaryStateAgencyId |  |
| WELL_LOCATION_TOWN | Town | ? |  | match to towns? |
| WELL_LOCATION_ADDRESS | Address | ? |  | match to parcels? |
| TAX_MAP_NO | Tax Map No | ? |  | match to parcels? |
| TAX_LOT_NO | Tax Map Lot No | ? |  | match to parcels? |
| DRILL_DATE | Drill Date | No  |  |   |
| DRILL_DATE_ESTIMATED | Drill Date Estimated | No |  | boolean <br/> ~15% of records |
| WELL_DRILLER_COMPANY | Driller | No |  |  |
| WELL_USE | Well Use | Yes | me_mgs:hasWaterUse | controlled vocabulary (see below) |
| WELL_TYPE | Well Type | Yes | hyfo:hasAquiferType | controlled vocabulary (see below) |
| WELL_CONSTRUCTION | Well Construction | No |  | controlled vocabulary (see below) <br/> ~19% of records |
| WELL_DEVELOPMENT | Well Development | No |  | controlled vocabulary (see below) <br/> ~45% of records |
| CASING_LENGTH_FT | Casing Length (ft) | Yes | hyfo:hasCasingDepth | sparse data in unlocated wells |
| OVERBURDEN_THICKNESS_FT | Overburden Thickness (ft) | Yes | hyfo:hasBedrockDepth | [sparse data] thickness of earth material until bedrock |
| WELL_DEPTH_FT | Well Depth (ft) | Yes | hyfo:hasTotalDepth |  |
| WELL_YIELD_MODIFIER | Yield Modifier | ? |  | '> (GREATER THAN)' or '< (LESS THAN)' <br/> ~2% of records |
| WELL_YIELD_GPM | Yield (GPM) | Yes | hyfo:hasYield | sparse in unlocated wells |
| YIELD_DATE | Yield Date | No |  | sparse |
| WELL_STATIC_LEVEL_FT | State Level (ft) | Yes | hyfo:hasStaticWaterDepth |  |
| WELL_STATIC_DATE | Static Level Date | No |  |  |
| VEIN1_DEPTH_FT | Vein1 Depth (ft) | No |  |  |
| VEIN1_YIELD_GPM | Vein1 Yield (gpm) | No |  |  |
| VEIN2_DEPTH_FT | Vein2 Depth (ft) | No |  |  |
| VEIN2_YIELD_GPM | Vein2 Yield (gpm) | No |  |  |
| VEIN3_DEPTH_FT | Vein3 Depth (ft) | No |  |  |
| VEIN3_YIELD_GPM | Vein3 Yield (gpm) | No |  |  |
| VEIN4_DEPTH_FT | Vein4 Depth (ft) | No |  |  |
| VEIN4_YIELD_GPM | Vein4 Yield (gpm) | No |  |  |
| REPLACEMENT_WELL | Replacement Well | No |  | boolean <br/> ~19% of records |
| GEOTHERMAL_WELL | Geothermal Well | No |  | boolean <br/> ~14% of records |
| WELL_COMMENT | Comment | No |  |  |
| *LOCATION_METHOD* | *Location Method* | No |  | *controlled vocabulary (see below)* <br/> *In located wells table only* |
| *LOCATION_ACCURACY* | *Location Accuracy* | No |  | *All entries are 0* <br/> *In located wells table only* |
| *LOCATION_DATE* | *Location Date* | No |  | *All entries are 0* <br/> *In located wells table only* |
| *LOCATION_UPDATED_DATE* | *Location Updated* | No |  | *All entries are 0* <br/> *In located wells table only* |
| *LATITUDE* | *Latitude* | No |  | *In located wells table only* |
| *LONGITUDE* | *Longitude* | No |  | *In located wells table only* |
| *WELL_YIELD_CLASS* |  | No |  | *In located wells table only* |
| *WELL _DEPTH_CLASS* |  | No |  | *In located wells table only* |
| *WELL_OVERBURDEN_THICKNESS_CLASS* |  | No |  | *In located wells table only* |
| WELLCARDNO |  | Yes | me_mgs:hasSecondaryStateAgencyId |  |
| HYDROFRACTURE |  | No |  |  |
| ERROR_REPORT_URL |  | No |  |  |
| *DATE_ENTERED* |  | No |  | *In located wells table only* |
| *DATE_EDITED* |  | No |  | *In located wells table only* |

**Notes on the data:**
- 

## Schema Diagram
- [*Draft* schema](https://lucid.app/lucidchart/16e658ef-6f61-4ce3-a770-0c410ecb194a/edit?viewport_loc=-1074%2C-511%2C3767%2C1853%2CssMfXgoENRPy&invitationId=inv_ea094a2c-59da-4347-b175-700b91e5623d)

**Legend description:** (TO ADD)
- 

## Controlled Vocabularies
**List 1. Well Use**
- Domestic
- Commercial
- Other
- Municipal
- Farm, Domestic
- Institutional
- Test
- Geothermal
- Industrial
- Irrigation
- Farm
- Observation
- Monitoring

**List 2. Well Type**
- Bedrock
- Gravel
- Overburden
- Spring
- Other
- Gravel Packed
- Dug
- Observation

**List 3. Well Construction**
- Drilled
- Rotary Drilled
- Dug
- Hammer Drilled
- Cable Tool
- Driven Point
- Jet
- Auger
- Drilled Overburden

**List 4. Well Development** 
- None
- Air
- Air/Water
- Other
- Jetting
- Blasting
- Dry Ice
- Dynamite
- Not Sure

**List 5. Location_Method**
- TAX MAP AND LOT
- GEOCODED STREET ADDRESS MAINE E911
- GPS
- DRILLER PROVIDED - OK	
- GEOCODED ADDRESS POINT MAINE E911	
- GEOCODED STREET ADDRESS OTHER	
- OWNER PROVIDED - OK	
- DRILLER PROVIDED - CORRECTED BY MGS	
- ORTHOIMAGERY	
- DRILLER PROVIDED - INCORRECT	
- OWNER PROVIDED - CORRECTED BY MGS

## Sample Data

## Competency Questions 

## Contributors
- Katrina Schweikert
- David Kedrowski
