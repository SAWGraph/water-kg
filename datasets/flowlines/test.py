# %%
from pathlib import Path
import geopandas as gpd
import shapely

cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent
data_dir = cwd.parent / "data"
ttl_dir = cwd / "ttl_files"
log_dir = cwd / "logs"

# %%
# Read in the geopackage files; these can be downloaded from
# https://www.sciencebase.gov/catalog/item/61295190d34e40dd9c06bcd7
catchments = gpd.read_file(data_dir / f'Hydrofabric/reference_catchments.gpkg')
flowlines = gpd.read_file(data_dir / f'Hydrofabric/reference_flowline.gpkg')

# %%
# Project catchments to the same coordinate system
catchments = catchments.to_crs("epsg:4326")
assert catchments.crs == "epsg:4326", catchments.crs
flowlines = flowlines.to_crs("epsg:4326")
assert flowlines.crs == "epsg:4326", flowlines.crs

# %%
# First we get the featureid for the catchment. This is a catchment id aka COMID
pointOnColoradoRiver = shapely.geometry.Point(-108.50231860661755, 39.05108882481538)
associatedCatchment = catchments[catchments.intersects(pointOnColoradoRiver)]
featureID = associatedCatchment["featureid"].iloc[0]
assert featureID == 3185828

# %%
# Next we get the associated flowline(s) for the catchment
relevantFlowline = flowlines[flowlines["COMID"] == featureID]
assert relevantFlowline.shape[0] == 1
assert relevantFlowline["gnis_name"].iloc[0] == "Colorado River"
assert relevantFlowline["gnis_id"].iloc[0] == 45730

# All lines with the same LevelPathI form one continuous routed path (e.g., the entire main stem of a river);
# There is also a column for TerminalPath but that represents the ultimate destination of the flowline
# and thus could be very far away from the catchment
MAINSTEM_COLUMN = "LevelPathI"
mainstemID = relevantFlowline[MAINSTEM_COLUMN].iloc[0]
assert mainstemID == 308280

# %%
# Finally we use the id of the terminal path to find the associated geoconnex mainstem
mainstem_lookup = gpd.read_file(
    "https://github.com/internetofwater/ref_rivers/releases/download/v2.1/mainstem_lookup.csv"
)
# The mainstem lookup CSV uses strings instead of integers so we cast
mainstem_lookup["lp_mainstem"] = mainstem_lookup["lp_mainstem"].astype(int)
mainstem_lookup["ref_mainstem_id"] = mainstem_lookup["ref_mainstem_id"].astype(int)

geoconnex_mainstem_id = mainstem_lookup.loc[
    mainstem_lookup["lp_mainstem"] == mainstemID
]["ref_mainstem_id"].iloc[0]

assert geoconnex_mainstem_id == 29559

# The point POINT (-108.50231860661755 39.05108882481538) is associated with the mainstem https://reference.geoconnex.us/collections/mainstems/items/29559
print(
    f"The point {pointOnColoradoRiver} is associated with the mainstem https://reference.geoconnex.us/collections/mainstems/items/{geoconnex_mainstem_id}"
)


wkt_line = "LINESTRING (-70.48113386770586 45.14002192993371, -70.48061640103998 45.1396795299342, -70.47941866770856 45.138286196603076, -70.47789846771087 45.13709892993825, -70.47734920104506 45.13693939660516, -70.47644506771314 45.13710019660488)"
# %%
# First we get the featureid for the catchment. This is a catchment id aka COMID
flowlinevpu01 = shapely.wkt.loads(wkt_line)
associatedCatchment = catchments[catchments.intersects(flowlinevpu01)]
featureID = associatedCatchment["featureid"].iloc[0]
# assert featureID == 3185828

# %%
# Next we get the associated flowline(s) for the catchment
relevantFlowline = flowlines[flowlines["COMID"] == featureID]
# assert relevantFlowline.shape[0] == 1
# assert relevantFlowline["gnis_name"].iloc[0] == "Colorado River"
# assert relevantFlowline["gnis_id"].iloc[0] == 45730

# All lines with the same LevelPathI form one continuous routed path (e.g., the entire main stem of a river);
# There is also a column for TerminalPath but that represents the ultimate destination of the flowline
# and thus could be very far away from the catchment
MAINSTEM_COLUMN = "LevelPathI"
mainstemID = relevantFlowline[MAINSTEM_COLUMN].iloc[0]
# assert mainstemID == 308280

# %%
# Finally we use the id of the terminal path to find the associated geoconnex mainstem
mainstem_lookup = gpd.read_file(
    "https://github.com/internetofwater/ref_rivers/releases/download/v2.1/mainstem_lookup.csv"
)
# The mainstem lookup CSV uses strings instead of integers so we cast
mainstem_lookup["lp_mainstem"] = mainstem_lookup["lp_mainstem"].astype(int)
mainstem_lookup["ref_mainstem_id"] = mainstem_lookup["ref_mainstem_id"].astype(int)

geoconnex_mainstem_id = mainstem_lookup.loc[
    mainstem_lookup["lp_mainstem"] == mainstemID
]["ref_mainstem_id"].iloc[0]

# assert geoconnex_mainstem_id == 29559

# The point POINT (-108.50231860661755 39.05108882481538) is associated with the mainstem https://reference.geoconnex.us/collections/mainstems/items/29559
print(
    f"The point {flowlinevpu01} is associated with the mainstem https://reference.geoconnex.us/collections/mainstems/items/{geoconnex_mainstem_id}"
)