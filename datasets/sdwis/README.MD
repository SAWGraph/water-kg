#

## Overview of the raw dataset

* **Name of dataset:** Safe Drinking Water Information System SDWIS
* **Source Agency:** EPA
* **Data source location:**
  * [Drinking Water State | EPA Pfas analytic tools downloads](https://echo.epa.gov/trends/pfas-tools#data)
  * [SDWA Dataset | ECHO data downloads](https://echo.epa.gov/tools/data-downloads)
  * [Water System Boundaries](https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/Water_System_Boundaries/FeatureServer)
* **Additional data sources:**
  * [SDWIS Federal Reports Search](https://sdwis.epa.gov/ords/sfdw_pub/r/sfdw/sdwis_fed_reports_public/200)

* **Metadata description:**
  * [Envirofacts model](https://enviro.epa.gov/envirofacts/metadata/model/sdwis)
  * [SDWA download summary](https://echo.epa.gov/tools/data-downloads/sdwa-download-summary#sdwis)

  * [Community Water System Service Area Boundaries](https://www.epa.gov/ground-water-and-drinking-water/community-water-system-service-area-boundaries?tab=map) , [Water System Boundaries](https://epa.maps.arcgis.com/home/item.html?id=80c6912ef14f46e480f5afd807767b4b), [ORB_SAB_Model Github](https://github.com/USEPA/ORD_SAB_Model)
* **Format of data returned:** XLSX, CSV, (API available with json but has less tables), esri rest service (CWS boundaries)
* **General Comments:**

## Schema Diagram

[draft](https://lucid.app/lucidchart/16e658ef-6f61-4ce3-a770-0c410ecb194a/edit?viewport_loc=2887%2C55%2C2505%2C1076%2CO.sGt549hds0&invitationId=inv_ea094a2c-59da-4347-b175-700b91e5623d)

## Code

## Raw Data Attribute List and Ontology Mappings

### Drinking Water State Download from PFAS Analytic Tools

code: drinkingWater_state.py

| Attribute| Description | Lift to Graph | Ontology | Property |
|---------|-------------|------------|-------|--------|
| PWSID    | Uniquely identifies the water system within a specific state.Format: SSXXXXXXXXXX where: SS = the Federal Information Processing Standard (FIPS) Pub 5-2 State abbreviation in which the water system is located, or the region number of the EPA region responsible for an Indian reser vation, and XXXXXXXXXX = the water system identification code assigned by the State. | YES         | |us_sdwis:PublicWaterSystem us_sdwis:pwsId and in URI|
| PWS Name | The name of the water system. The name can be the formal, legal, or common name that is used most generally in referring to the water system. When multiple facilities exist for the water system at different physical locations, the name identifies the means by which the system, as a whole, is generally known.       | YES         | us_sdwis | us_sdwis:PublicWaterSystem us_sdwis:pwsName xsd:string |
| State    |       |   |||
| Region   |       |   |||
| County   |       |   |||
| Tribal Name        |       | ?  |||
| Population Served  | A system-generated count of the total retail population served by a water system.     | YES         | us_sdwis| us_sdwis:PublicWaterSystem us_sdwis:populationServed xsd:Int |
| Size     | Five main water system size categories, based on retail population served. Very small <=500, Small 501-3,300, Medium 3,301-10,000, Large 10,001-100,000, Very Large >100,000.   | YES         || us_sdwis:PublicWaterSystem us_sdwis:sizeCategory xsd:string|
| Cities Served      |       | Use from API instead  |||
| Zip Codes Served   |       | Use from API instead  |||
| Sample ID|       | Yes         || us_sdwis:PWS-SamplePoint iri and us_sdwis:PWS-SamplePoint us_sdwis:samplePointId xsd:string|
| Sample Point ID    |       | Yes         ||us_sdwis:SamplePoint us_sdwis:samplePointID xsd:string|
| Code     | Contaminant Code| Yes         ||us_sdwis:PWS-PFAS iri|
| Contaminant        |       | pull from code lookup |||
| Method   | Text field of method - needs cleaning         | TODO         |||
| Detected |       | ?         |||
| Concentration      |       | Yes         ||qudt:QuantityValue qudt:numericValue xsd:float|
| Units    |       | Yes         || qudt:QuantityValue qudt:unit qudt:Unit (mapped to) |
| Concentration (ng/l)         |       | ?        |||
| Reporting Level    |       | TODO        |||
| Health Advisory Level (ng/L) |       | ? |||
| Sample Date        |       | Yes         || us_sdwis:PWS-Observation coso:sampleTime xsd:Date|
| Compliance Period Begin Date |       |   |||
| Compliance Period End Date   |       |   |||
| Sample Type        |       | ?         |||
| MRL/MDL  | Categorical MRL or MDL    | TODO         |||
| Reporting| Automated/Manual|   |||
| Comment  |       |   |||
| Most Recent Sample | Yes/No|   |||
| Results  | Count of results?         |   |||

### SDWIS download tables

#### Table: SDWA_PUB_WATER_SYSTEMS

code: sdwa_pws.py

| Attribute  | Description    | Lift to Graph | Ontology | Property |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|----------|----------|
| SUBMISSIONYEARQUARTER|      | ?   |||
| PWSID      | Unique identifying code for a public water system in SDWIS. The PWSID consists of a two-letter state or region code, followed by seven digits.   | YES | us_sdwis | us_sdwis:PublicWaterSystem us_sdwis:pwsId and in URI |
| PWS_NAME   |      | YES | | us_sdwis:PublicWaterSystem us_sdwis:pwsName|
| PRIMACY_AGENCY_CODE  | Primacy agency code is the two-character state code or EPA Region number.  |     |||
| EPA_REGION |      |     |||
| SEASON_BEGIN_DATE    | Opening month and day of the period of time when the water system serves water for those systems that operate seasonally (DD-MONTH format).      | ? | | |
| SEASON_END_DATE      | Ending month and day of the period of time when the water system serves water for those systems that operate seasonally (DD-MONTH format).       | ? || |
| PWS_ACTIVITY_CODE    | A single-character code identifying the current activity status of the public water system. A - Active, I- inactive, N- changed from public to non-public, M - merged with another system, P- potential future system to be regulated      | YES | | us_sdwis:PublicWaterSupply us_sdwis:hasActivity xsd:string
| PWS_DEACTIVATION_DATE| Date on which the water system was reported as being closed/deactivated (MM/DD/YYYY format).   | yes || us_sdwis:PublicWaterSystem us_sdwis:deactivationDate xsd:Date|
| PWS_TYPE_CODE        | Indicates the type of public water system (PWS). CWS- community water system, TNCWS - transient community water system, NTNCWS - nontransient non-community water system (see metadata for defintions)       | Yes || us_sdwis:PublicWaterSystem rdf:type (subclass of us_sdwis:PublicWaterSystem) |
| DBPR_SCHEDULE_CAT_CODE         | Stage 2 Disinfectant Byproducts Rule schedule category code.     |     |||
| CDS_ID     | Combined distribution system identifier.     | Yes |  |us_sdwis:CombinedDistributionSystem (in URI)|
| GW_SW_CODE | Identifies whether a system’s water source is groundwater (GW) or surface water (SW) under SDWA. An empty cell indicates the system relied on another water source.  | Yes |||
| LT2_SCHEDULE_CAT_CODE| Single-digit code to identify the category for Long Term 2 Enhanced Surface Water Treatment (LT2) schedule.        |     |||
| OWNER_TYPE_CODE      | F – Federal government, L- Local government, M- Public/Private, N – Native American, P - Private, S – State government       | Yes |||
| POPULATION_SERVED_COUNT        | Estimated average daily population served by a system. | YES |||
| POP_CAT_2_CODE       |      |     |||
| POP_CAT_3_CODE       |      |     |||
| POP_CAT_4_CODE       |      |     |||
| POP_CAT_5_CODE       |      |     |||
| POP_CAT_11_CODE      |      |     |||
| PRIMACY_TYPE         | Indicates whether the water system is regulated by a state, tribal, or territorial primacy program. Note that EPA direct implementation programs, except for Wyoming, are tribal primacy programs. | ?   |||
| PRIMARY_SOURCE_CODE  | Primary water source code. GW - Ground water ,GWP - Ground water purchased, SW - Surface water, SWP - Surface water purchased, GU - Groundwater under influence of surface water, GUP – Purchased ground water under influence of surface water source         | Yes | | us_sdwis:PublicWaterSystem us_sdwis:primarySource xsd:string|
| IS_GRANT_ELIGIBLE_IND|      |     |||
| IS_WHOLESALER_IND    |      | ?   |||
| IS_SCHOOL_OR_DAYCARE_IND       |      | ?   |||
| SERVICE_CONNECTIONS_COUNT      | Number of service connections to the water system.     | Yes || us_sdwis:PublicWaterSystem us_sdwis:serviceConnections xsd:Int|
| SUBMISSION_STATUS_CODE         | Code that indicates whether an active water system was reported, rejected, or not reported during the recent inventory submission. This field is not applicable to inactive water systems. Generated by ODS. Y - Reported and accepted, U - Unreported, R - Reported, but rejected |     |||
| ORG_NAME   | The organization to which the legal entity is associated.        |     |||
| ADMIN_NAME | Name of the water system administrative contact – usually a person’s name. |     |||
| EMAIL_ADDR | Email address of the administrative contact. |     |||
| PHONE_NUMBER         | Telephone number of a water system or the system’s primary contact         |     |||
| PHONE_EXT_NUMBER     | Telephone extension of the administrative contact.     |     |||
| FAX_NUMBER | Administrative contact's fax number.         |     |||
| ALT_PHONE_NUMBER     | Administrative contact's alternative telephone number. |     |||
| ADDRESS_LINE1        | First line of an address applicable to a legal entity. |     |||
| ADDRESS_LINE2        | Second line of an address applicable to a legal entity. This field is the street address, rural route, etc.        |     |||
| CITY_NAME  | City in which a legal entity is located.     |  ?   |||
| ZIP_CODE   | U.S. Postal Service (USPS) ZIP code in which a legal entity is located.    |   ?  |||
| COUNTRY_CODE         |      |     |||
| FIRST_REPORTED_DATE  | First reported date for the system (format  MM/DD/YYYY)| YES ||us_sdwis:firstReport xsd:Date|
| LAST_REPORTED_DATE   | Last reported date for the system (format MM/DD/YYYY). | YES || us_sdwis:lastReport xsd:Date|
| STATE_CODE | A coded value that represents the U.S. Postal Service (USPS) state abbreviation in which a legal entity is located. Must be one of the USPS Postal State Codes.      |     |||
| SOURCE_WATER_PROTECTION_CODE   | Indicates whether the water system has implemented source water protection according to state policy.    | ?   |||
| SOURCE_PROTECTION_BEGIN_DATE   | Date water system substantially implemented source water protection according to state policy (MM/DD/YYYY format). |     |?||
| OUTSTANDING_PERFORMER| Indicates whether the system met the outstanding performer criteria according to state policy. |     |||
| OUTSTANDING_PERFORM_BEGIN_DATE | Date water system met the outstanding performer criteria according to state policy.  |     |||
| REDUCED_RTCR_MONITORING        | Frequency of Revised Total Coliform Rule (RTCR) monitoring, which could be annually, quarterly, or semi-annually.  |     |||
| REDUCED_MONITORING_BEGIN_DATE  | Initial date of reduced monitoring (MM/DD/YYYY format).|     |||
| REDUCED_MONITORING_END_DATE    | Reduced monitoring end date (MM/DD/YYYY format)        |     |||
| SEASONAL_STARTUP_SYSTEM        | Indicates whether the system pressurized including during the offseason or whether the system was not pressurized all year. Only pertains to seasonal systems.       |     |||

#### Table: geographic_area  (one to many with PWSID)

code:sdwa_geographicArea.py

| Attribute | Description | Lift to Graph | Ontology | Property |
|---------------------|-------------|---------------|----------|----------|
| ansi_entity_code    | American National Standards Institute (ANSI) code for the county, city, or legal statistical area. Taken with the ANSI state code, uniquely identifies a county (or other area) within the country. See the U.S. Census Bureau webpage for more information about ANSI codes.  |     |||
| area_type_code      | Indicates the area type, which is TR (Tribal), CN (County), ZC (Zip Code), CT (City), or IR (Indian Reservation)  |     |||
| city_served         |   |     |||
| county_served       |   |     |||
| epa_region|   |     |||
| geo_id    |   |     |||
| primacy_agency_code |   |     |||
| pws_activity_code   |   |     |||
| pws_type_code       | A system-generated coded value which classifies the water system according to federal requirements. It includes Community Water Systems (CWS), Non-Transient Non-Community Water Systems (NTNCWS), and Transient Non-Community Water Systems (TNCWS).  |     |||
| pwsid     |   |     |||
| state_served        |   |     |||
| tribal_code         |   |     |||
| zip_code_served     |   |     |||

#### Table: service_area (one to many with PWSID)

| Attribute| Description   | Lift to Graph | Ontology | Property |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|----------|----------|
| epa_region         |     |     |||
| is_primary_service_area_code | Code indicating the type of primary service area served by the water system.        |     |||
| primacy_agency_code| Two character postal code for the state or territory having regulatory oversight for the water system. If the water system is regulated directly by EPA, this code will consist of the two-digit EPA Region number (01â€¦10). The Navajo Nation has primacy over its water systems, so NN is used in this case. |     |||
| pws_activity_code  | Code that indicates the activity status of the public water system.       |     |||
| pws_type_code      | A system-generated coded value which classifies the water system according to federal requirements. It includes Community Water Systems (CWS), Non-Transient Non-Community Water Systems (NTNCWS), and Transient Non-Community Water Systems (TNCWS).         |     |||
| pwsid    |     |     |||
| service_area_type_code       | Service area type code. (Dispenser, Hotel/Motel, School, Residential Area, etc.)    |     |||
||     |     |||

#### Table: sdwa_facilities.csv

| Attribute        | Description        | Lift to Graph | Ontology | Property |
|----------------------------|----------------------------------------|---------------|----------|----------|
| SUBMISSIONYEARQUARTER      ||     |||
| PWSID  ||     |||
| FACILITY_ID      ||     |||
| FACILITY_NAME    ||     |||
| STATE_FACILITY_ID||     |||
| FACILITY_ACTIVITY_CODE     ||     |||
| FACILITY_DEACTIVATION_DATE ||     |||
| FACILITY_TYPE_CODE         | Code identifying the type of facility. |     |||
| SUBMISSION_STATUS_CODE     ||     |||
| IS_SOURCE_IND    ||     |||
| WATER_TYPE_CODE  ||     |||
| AVAILABILITY_CODE||     |||
| SELLER_TREATMENT_CODE      ||     |||
| SELLER_PWSID     ||     |||
| SELLER_PWS_NAME  ||     |||
| FILTRATION_STATUS_CODE     ||     |||
| IS_SOURCE_TREATED_IND      ||     |||
| FIRST_REPORTED_DATE        ||     |||
| LAST_REPORTED_DATE         ||     |||

### Water System Boundaries

code: cws_serviceAreas.py

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

### Controlled Vocabulary -

Facility_type_Code

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
