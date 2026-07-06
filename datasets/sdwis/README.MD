# Safe Drinking Water Information System (SDWIS)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Safe Drinking Water Information System (SDWIS) |
| **Source Agency:** | [EPA](https://www.epa.gov/) |
| **Data source location:** | <!-- [Drinking Water State `\|` EPA Pfas analytic tools downloads](https://echo.epa.gov/trends/pfas-tools#data) <br/> --> [SDWA Dataset `\|` ECHO data downloads](https://echo.epa.gov/tools/data-downloads#drinkingwater) <br/> [Water System Boundaries](https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/Water_System_Boundaries/FeatureServer) |
| **Additional data sources:** | [SDWIS Federal Reports Search](https://sdwis.epa.gov/ords/sfdw_pub/r/sfdw/sdwis_fed_reports_public/200)
| **Metadata description:** | [Envirofacts model](https://enviro.epa.gov/envirofacts/metadata/model/sdwis) <br/> [SDWA download summary](https://echo.epa.gov/tools/data-downloads/sdwa-download-summary#sdwis) <br/> [Community Water System Service Area Boundaries](https://www.epa.gov/ground-water-and-drinking-water/community-water-system-service-area-boundaries?tab=map) <br/> [Water System Boundaries](https://epa.maps.arcgis.com/home/item.html?id=80c6912ef14f46e480f5afd807767b4b) <br/> [ORB_SAB_Model Github](https://github.com/USEPA/ORD_SAB_Model) |
| **Format of data returned:** | XLSX, CSV, (API available with json but has less tables), esri rest service (CWS boundaries) |
| **General Comments:** | SDWIS features are contained in the hydrology repo (and share geoconnex uris when available). Sampling reports from SDWIS regarding pfas are contained in the PFAS-KG repo. |

## Schema Diagram

[draft](https://lucid.app/lucidchart/16e658ef-6f61-4ce3-a770-0c410ecb194a/edit?viewport_loc=2887%2C55%2C2505%2C1076%2CO.sGt549hds0&invitationId=inv_ea094a2c-59da-4347-b175-700b91e5623d)

**Legend description:** (TO ADD)
*  

## Code and Triples (TO ADD)
* [Code Directory](https://github.com/SAWGraph/water-kg/tree/main/datasets/sdwis)
  * pws_serviceAreas_cws-ncws.py
  * sdwa_controlledVocab.py
* [GDrive Output Directory]()

## IRIs
Geoconnex does not include links to geometries in either their KG or their Reference Server

Define `@prefix us_sdwis: <http://sawgraph.spatialai.org/v1/us-sdwis#>`

Define `@prefix us_sdwis_data: <http://sawgraph.spatialai.org/v1/us-sdwis-data#>`

| Instance Class | IRI Format |
| --- | --- |
| `us_sdwis:PublicWaterSupply` | `http://geoconnex.us/ref/pws/<PWSID>` |
| `us_sdwis:PWS-ServiceArea` | `us_sdwis_data:d.PWS-ServiceArea.<PWSID>` |
| `geo:Geometry` | `us_sdwis_data:d.PWS-ServiceArea.<PWSID>` |

Note: Instances of the first two types are related by `http://geoconnex.us/ref/pws/<PWSID> us_sdwis:serviceArea us_sdwis_data:d.PWS-ServiceArea.<PWSID>`

## Raw Data Attribute List and Mapping with Ontology Concepts

### SDWIS download tables

#### Table: SDWA_PUB_WATER_SYSTEMS.csv

<!-- > **code**: *sdwa_pws.py* -->

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| SUBMISSIONYEARQUARTER | Fiscal year and quarter of the quarterly snapshot of SDWIS. | ? |  |  |
| PWSID | Unique identifying code for a public water system in SDWIS. The PWSID consists of a two-letter state or region code, followed by seven digits. | Yes | `us_sdwis:pwsId` | Also in IRI |
| PWS_NAME | Name of the public water system. | Yes | `us_sdwis:pwsName` | Also `rdfs:label` |
| PRIMACY_AGENCY_CODE | Primacy agency code is the two-character state code or EPA Region number. |  |  |  |
| EPA_REGION | A two-character code identifying the EPA Region in which the system is located. |  |  |  |
| SEASON_BEGIN_DATE | Opening month and day of the period of time when the water system serves water for those systems that operate seasonally (DD-MONTH format). | ? |  |  |
| SEASON_END_DATE | Ending month and day of the period of time when the water system serves water for those systems that operate seasonally (DD-MONTH format). | ? |  |  |
| PWS_ACTIVITY_CODE | A single-character code identifying the current activity status of the public water system. A - Active, I - inactive, N - changed from public to non-public, M - merged with another system, P - potential future system to be regulated | Yes | `us_sdwis:hasActivity` | Capture as `xsd:string` |
| PWS_DEACTIVATION_DATE | Date on which the water system was reported as being closed/deactivated (MM/DD/YYYY format). | Yes | `us_sdwis:deactivationDate` | Capture as `xsd:date` |
| PWS_TYPE_CODE | Indicates the type of public water system (PWS). CWS- community water system, TNCWS - transient community water system, NTNCWS - nontransient non-community water system (see [metadata](https://echo.epa.gov/tools/data-downloads/sdwa-download-summary) for defintions) | Yes | `us_sdwis:PublicWaterSystem-<PWS_TYPE_CODE>` | Class |
| DBPR_SCHEDULE_CAT_CODE | Stage 2 Disinfectant Byproducts Rule schedule category code. |  |  |  |
| CDS_ID | Combined distribution system identifier. | ? |  `us_sdwis:CombinedDistributionSystem` | Capture in IRI |
| GW_SW_CODE | Identifies whether a system’s water source is groundwater (GW) or surface water (SW) under SDWA. An empty cell indicates the system relied on another water source. | Yes | `us_sdwis:PublicWaterSystem-<GW_SW_CODE>` | Class |
| LT2_SCHEDULE_CAT_CODE| Single-digit code to identify the category for Long Term 2 Enhanced Surface Water Treatment (LT2) schedule. |  |  |  |
| OWNER_TYPE_CODE | F – Federal government, L - Local government, M- Public/Private, N – Native American, P - Private, S – State government | Yes | `us_sdwis:hasOwnership` | Capture as `xsd:string` |
| POPULATION_SERVED_COUNT | Estimated average daily population served by a system. | Yes | `us_sdwis:populationServed` | Capture as `xsd:int` |
| POP_CAT_2_CODE |  |  |  |  |
| POP_CAT_3_CODE |  |  |  |  |
| POP_CAT_4_CODE |  |  |  |  |
| POP_CAT_5_CODE |  |  |  |  |
| POP_CAT_11_CODE |  |  |  |  |
| PRIMACY_TYPE | Indicates whether the water system is regulated by a state, tribal, or territorial primacy program. Note that EPA direct implementation programs, except for Wyoming, are tribal primacy programs. | ? |  |  |
| PRIMARY_SOURCE_CODE | Primary water source code. GW - Ground water ,GWP - Ground water purchased, SW - Surface water, SWP - Surface water purchased, GU - Groundwater under influence of surface water, GUP – Purchased ground water under influence of surface water source | Yes | `us_sdwis:primarySourceType` | `us_sdwis:PWS-WaterSourceType.<PRIMARY_SOURCE_CODE>` |
| IS_GRANT_ELIGIBLE_IND | Indicates whether the primacy agency has reported the minimum necessary data elements for this water system to include it in grant calculations. |  |  |  |
| IS_WHOLESALER_IND | Indicates whether the system is a wholesaler of water. | ? |  |  |
| IS_SCHOOL_OR_DAYCARE_IND | Indicates if the water system’s primary service area is a school or daycare, as defined by EPA/OGWDW. | ? |  |  |
| SERVICE_CONNECTIONS_COUNT | Number of service connections to the water system. | Yes |  `us_sdwis:serviceConnections` | Capture as `xsd:int` |
| SUBMISSION_STATUS_CODE | Code that indicates whether an active water system was reported, rejected, or not reported during the recent inventory submission. This field is not applicable to inactive water systems. Generated by ODS. Y - Reported and accepted, U - Unreported, R - Reported, but rejected |  |  |  |
| ORG_NAME | The organization to which the legal entity is associated. |  |  |  |
| ADMIN_NAME | Name of the water system administrative contact – usually a person’s name. |  |  |  |
| EMAIL_ADDR | Email address of the administrative contact. |  |  |  |
| PHONE_NUMBER | Telephone number of a water system or the system’s primary contact |  |  |  |
| PHONE_EXT_NUMBER | Telephone extension of the administrative contact. |  |  |  |
| FAX_NUMBER | Administrative contact's fax number. |  |  |  |
| ALT_PHONE_NUMBER | Administrative contact's alternative telephone number. |  |  |  |
| ADDRESS_LINE1 | First line of an address applicable to a legal entity. |  |  |  |
| ADDRESS_LINE2 | Second line of an address applicable to a legal entity. This field is the street address, rural route, etc. |  |  |  |
| CITY_NAME | City in which a legal entity is located. | ? |  |  |
| ZIP_CODE | U.S. Postal Service (USPS) ZIP code in which a legal entity is located. | ? |  |  |
| COUNTRY_CODE | Two-character abbreviation of the country code where the administrative contact is located. |  |  |  |
| FIRST_REPORTED_DATE | First reported date for the system (format  MM/DD/YYYY)| Yes | `us_sdwis:firstReport` | Capture as `xsd:date` |
| LAST_REPORTED_DATE | Last reported date for the system (format MM/DD/YYYY). | Yes | `us_sdwis:lastReport` | Capture as `xsd:date` |
| STATE_CODE | A coded value that represents the U.S. Postal Service (USPS) state abbreviation in which a legal entity is located. Must be one of the USPS Postal State Codes. |  |  |  |
| SOURCE_WATER_PROTECTION_CODE | Indicates whether the water system has implemented source water protection according to state policy. | ? |  |  |
| SOURCE_PROTECTION_BEGIN_DATE | Date water system substantially implemented source water protection according to state policy (MM/DD/YYYY format). | ?  |  |  |
| OUTSTANDING_PERFORMER | Indicates whether the system met the outstanding performer criteria according to state policy. |  |  |  |
| OUTSTANDING_PERFORM_BEGIN_DATE | Date water system met the outstanding performer criteria according to state policy.  |  |  |  |
| REDUCED_RTCR_MONITORING | Frequency of Revised Total Coliform Rule (RTCR) monitoring, which could be annually, quarterly, or semi-annually. |  |  |  |
| REDUCED_MONITORING_BEGIN_DATE | Initial date of reduced monitoring (MM/DD/YYYY format). |  |  |  |
| REDUCED_MONITORING_END_DATE | Reduced monitoring end date (MM/DD/YYYY format) |  |  |  |
| SEASONAL_STARTUP_SYSTEM | Indicates whether the system pressurized including during the offseason or whether the system was not pressurized all year. Only pertains to seasonal systems. |  |  |  |

#### Table: SDWA_SERVICE_AREAS.csv

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| SUBMISSIONYEARQUARTER	|	Fiscal year and quarter of the quarterly snapshot of SDWIS. |  |  |  |
| PWSID	|	Unique identifying code for a public water system in SDWIS. The PWSID consists of a two-letter state or region code, followed by seven digits. |  |  |  |
| SERVICE_AREA_TYPE_CODE |	Service area type code. For a full list of visit codes and their descriptions see SDWA_REF_CODE_VALUES.csv under VALUE_TYPE=SERVICE_AREA_CODE. | Yes | `us_sdwis:serviceAreaType` | Controlled vocabulary |
| IS_PRIMARY_SERVICE_AREA_CODE | Indicates whether the area is the primary service area served by the water system. |  |  |  |
| FIRST_REPORTED_DATE	| First reported date of the service area (format MM/DD/YYYY). |  |  |  |
| LAST_REPORTED_DATE | Last reported date of the service area (format MM/DD/YYYY). |  |  |  |

#### Table: SDWA_REF_CODE_VALUES.csv

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| VALUE_TYPE | Column name associated with the value code as found in the other files. |  |  |  |
| VALUE_CODE | Value associated with the column named in VALUE_TYPE. | Yes | `us_sdwis:PWS-ServiceArea-<VALUE_CODE>` | Look up `SERVICE_AREA_TYPE_CODE` based on 'VALUE_DESCRIPTION` (see below) |
| VALUE_DESCRIPTION | Description of the value in VALUE_CODE. |  |  | `Service_Area_Type` in CWS layer or `SERVICE_AREA_TYPE` in T_NTNC layer of Geopackage |

<!--
#### Table: GEOGRAPHIC_AREA  (one to many with PWSID)

> **code**: *sdwa_geographicArea.py*

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| ansi_entity_code | American National Standards Institute (ANSI) code for the county, city, or legal statistical area. Taken with the ANSI state code, uniquely identifies a county (or other area) within the country. See the U.S. Census Bureau webpage for more information about ANSI codes. |  |  |  |
| area_type_code | Indicates the area type, which is TR (Tribal), CN (County), ZC (Zip Code), CT (City), or IR (Indian Reservation) |  |  |  |
| city_served |  |  |  |  |
| county_served |  |  |  |  |
| epa_region |  |  |  |  |
| geo_id |  |  |  |  |
| primacy_agency_code |  |  |  |  |
| pws_activity_code |  |  |  |  |
| pws_type_code | A system-generated coded value which classifies the water system according to federal requirements. It includes Community Water Systems (CWS), Non-Transient Non-Community Water Systems (NTNCWS), and Transient Non-Community Water Systems (TNCWS). |  |  |  |  |
| pwsid |  |  |  |  |
| state_served |  |  |  |  |
| tribal_code |  |  |  |  |
| zip_code_served |  |  |  |  |

#### Table: SERVICE_AREA.csv (one to many with PWSID)

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| epa_region |  |  |  |  |
| is_primary_service_area_code | Code indicating the type of primary service area served by the water system. |  |  |  |  |
| primacy_agency_code| Two character postal code for the state or territory having regulatory oversight for the water system. If the water system is regulated directly by EPA, this code will consist of the two-digit EPA Region number (01â€¦10). The Navajo Nation has primacy over its water systems, so NN is used in this case. |  |  |  |  |
| pws_activity_code | Code that indicates the activity status of the public water system. |  |  |  |  |
| pws_type_code | A system-generated coded value which classifies the water system according to federal requirements. It includes Community Water Systems (CWS), Non-Transient Non-Community Water Systems (NTNCWS), and Transient Non-Community Water Systems (TNCWS). |  |  |  |  |
| pwsid |  |  |  |  |
| service_area_type_code | Service area type code. (Dispenser, Hotel/Motel, School, Residential Area, etc.) |  |  |  |  |

#### Table: SDWA_FACILITIES.csv

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| SUBMISSIONYEARQUARTER | Fiscal year and quarter of the quarterly snapshot of SDWIS. |  |  |  |
| PWSID | Unique identifying code for a public water system in SDWIS. The PWSID consists of a two-letter state or region code, followed by seven digits. |  |  |  |
| FACILITY_ID | Facility ID that, when used with the PWSID, uniquely identifies a water system facility. |  |  |  |
| FACILITY_NAME | Name of the water system facility. |  |  |  |
| STATE_FACILITY_ID | ID that a state uses to identify in their own state system database. |  |  |  |
| FACILITY_ACTIVITY_CODE | A single-character code identifying the current status of the facility. A - Active, I - Inactive, N - Changed from public to non-public, M - Merged with another system, P - Potential future system to be regulated |  |  |  |
| FACILITY_DEACTIVATION_DATE | Date the facility was deactivated (no longer actively serving water) or removed from federal oversight because it no longer met SDWA criteria as a public water system (MM/DD/YYYY format). |  |  |  |
| FACILITY_TYPE_CODE | Code identifying the type of facility. (see [metadata](https://echo.epa.gov/tools/data-downloads/sdwa-download-summary) for complete list) |  |  |  |
| SUBMISSION_STATUS_CODE | Code that indicates whether an active water system was reported, rejected, or not reported during the recent inventory submission. This field is not applicable to inactive water systems. 
Y - Reported and accepted, U - Unreported, R - Reported, but rejected |  |  |  |
| IS_SOURCE_IND | Indicates whether the water system facility is designated a source (either a Consecutive Connection (CC), Infiltration Gallery (IG), Intake (IN), Non-piped (NP), Roof Catchment (RC), Reservoir (RS), Spring (SP), Well (WL), or Non-piped non-purchased (NN)). |  |  |  |
| WATER_TYPE_CODE | Character code identifying the type of water source. Ground water (GW), Surface water (SW), Ground water under the influence of surface water (GU). See the Water Topics page on the EPA website for full definitions of these terms and more. |  |  |  |
| AVAILABILITY_CODE | A single-character code for how the water source is utilized by a water system. E - Emergency, I - Interim, P - Permanent, O - Other, S - Seasonal, U - Unknown |  |  |  |
| SELLER_TREATMENT_CODE | Code that indicates the treatment status of the water. Applies only to source facilities. F - Filtered, G - Treated by seller including 4-log for the Ground Water Rule, Y - Partially treated by seller, N - Not treated, U - Unknown |  |  |  |
| SELLER_PWSID | PWSID of the water system that is selling water to this system through this interconnection. Is also the "upstream" water system to the parent of this facility. |  |  |  |
| SELLER_PWS_NAME | Name of the water system that is selling water to this system through this interconnection. Is also the "upstream" water system to the parent of this facility. |  |  |  |
| FILTRATION_STATUS_CODE | Code reported by the state to indicate whether a non-emergency surface water source or a non-emergency ground water under the influence of surface water source is required to install filtration by a certain date or is successfully avoiding filtration. MIF - Must install filtration, SAF - Successfully avoiding filtration, FIL - Filtration already in place |  |  |  |
| IS_SOURCE_TREATED_IND | Indicates whether the water system source water is being treated or not. |  |  |  |
| FIRST_REPORTED_DATE | First reported date for the milestone event. The date format is MM/DD/YYYY. |  |  |  |
| LAST_REPORTED_DATE | Last reported date for the milestone event. The date format is MM/DD/YYYY. |  |  |  |
-->

### Water System Boundaries: `Service_Areas_V_3_0.gpkg`

#### Layer: CWS ([metadata](https://epa.maps.arcgis.com/sharing/rest/content/items/e29a5059ab8f400ab9802026aee1b761/data))

`us_sdwis:PublicWaterSystem-CWS` subclass of `us_sdwis:PublicWaterSystem`

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| fid |  |  |  |  |
| Original_Data_Provider | The name of the entity responsible for creating the boundary or the original provider of the boundary. Typical values include: the water system itself; the specific state agency/department/division that provided the data; federal agency/department; or other organization. |  |  |  |
| Data_Provider_Type | The type of entity responsible for creating the boundary or the original source of the boundary (such as, water system itself, state agency, federal agency). |  |  |  |
| Data_Source | Link or URL to the data source for this boundary |  |  |  |
| PWSID | The identifier for individual drinking water system recognized by and used in the Safe Drinking Water Information System (SDWIS). The first two characters of the PWSID typically consist of a two-letter state or EPA region code, followed by seven numeric digits. | Yes | `us_sdwis:pwsId` | Also in IRI |
| PWS_Name | The name of the Public Water System (PWS). | Yes | `us_sdwis:pwsName` |  |
| Primacy_Agency | Primacy agency code is the two-character state code or EPA Region number. | Yes |  | First two characters (state) captured to aid processing |
| Pop_Cat_5 | Values identifying the population size category |  |  |  |
| Population_Served_Count | Estimated average daily population served by a system. |  |  |  |
| Service_Connections_Count | Number of service connections to the water system. |  |  |  |
| Model_Method | The modeling method used for EPA modeled service areas | Yes | `us_sdwis:hasMethod` |  |
| Service_Area_Type | Indicates the type of primary service area served by the water system. Data element reported to the Safe Drinking Water Information System (SDWIS). | Yes | `us_sdwis:serviceAreaType` | Controlled vocabulary |
| Symbology_Field | Field used to symbolize the service areas in the web map |  |  |  |
| Modification_Method | The method used to create the service areas. This is typically the method employed by the EPA to transform system sourced data that is not a service area into a service area. Examples include using water main data and buffering it by 150 meters or buffering lead service line inventories or georeferencing a service area map and drawing the boundary |  |  |  |
| Feature_Type | The original type of data that was used to use or create a service area. Many of the feature types are simply a polygon feature of a service area. Other feature types could be water mains, lead service line inventories, PDF map of a service area |  |  |  |
| Method_Details | Any other relevant details about the service area |  |  |  |
| Verification_Status | Indicates whether the boundary has been verified. |  |  |  |
| Detailed_Facility_Report | URL to EPA ECHO's SDWA violation report for the CWS |  |  |  |
| Confirmed |  |  |  |  |
| PWSID_1 |  |  |  |  |
| Shape_Length |  |  |  |  |
| Shape_Area |  |  |  |  |
| Date_Create | Date the boundary data was initially created or published. |  |  |  |

#### Layer: T_NTNC ([metadata](https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/Transient_and_Non_Transient_Non_Community_Water_System_Service_Areas/FeatureServer/layers))

`us_sdwis:PublicWaterSystem-TNCWS` or `us_sdwis:PublicWaterSystem-NTNCWS` subclass of `us_sdwis:PublicWaterSystem`:

| Attribute | Description | Lift to Graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| fid | OBJECTID |  |  |  |
| PWSID | PWSID |  |  |  |
| PWS_Name | PWS Name | Yes | `us_sdwis:pwsName` |  |
| LOCATION_CONFIDENCE | Location Confidence |  |  |  |
| PRIMACY_AGENCY_CODE | Primacy Agency Code |  |  |  |
| PWS_TYPE_CODE | PWS Type Code |  |  |  |
| POPULATION_SERVED_COUNT | Population Served |  |  |  |
| PRIMARY_SOURCE_CODE | Primary Source Code |  |  |  |
| IS_WHOLESALER_IND | Is Wholesaler Indicator |  |  |  |
| IS_SCHOOL_OR_DAYCARE_IND | Is School or Daycare Indicator |  |  |  |
| SERVICE_CONNECTIONS_COUNT | Service Connections Count |  |  |  |
| parcelnumb | Parcel Number |  |  |  |
| AREAKM | Service Area (km<sup>2</sup>) |  |  |  |
| Service_Area_Type | Service Area Type | Yes | `us_sdwis:serviceAreaType` | Controlled vocabulary |
| Detailed_Facility_Report | Detailed Facility Report |  |  |  |
| Date_Source | Data Source |  |  |  |

<!--
> **code**: *cws_serviceAreas.py*

| Attribute       | Description| Lift to Graph | Ontology | Property |
|-----------------|------------|---------------|----------|----------|
| OBJECTID        | | | | |
| PWSID |  Public water system identifier as assigned by SDWIS.        | Yes | us_sdwis:PublicWaterSystem iri , us_sdwis:PWS-ServiceArea iri, us_sdwis:PWS-ServiceArea.geometry iri||
| State | | used to filter | | |
| PWS_Name        | Name of public water system as reported to SDWIS.  | Yes || |
| Primacy_Agency  | The state or EPA region that holds primacy over the system and handles reporting.| Yes || |
| Pop_Cat_5       | A category variable derived by SDWIS that denotes the number of people served by a system. Possible values are "<=500", "501-3,300", "3,301-10,000","10,000-100,000" and ">100,000". |     || |
| Population_Served_Count   | The reported population that the system serves.    || | |
| Service_Connections_Count | The reported number of service connections in the system.    || | |
| Method| The method used to derive the service area. Possible values include "Census Place", "Decision Tree", "OSM", "Parcel", "Random Forest" and "State".     |
| Service_Area_Type         | The primary type of area served by the system as reported to SDWIS     | Yes | | |
| Symbology_Field | The symbology used for the web application, possible values are "MODELED" and "STATE".     | No  |||
| Original_Data_Provider    | Source of data.      |
| Data_Provider_Type        |  Type of source for original data.       |     ||
| Boundary_Method |  How Original Data was Sourced.|     ||
| Method_Basis    |  How original data was developed.        |
| Method_Details  |  |
| System_Type     | Type of system. The only value here is "Water Service Area"  | No |
| Verification_Status       |  Whether the service area has been verified to be correct.   |
| Verification_Process      |  How verification was performed.         |
| Verifier_Type   | Type of entity that performed verification (ex: Non-Profit, Municipality)        |
| Publisher_Owner |
| Data_Source_Link|
| Secondary_ID    |
| Secondary_ID_Source       |
| Detailed_Facility_Report  | URL to frs registry based on pwsid       |
| Date_Created    |  Date of creation.   |
| Date_Modified   |  Date service area was modified.         |
| Verification_Date         | Date of verification.|
| Shape_Area      |
| Shape_Length    |
-->

### Controlled Vocabulary -

Service_Area_Type_Code

| Service Area Type | Code | IRI |
| --- | --- | --- |
| Daycare Center | DC | `us_sdwis:PWS-ServiceArea-DC` |
| Dispenser | DI | `us_sdwis:PWS-ServiceArea-DI` |
| Homeowners Association | HA | `us_sdwis:PWS-ServiceArea-HA` |
| Hotel/Motel | HM | `us_sdwis:PWS-ServiceArea-HM` |
| Highway Rest Area | HR | `us_sdwis:PWS-ServiceArea-HR` |
| Industrial/Agricultural | IA | `us_sdwis:PWS-ServiceArea-IA` |
| Interstate Carrier | IC | `us_sdwis:PWS-ServiceArea-IC` |
| Institution | IN | `us_sdwis:PWS-ServiceArea-IN` |
| Medical Facility | MF | `us_sdwis:PWS-ServiceArea-MF` |
| Mobile Home Park | MH | `us_sdwis:PWS-ServiceArea-MH` |
| Mobile Home Park - Principal Residence | MP | `us_sdwis:PWS-ServiceArea-MP` |
| Municipality | MU | `us_sdwis:PWS-ServiceArea-MU` |
| Other Area | OA | `us_sdwis:PWS-ServiceArea-OA` |
| Other Non-transient Area | ON | `us_sdwis:PWS-ServiceArea-ON` |
| Other Residential | OR | `us_sdwis:PWS-ServiceArea-OR` |
| Other Transient Area | OT | `us_sdwis:PWS-ServiceArea-OT` |
| Recreation Area | PA | `us_sdwis:PWS-ServiceArea-PA` |
| Residential Area | RA | `us_sdwis:PWS-ServiceArea-RA` |
| Retail Employees | RE | `us_sdwis:PWS-ServiceArea-RE` |
| Restaurant | RS | `us_sdwis:PWS-ServiceArea-RS` |
| School | SC | `us_sdwis:PWS-ServiceArea-SC` |
| Sanitary Improvement District | SI | `us_sdwis:PWS-ServiceArea-SI` |
| Summer Camp | SK | `us_sdwis:PWS-ServiceArea-SK` |
| Secondary Residences | SR | `us_sdwis:PWS-ServiceArea-SR` |
| Service Station | SS | `us_sdwis:PWS-ServiceArea-SS` |
| Subdivision | SU | `us_sdwis:PWS-ServiceArea-SU` |
| Water Bottler | WB | `us_sdwis:PWS-ServiceArea-WB` |
| Wholesaler of Water | WH | `us_sdwis:PWS-ServiceArea-WH` |


Facility_Type_Code

* CC - Consecutive Connection
* CH - Common Headers
* CS - Cistern
* CW - Clear Well
* DS - Distribution System System/Zone
* IG - Infiltration Gallery
* IN - Intake
* NN - Non-piped, Non-purchased
* NP - Non-piped
* OT - Other
* PC - Pressure Control
* PF - Pump Facility
* RC - Roof Catchment
* RS - Reservoir
* SI - Surface Impoundment
* SP - Spring
* SS - Sampling Station
* ST - Storage
* TM - Transmission Main (Manifold)
* TP - Treatment Plant
* WH - Wellhead
* WL - Well
