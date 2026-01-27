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
hydrofabric_catchments_file = data_dir / f'Hydrofabric/reference_catchments.gpkg'
hydrofabric_flowline_file = data_dir / f'Hydrofabric/reference_flowline.gpkg'
print(f'Reading {hydrofabric_catchments_file}.')
catchments = gpd.read_file(hydrofabric_catchments_file)
print(f'Reading {hydrofabric_flowline_file}.')
flowlines = gpd.read_file(hydrofabric_flowline_file)

### HUCxx VPU ###
vpunum = '01'
# Valid codes: 01, 02, 03N, 03S, 03W, 04, 05, 06, 07, 08, 09, 10U, 10L, 11, 12, 13, 14, 15, 16, 17, 18, 20

vpu_flowline_file = data_dir / f'NHDFlowline/HUC{vpunum}_NHDFlowline.shp'
print(f'Reading and processing HUC {vpunum} flowlines.')
gdf = gpd.read_file(vpu_flowline_file)
gdf.drop(['FDATE',
          'GNIS_ID',
          'WBAREACOMI',
          'SHAPE_LENG',
          'ENABLED',
          'GNIS_NBR'],
          axis=1,
          inplace=True)
gdf = gdf[gdf.FTYPE != 'Coastline']
gdf[['COMID', 'REACHCODE']] = gdf[['COMID', 'REACHCODE']].astype(str)
for row in gdf.itertuples():
    gdf._set_value(row.Index, 'geometry', shapely.wkb.loads(shapely.wkb.dumps(row.geometry, output_dimension=2)))

# %%
# Project catchments to the same coordinate system
print('Setting CRS to epsg:4326.')
catchments = catchments.to_crs("epsg:4326")
flowlines = flowlines.to_crs("epsg:4326")
gdf = gdf.to_crs("epsg:4326")

# %%
# First we get the featureid for the catchment. This is a catchment id aka COMID
print(f'Retrieving one VPU {vpunum} flowline.')
flowline_instance = gdf.head(1)
print('Finding the catchment for the flowline.')
associatedCatchment = catchments[catchments.intersects(flowline_instance['geometry'])]
featureID = associatedCatchment["featureid"].iloc[0]

print("Find the mainstem associated with the flowline's catchment.")
# %%
# Next we get the associated flowline(s) for the catchment
relevantFlowline = flowlines[flowlines["COMID"] == featureID]

# All lines with the same LevelPathI form one continuous routed path (e.g., the entire main stem of a river);
# There is also a column for TerminalPath but that represents the ultimate destination of the flowline
# and thus could be very far away from the catchment
MAINSTEM_COLUMN = "LevelPathI"
mainstemID = relevantFlowline[MAINSTEM_COLUMN].iloc[0]

# %%
# Finally we use the id of the terminal path to find the associated geoconnex mainstem
mainstem_lookup = gpd.read_file("https://github.com/internetofwater/ref_rivers/releases/download/v2.1/mainstem_lookup.csv"
)
# The mainstem lookup CSV uses strings instead of integers so we cast
mainstem_lookup["lp_mainstem"] = mainstem_lookup["lp_mainstem"].astype(int)
mainstem_lookup["ref_mainstem_id"] = mainstem_lookup["ref_mainstem_id"].astype(int)

geoconnex_mainstem_id = mainstem_lookup.loc[mainstem_lookup["lp_mainstem"] == mainstemID]["ref_mainstem_id"].iloc[0]

# The point POINT (-108.50231860661755 39.05108882481538) is associated with the mainstem https://reference.geoconnex.us/collections/mainstems/items/29559
print(f"The associated mainstem is https://reference.geoconnex.us/collections/mainstems/items/{geoconnex_mainstem_id}")