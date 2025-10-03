# Secondary Hydrogeologic Regions of the Conterminous US - United States Geological Survey (USGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Hydrogeologic Settings of the Conterminous United States |
| **Source agency:** | [United States Geological Survey](https://www.usgs.gov/) |
| **Data source location:** | [Data for depth of groundwater used for drinking-water supplies in the United States](https://www.sciencebase.gov/catalog/item/5e43efc3e4b0edb47be84c3d) |
| **Metadata description**: | [Metadata](https://www.sciencebase.gov/catalog/file/get/5e43efc3e4b0edb47be84c3d?f=__disk__f6%2Fb5%2F6e%2Ff6b56ecf03139fd16996eebce6a7e5ef7e15266a&transform=1&allowOpen=true) |
| **Other metadata** |  |
| **Format of data**: | .shp files |
| **Data Update Interval**: | Last updated November 15, 2021 |
| **Location of triples:** |  |

## Schema Diagram (TO ADD)
- [*Draft* schema]()

**Legend description:** (TO ADD)
- 

## Code (TO ADD)
- ?.py
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
<!-- | `me_mgs:MGS_Aquifer` | `me_mgs_data:d.MGS_Aquifer.<OBJECTID>` | -->
<!-- | `geo:Geometry` | `me_mgs_data:d.MGS_Aquifer.geometry.<OBJECTID>` | -->

## Raw Data Attribute List and Mapping with Ontology Concepts

**Examples of triples from data/metadata sources**
<!-- * `me_mgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel" -->
<!-- * `me_mgs:GW_Aquifer hyfo:hasDescription` "Maine aquifer systems consist of aquifers within 100m of each other" -->

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| PASHR_ID | An identifier for the principal aquifer or secondary hydrogeologic region (The first letter is P for principal aquifers, S for secondary hydrogeologic regions. The numbers match those used in Figure 1 of Lovelace and others (2020) for principal aquifers and Figure 3 of Belitz and others (2018) for secondary hydrogeologic regions) | Yes | `usgs:hasHGSettingId` | Not unique, so combined with Overlay attribute |
| PASHR | Names of principal aquifer or secondary hydrogeologic region | Yes | `usgs:hasPAorSHRName` |  |
| Overlay | Overlying sediment type if present | Yes | `usgs:hasHGSettingId` <br> `usgs:hasOverlay` | Not unique, so combined with PASHR_ID attribute <br> Controlled vocabulary |
| HG_Setting | Hydrogeologic setting name (A combination of the name of the principal aquifer or secondary hydrogeologic region and overlying sediment type acronym) | Yes | `usgs:hasHGSettingName` |  |
| Lithology | Hydrogeologic setting lithology | Yes | `usgs:hasLithology` | Controlled vocabulary |
| DomMedTop | Median depth to the top of the open interval of domestic-supply wells by hydrogeologic setting | Yes | `usgs:hasDomesticMedianTopDepth` | units are feet |
| DomMedBot | Median depth to the bottom of open interval of domestic-supply wells by hydrogeologic setting | Yes | `usgs:hasDomesticMedianBottomDepth` | units are feet |
| DomMedOL | Median open interval length of domestic-supply wells by hydrogeologic setting | Yes | `usgs:hasDomesticMedianOpenIntervalLength` | units are feet |
| PubMedTop | Median depth to the top of the open interval of public-supply wells by hydrogeologic setting | Yes | `usgs:hasPublicMedianTopDepth` | units are feet |
| PubMedBot | Median depth to the bottom of the public-supply well groundwater-withdrawal zone by hydrogeologic setting | Yes | `usgs:hasPublicMedianBottomDepth` | units are feet |
| PubMedOL | median open interval length of public-supply wells by hydrogeologic setting | Yes | `usgs:hasPublicMedianOpenIntervalLength` | units are feet |
| HG_Setti_1 | An alternative hydrogeologic setting name (A combination of the name of the principal aquifer or secondary hydrogeologic region and overlying sediment type acronym, if present.  Differs from HG_Settting in that setting without overlying sediment do not have AA suffix) | No |  |  |

**Notes on the data:**
- 

## Controlled Vocabularies
**List 1. Overlay
* AA - no overlying sediment
* AV - stream valley alluvium
* G - glacial sediment that is not coarse stratified
* GC - coarse-stratified glacial sediment

**List 2. Lithology
* Carbonate-rock aquifers
* Crystalline
* Igneous and metamorphic-rock aquifers
* Mixed
* Sandstone and carbonate-rock aquifers
* Sandstone aquifers
* Sedimentary
* Semiconsolidated sand aquifers
* Unconsolidated sand and gravel aquifers
* Volcanic

## Sample Data

## Competency Questions 

## Contributors
- David Kedrowski
