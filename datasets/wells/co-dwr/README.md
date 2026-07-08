# Colorado Wells - Colorado Division of Water Resources (CDWR)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Well Applications |
| **Source Agency:** | [Colorado Division of Water Resources](https://dwr.colorado.gov/) |
| **Data Source Location:** | [GIS Data By Category](https://cdss.colorado.gov/gis-data/gis-data-by-category)  (see *Well Applications* under *HydroBase Point Data*) <br/> see also [DWR Well Application Permit](https://data.colorado.gov/Water/DWR-Well-Application-Permit/wumm-7awb/data_preview) |
| **Metadata description:** | [DWR Well Application Permit](https://data.colorado.gov/Water/DWR-Well-Application-Permit/wumm-7awb/about_data) |
| **Format:** | ShapeFile |
| **Data update interval** | updated daily (?) |
| **Location of triples:** |  |

## Schema Diagram (TO ADD)
- [*Draft* schema]()

**Legend description:** (TO ADD)
- 

## Code (TO ADD)
- co-wells.py
- [Code Directory]()
- [GDrive Output Directory]()

## IRIs
| Instance Class | IRI Format |
| --- | --- |
| `co_dwr:CDWR_Well` | `co_dwr_data:d.CWDR_Well.<Receipt>` |
| `geo:Geometry` | `co_cdwr_data:d.CDWR_Well.<Receipt>.geometry` |

## Raw Data Attribute List and Mapping with Ontology Concepts
| CDWR Well | Description | Lift to graph | Ontology Property | Comments |
| --- | --- | --- | --- | --- |
| MoreInfo | Hyperlink to more information about the Well Application/Permit | Yes | `rdfs:seeAlso` | Possibly use as IRI? |
| Receipt | Permit application receipt number | Yes | `rdfs:label` | Used in well IRI |
| Permit | Concatenation of permit number, suffix code, and replacement code |  |  |  |
| WDID | DWR unique structure identifier |  |  | Non-zero for 80366 of 658270 rows |
| CurrStatus | Indicates the current application or physical status of the application/well permit based on entered information | Yes | `hyfo:hasWellStatus` | Controlled vocabulary |
| WellName |  |  |  | 0 for every row |
| CaseNo | Water court case number(s) associated with water right |  |  |  |
| Div | DWR Water Division | ? |  |  |
| WD | DWR Water District | ? |  |  |
| County | County where the Well is located | ? |  |  |
| MgmtDist | Thirteen local districts, within the Designated Basins, with additional administrative authority | ? |  |  |
| DesigBasin | Designated basin where Well is located | ? |  |  |
| SubdivName |  |  |  |  |
| Filing |  |  |  |  |
| Lot |  |  |  |  |
| Block |  |  |  |  |
| CtyParclID |  |  |  |  |
| ParcelSize |  |  |  |  |
| PM | Principal Meridian |  |  |  |
| Township | Legal location - Township number and direction |  |  |  |
| Range | Legal location - range |  |  |  |
| Section | Legal location - section number |  |  |  |
| Q160 | Legal location - 160 acre quarter section |  |  |  |
| Q40 | Legal location - 40 acre quarter section |  |  |  |
| Q10 | Legal location - 10 acre quarter section |  |  |  |
| CoordsEW | Distance from East/West section line (feet) |  |  |  |
| CoordsWEdi | Direction of measurement from East/West section line |  |  |  |
| CoordsNS | Distance from North/South section line (feet) |  |  |  |
| CoordsNSdi | Direction of measurement from North/South section line |  |  |  |
| UTMX | The x (Easting) component of the Universal Transverse Mercator system. (Zone 12, NAD83 datum) |  |  |  |
| UTMY | The y (Northing) component of the Universal Transverse Mercator system. (Zone 12, NAD83 datum) |  |  |  |
| LocAccurac | Accuracy of location coordinates | Yes | `co_dwr:locAccuracy` | Controlled vocabulary |
| LatDecDeg | Latitude (decimal degrees) |  |  |  |
| LongDecDeg | Longitude (decimal degrees) |  |  |  |
| Use1 | Decreed use associated with the Well | Yes | `hyfo:hasWaterUse` | Controlled vocabulary |
| Use2 | Decreed use associated with the Well | ? |  |  |
| SpecialUse |  | ? |  |  |
| Aquifer1 | Aquifer associated with the Well | Yes | `co_dwr:hasAquifer` | Controlled vocabulary |
| Aquifer2 | Aquifer associated with the Well | ? |  |  |
| PermitArea |  |  |  |  |
| PermitUnit |  |  |  |  |
| AnnAppropr |  |  |  |  |
| PermIssued | Date Well permit was issued | ? |  |  |
| PermExpire | Date the Well permit will expire if not constructed | ? |  |  |
| WellConstr | Date the Well was constructed or DWR was notified of the construction | ? |  |  |
| FirstBenef | Date of first beneficial use or DWR was notified of first beneficial use | ? |  |  |
| PumpInstal | Date the pump was installed or DWR was notified of the installation | ? |  |  |
| WellPlugge | Date the Well was plugged and abandoned or DWR was notified | ? |  |  |
| Comment |  |  |  |  |
| Elev | Surface elevation at the location of the Well (feet above mean sea level) | ? |  |  |
| WellDepth | Completed depth of Well (ft) | Yes | `hyfo:hasTotalDepth` |  |
| TopPerfCas | Depth from surface to top of perforated casing (feet) | ? |  |  |
| BotPerfCas | Depth from surface to bottom of perforated casing (feet) | ? |  |  |
| Yield | Yield in gallons per minute | Yes | `hyfo:hasYield` |  |
| StaticWL | Static Water Level | Yes | `hyfo:hasStaticWaterDepth` |  |
| ApplicantN |  |  |  |  |
| CompleteWe |  |  |  |  |
| OGCC_API |  |  |  |  |
| OGJobBatch |  |  |  |  |
| DispUTMX |  |  |  |  |
| DispUTMY |  |  |  |  |

## Controlled Vocabularies
**List 1. CurrStatus (Current Status)**
| CurrStatus | Count | Class |
| --- | ---: | --- |
| Additional Fee Required | 4 | `co_dwr:CODWR-WellStatus.AdditionalFeeRequired` |
| Application Denied | 14688 | `co_dwr:CODWR-WellStatus.ApplicationDenied` |
| Application Hold | 88 | `co_dwr:CODWR-WellStatus.ApplicationHold` |
| Application Information Requested | 13901 | `co_dwr:CODWR-WellStatus.ApplicationInformationRequested` |
| Application Received | 4832 | `co_dwr:CODWR-WellStatus.ApplicationReceived` |
| Application Withdrawn | 3418 | `co_dwr:CODWR-WellStatus.ApplicationWithdrawn` |
| Dry Hole Abandoned | 25 | `co_dwr:CODWR-WellStatus.DryHoleAbandoned` |
| Dry Hole Constructed | 2 | `co_dwr:CODWR-WellStatus.DryHoleConstructed` |
| Final Permit | 6278 | `co_dwr:CODWR-WellStatus.FinalPermit` |
| Final Permit - Replacement Permit Issued | 124 |`co_dwr:CODWR-WellStatus.FinalPermit.ReplacementPermitIssued`  |
| Final Permit - Well Deepened | 18 | `co_dwr:CODWR-WellStatus.FinalPermit.WellDeepened` |
| Final Permit - Well Replaced | 319 | `co_dwr:CODWR-WellStatus.FinalPermit.WellReplaced` |
| Final Permit - Well Replaced, Abandonment Required | 355 | `co_dwr:CODWR-WellStatus.FinalPermit.WellReplacedAbandonmentRequired` |
| Final Permit Canceled | 221 | `co_dwr:CODWR-WellStatus.FinalPermitCanceled` |
| Hydrogeology Review Requested | 11 | `co_dwr:CODWR-WellStatus.HydrologyReviewRequiested` |
| NA | 9564 | `co_dwr:CODWR-WellStatus.NA` |
| Permit Canceled | 23471 | `co_dwr:CODWR-WellStatus.PermitCanceled` |
| Permit Expired | 100479 | `co_dwr:CODWR-WellStatus.PermitExpired` |
| Permit Expired (Pump Installed) | 2024 | `co_dwr:CODWR-WellStatus.PermitExpiredPumpInstalled` |
| Permit Extended | 1027 | `co_dwr:CODWR-WellStatus.PermitExtended` |
| Permit Issued | 25877 | `co_dwr:CODWR-WellStatus.PermitIssued` |
| Post Construction Review Requested | 23 | `co_dwr:CODWR-WellStatus.PostConstructionReviewRequested` |
| Pump Installed in Well Without a Permit | 1128 | `co_dwr:CODWR-WellStatus.PumpInstalledWithoutPermit` |
| Pump Installed, No Construction Info Received | 2281 | `co_dwr:CODWR-WellStatus.PumpInstalledNoConstructionInfo` |
| See Associated Receipts | 520 | `co_dwr:CODWR-WellStatus.SeeAssociatedReceipts` |
| Well Abandoned | 43841 | `co_dwr:CODWR-WellStatus.WellAbandoned` |
| Well Constructed | 373139 | `co_dwr:CODWR-WellStatus.WellConstructed` |
| Well Constructed - Replacement Permit Issued | 975 | `co_dwr:CODWR-WellStatus.WellConstructed.ReplacementPermitIssued` |
| Well Replaced - Abandonment Required | 17007 | `co_dwr:CODWR-WellStatus.WellReplaced.AbandonementRequired` |
| `<NULL>` | 2460 |  |

**List 2. LocAccurac (Location Accuracy)**
| LocAccurac | Count | Class |
| --- | ---: | --- |
| Digitized | 544 | `co_dwr:CODWR-LocAccuracy.Digitized` |
| GPS | 15545 | `co_dwr:CODWR-LocAccuracy.GPS` |
| Per Decree | 15 | `co_dwr:CODWR-LocAccuracy.PerDecree` |
| Spotted from quarters | 131584 | `co_dwr:CODWR-LocAccuracy.SpottedFromQuarters` |
| Spotted from section lines | 361288 | `co_dwr:CODWR-LocAccuracy.SpottedFromSectionLines` |
| Surveyed | 2 | `co_dwr:CODWR-LocAccuracy.Surveyed` |
| Unable to spot | 766 | `co_dwr:CODWR-LocAccuracy.UnableToSpot` |
| User Supplied | 140235 | `co_dwr:CODWR-LocAccuracy.UserSupplied` |
| `<NULL>` | 8291 |  |
