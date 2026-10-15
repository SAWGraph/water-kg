# National Water-Well Database (NWWDB)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | National Water-Well Database (NWWDB): Derived Aquifer Properties and Harmonized Lithologic Logs for the Conterminous United States |
| **Source agency:** | [U.S. Geologic Survey](https://www.usgs.gov/) |
| **Data source location:** | [National Water-Well Database (NWWDB): Derived Aquifer Properties and Harmonized Lithologic Logs for the Conterminous United States](https://www.sciencebase.gov/catalog/item/61b897c9d34e9e224ac120de) <br/> Note: State files = original data and USGS files = processed data |
| **Metadata description**: | [National Water-Well Database (NWWDB): Derived Aquifer Properties and Harmonized Lithologic Logs for the Conterminous United States](https://www.sciencebase.gov/catalog/item/61b897c9d34e9e224ac120de) <br/> Note: See Data Dictionary csv file | 
| **Other metadata** |  |
| **Format of data**: | State-by-state .gpkg files with supporting .csv files <br/> One set for the original state data and one set for the USGS processed data <br/> Note: SAWGraph focuses on the NWWDB_Lite layer in the USGS processed packages |
| **Data Update Interval**: | Unknown: 3 states available as of 2026-10-15: MN, MI, LA |
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
| `nwwdb:NWWDB_Well` | `nwwdb_data:d.NWWDB_Well.<Well ID>` |
| `geo:Geometry` | `nwwdb_data:d.NWWDB_Well.geometry.<Well ID>` |

## Raw Data Attribute List and Mapping with Ontology Concepts (NWWDB_Lite layer)

The NWWDB_Lite table is a flattened version of the NWWDB dataset. It stores basic information about a water well such as its name and geographic location in addition to derived attributes summarizing the well construction details, water level measurements, lithologic material, and aquifer properties. Each water well is represented as a single row in the NWWDB_Lite table.

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| fid |  |  |  |  |
| gwWellName | Unique name or identifier of the well, typically a registration number assigned by the state agency that issued the well permit. |  |  |  |
| gwWellOtherName | Alternate name or identifier of the well, for example, if the same well has been assigned more than one identifier by different organizations. |  |  |  |
| gwWellPermitAgency | Agency that issued the permit for well construction, identified using the Research Organization Registry (ROR). |  |  |  |
| gwUnitName | The name or identifier of the primary hydrogeologic unit contributing water to the well. |  |  |  |
| gwWellTotalLength | Total length of the well relative to the reference elevation. |  |  |  |
| gwWellConstructedDepth | Constructed depth of the well relative to the reference elevation. |  |  |  |
| gwYield | Measurement of the yield of the well. |  |  |  |
| gwYieldType | Type of well yield, for example, the specific or safe yield. |  |  |  |
| gwWellBedrockDepth | Depth to bedrock from reference elevation. |  |  |  |
| xCoordinate | Horizontal x-coordinate of the well location using a projected coordinate reference system, for example, Albers equal-area conic projection for the conterminous United States (EPSG:5070). |  |  |  |
| yCoordinate | Horizontal y-coordinate of the well location using a projected coordinate reference system, for example, Albers equal-area conic projection for the conterminous United States (EPSG:5070). |  |  |  |
| latitude | Latitude of the well location using the WGS84 geodetic datum (EPSG:4326). |  |  |  |
| longitude | Longitude of the well location using the WGS84 geodetic datum (EPSG:4326). |  |  |  |
| positionalAccuracy | Description of the accuracy of the location measurement. |  |  |  |
| locationCRS | Coordinate reference system (CRS) associated with the horizontal coordinates of the well location. The CRS is identified using a code from the EPSG registry. |  |  |  |
| locationMeasurementMethod | Method used to determine the well location, for example, GPS, differential leveling, or topographic map. |  |  |  |
| locationSource | Organization that determined or reported the well location, identified using the Research Organization Registry (ROR). |  |  |  |
| locationDate | Date that the location of the well was determined using ISO 8601 formatting (YYYY-MM-DD). |  |  |  |
| elevation | The reference elevation for the well. |  |  |  |
| elevationAccuracy | Description of the accuracy of the elevation measurement. |  |  |  |
| elevationCRS | Coordinate reference system of the elevation measurement. |  |  |  |
| elevationMeasurementMethod | Method used to determine the reference elevation for the well, for example, GPS, Survey, or DEM. |  |  |  |
| elevationType | The type of reference elevation for the well, for example, top of casing or land surface. |  |  |  |
| elevationSource | Organization that determined or reported the elevation, identified using the Research Organization Registry (ROR). |  |  |  |
| elevationDate | Date that the reference elevation was determined using ISO 8601 formatting (YYYY-MM-DD). |  |  |  |
| casingFromDepth | Depth to the top of the first (shallowest) casing component relative to the borehole start point. |  |  |  |
| casingToDepth | Depth to the bottom of the last (deepest) casing component relative to the borehole start point. |  |  |  |
| casingMinDiameter | The smallest internal diameter of all casing component(s) in the well. |  |  |  |
| casingMaxDiameter | The largest internal diameter of all casing component(s) in the well. |  |  |  |
| casingCount | Number of casing components in the well. |  |  |  |
| screenFromDepth | Depth to the top of the first (shallowest) screen component relative to the borehole start point. |  |  |  |
| screenToDepth | Depth to the bottom of the last (deepest) screen component relative to the borehole start point. |  |  |  |
| screenMinDiameter | The smallest internal diameter of all screen component(s) in the well. |  |  |  |
| screenMaxDiameter | The largest internal diameter of all screen component(s) in the well. |  |  |  |
| screenCount | Number of screen components in the well. |  |  |  |
| boreholeDateOfDrilling | The earliest date of drilling reported for the well, if more than one drilling event occurred. |  |  |  |
| boreholeFromDepth | Depth to the top of the first (shallowest) borehole core interval relative to the borehole start point. |  |  |  |
| boreholeToDepth | Depth to the bottom of the last (deepest) borehole core interval relative to the borehole start point. |  |  |  |
| boreholeMinDiameter | The smallest internal diameter of all borehole core interval(s). |  |  |  |
| boreholeMaxDiameter | The largest internal diameter of all borehole core interval(s). |  |  |  |
| boreholeCount | Number of borehole core intervals, for example, in the case of telescoping wells or wells that have been deepened. |  |  |  |
| aquiferTestName | Name or identifier of the first aquifer test performed at the well (if more than one). |  |  |  |
| aquiferTestDate | Date that the aquifer test was performed. |  |  |  |
| aquiferFromDepth | Depth to the top of the aquifer that contributes water to the well. |  |  |  |
| aquiferToDepth | Depth to the bottom of the aquifer that contributes water to the well. |  |  |  |
| gwAquiferType | The type of aquifer that contributes water to the well, for example, unconfined vs. confined. |  |  |  |
| gwTransmissivity | Transmissivity estimate for the aquifer that contributes water to the well. |  |  |  |
| gwHydraulicConductivity | Hydraulic conductivity estimate for the aquifer that contributes water to the well. |  |  |  |
| aquiferTestCount | Number of aquifer tests performed at the well. |  |  |  |
| staticWaterDepthMin | The minimum (shallowest) of all water level measurement(s) recorded for the well. Negative water levels are indicative of artesian/flowing conditions. |  |  |  |
| staticWaterDepthMinDate | Date associated with the minimum water level recorded for the well. |  |  |  |
| staticWaterDepthMax | The maximum (deepest) of all water level measurement(s) recorded for the well. Negative water levels are indicative of artesian/flowing conditions. |  |  |  |
| staticWaterDepthMaxDate | Date associated with the maximum water level recorded for the well. |  |  |  |
| staticWaterDepthCount | Number of water level measurement(s) recorded for the well. |  |  |  |
| unconsolidatedThicknessMin | The minimum thickness of unconsolidated deposits observed at the location of the well and evidenced by the lithologic log. |  |  |  |
| unconsolidatedThicknessMax | The maximum or "actual" thickness of unconsolidated deposits observed at the location of the well and evidenced by the lithologic log. This value can only be reported for wells that fully penetrate the unconsolidated deposits. |  |  |  |
| coarseGrainedThicknessMin | The minimum thickness of coarse-grained deposits observed at the location of the well and evidenced by the lithologic log. |  |  |  |
| coarseGrainedThicknessMax | The maximum or "actual" thickness of coarse-grained deposits observed at the location of the well and evidenced by the lithologic log. This value can only be reported for wells that fully penetrate the unconsolidated deposits. |  |  |  |
| bedrockSurfaceLithology | Lithology of the first consolidated unit encountered in the well. The first consolidated unit is assumed to represent the bedrock surface, however, this may not be true for all geologic settings in the United States. |  |  |  |
| firstLithology | First lithology (nearest to the borehole start) encountered in the well. |  |  |  |
| lastLithology | Last lithology (farthest from the borehole start) encountered in the well. |  |  |  |
| lithologicUnitCount | Number of distinct units/intervals described in the lithologic log. |  |  |  |

**Notes on the data:**
- 

## Controlled Vocabularies - See Descriptions above
**List 1. Lithology Codes
| Code | Description | Vocabulary |
| --- | --- | --- |
| 0 | complete and consistent | `usgwd:FlagCounty.CompleteConsistent` |
| 1 | inconsistent | `usgwd:FlagCounty.Inconsistent` |
| 2 | incomparable due to missing coordinates or state-reported county | `usgwd:FlagCounty.IncomparableMissingInfo` |

## Sample Data

## Competency Questions 

## Contributors
- David Kedrowski

