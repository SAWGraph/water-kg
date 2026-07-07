# Colorado Wells - Colorado Division of Water Resources (CDWR)

## Dataset Overview
| Dataset Attribute | Description |
| --- | --- |
| **Name of dataset:** | Well Applications |
| **Source Agency:** | [Colorado Division of Water Resources](https://dwr.colorado.gov/) |
| **Data Source Location:** | [GIS Data By Category](https://cdss.colorado.gov/gis-data/gis-data-by-category)  (see *Well Applications* under *HydroBase Point Data*) <br/> see also [DWR Well Application Permit](https://data.colorado.gov/Water/DWR-Well-Application-Permit/wumm-7awb/data_preview) |
| **Metadata description:** | [DWR Well Application Permit](https://data.colorado.gov/Water/DWR-Well-Application-Permit/wumm-7awb/about_data) |
| **Format:** | ShapeFile |
| **Data update interval** | last updated on July 7, 2026 |
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
| MoreInfo | Hyperlink to more information about the Well Application/Permit | Yes | `co_dwr:moreInfo` | Possibly use as IRI? |
| Receipt | Permit application receipt number | Yes | `rdfs:label` | Used in well IRI |
| Permit | Concatenation of permit number, suffix code, and replacement code |  |  |  |
| WDID | DWR unique structure identifier |  |  | Non-zero for 80366 of 658270 rows |
| CurrStatus | Indicates the current application or physical status of the application/well permit based on entered information | Yes | `co_dwr:hasStatus` | Controlled vocabulary |
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
| Use1 | Decreed use associated with the Well | Yes | `co_dwr:hasWaterUse` | Controlled vocabulary |
| Use2 | Decreed use associated with the Well | ? |  |  |
| SpecialUse |  | ? |  |  |
| Aquifer1 | Aquifer associated with the Well | Yes | `co_dwr:drawsFromAquifer` | Controlled vocabulary |
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
| WellDepth | Completed depth of Well (ft) | Yes | `co_dwr:hasDepth` |  |
| TopPerfCas | Depth from surface to top of perforated casing (feet) | ? |  |  |
| BotPerfCas | Depth from surface to bottom of perforated casing (feet) | ? |  |  |
| Yield | Yield in gallons per minute | Yes | `co_dwr:hasYield` |  |
| StaticWL | Static Water Level | ? |  |  |
| ApplicantN |  |  |  |  |
| CompleteWe |  |  |  |  |
| OGCC_API |  |  |  |  |
| OGJobBatch |  |  |  |  |
| DispUTMX |  |  |  |  |
| DispUTMY |  |  |  |  |
