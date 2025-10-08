# Secondary Hydrogeologic Regions of the Conterminous US - United States Geological Survey (USGS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Secondary Hydrogeologic Regions of the Conterminous United States |
| **Source agency:** | [United States Geological Survey](https://www.usgs.gov/) |
| **Data source location:** | [Secondary Hydrogeologic Regions of the Conterminous United States](https://www.sciencebase.gov/catalog/item/5a5643b6e4b01e7be24449fc) |
| **Metadata description**: | [Metadata](https://www.sciencebase.gov/catalog/file/get/5a5643b6e4b01e7be24449fc?f=__disk__0c%2F28%2F49%2F0c2849f573af3233fad59dd89b5fa8a69b033060&transform=1&allowOpen=true) |
| **Other metadata** |  |
| **Format of data**: | .shp files |
| **Data Update Interval**: | Last updated June 29, 2022 |
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

Reuse IRIs from Geoconnex ?

Define `@prefix gcx: <https://geoconnex.us/ref/`
* Geoconnex does not include links to geometries in either their KG or their Reference Server

Define `@prefix usgs: <https://usgs.spatialai.org/v1/usgs#>`

Define `@prefix usgs_data: <https://usgs.spatialai.org/v1/usgs-data#>`

| Instance Class | IRI Format |
| --- | --- |
| `gwml2s:GW_HydrogeoUnit` | `gcx:sec_hydrg_reg/<SHR_ID>` | -->
| `geo:Geometry` | `usgs_data:d.USGS_Secondary_Hydrogeo_Region_<SHR_ID>.geometry` | -->

## Raw Data Attribute List and Mapping with Ontology Concepts

**Examples of triples from data/metadata sources**
<!-- * `me_mgs:GW_Aquifer hyfo:hasAquiferMaterial` "sand and gravel" -->
<!-- * `me_mgs:GW_Aquifer hyfo:hasDescription` "Maine aquifer systems consist of aquifers within 100m of each other" -->

| Attribute | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| OBJECTID | Internal feature number | No |  |  |
| SHR | Secondary Hydrogeologic Regions are ORRs of comparable age, lithology, and relationship to Principal Aquifers or glacial deposits. | Yes | `usgs:hasSHRName` |  |
| KM2 | Size of the Secondary Hydrogeologic Unit, in square kilometers. | No |  |  |
| PrimaryLith | Primary Lithology of the Secondary Hydrogeologic Region, derived from the "ROCKTYPE" attribute in Other_Aquifers feature class.  Named PrimaryLit in shapefile version. | Yes | `usgs:hasLithology` | Controlled vocabulary |
| Type | Classification of Secondary Hydrogeologic Regions by type, where type indicates the relationship between an SHR and the presence or absence of underlying Principal Aquifers (PAs) or overlying glacial deposits. | Yes | `usgs:hasSHRType` | Controlled vocabulary |
| GeologicProvince | Geologic province associated with each Secondary Hydrogeologic Regions, as identified by Reed and Bush, 2007.  Named GeologicPr in shapefile version. | Yes | `usgs:hasGeolProvince` | Controlled vocabulary |
| Subprovince | Subprovince of geologic provinces associated with each Secondary Hydrogeologic Regions. Named Subprovinc in shapefile version. | Yes | `usgs:hasGeolSubprovnice` | Controlled vocabulary |
| Shape_Length | Length of feature in internal units (meters).  Named Shape_Leng in shapefile version. | No |  |  |
| Shape_Area | Area of feature in internal units squared (meters). | No |  |  |
| SHR_ID | The number following the leading "S" in SHR_ID corresponds to the numbering shown in Figure 1 of this data release and figure 3 in the associated larger work [](https://ngwa.onlinelibrary.wiley.com/doi/10.1111/gwat.12806). | Yes | `usgs:hasSHRId` | Use as unique identifier |
| SHR_CODE | SHR_Code is a combination of the SHR_ID and a shortened version of the SHR. | No |  |  |

**Notes on the data:**
- 

## Controlled Vocabularies
**List 1. PrimaryLith
* Crystalline
* Mixed
* Sedimentary
* Volcanic

**List 2. Type
* NN - Not underlain by Principal Aquifers and not overlain by glacial deposits
* NY - Not underlain by Principal Aquifers and overlain by glacial deposits
* YN - Underlain by Principal Aquifers and not overlain by glacial deposits
* YY - Underlain by Principal Aquifers and overlain by glacial deposits

**List 3. GeologicProvince - Subprovince
* Appalachian - Appalachian, Ouachita
* Central Interior - Glaciated, Unglaciated
* Coastal Plain - Coastal Plain
* Cordilleran - Intermountain, Rocky Mountains, Western

## Sample Data

## Competency Questions 

## Contributors
- David Kedrowski
