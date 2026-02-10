"""Create a .ttl file for water bodies from a .shp file

Under ### HUCxx VPU ###, enter
    the VPU code for the current HUC2 region (valid codes listed below)
Under ### INPUT Filenames ###, modify (if necessary)
    the name (and path) of the input .shp file (NHDWaterbody)
Under ### OUTPUT Filename ###, modify (if necessary)
    the name (and path) of the output .ttl file

Required:
    * geopandas
    * pandas
    * shapely (LineString, Point, and Polygon)
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, and XSD)
    * pathlib (Path)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a water body and its geometry
    * process_waterbodies_shp2ttl - takes a .shp file and an output file name and creates and saves a .ttl file
"""

import geopandas as gpd
import pandas as pd
# import shapely
from pathlib import Path
from rdflib import Graph, Literal
from rdflib.namespace import GEO, OWL, PROV, RDF, RDFS, SDO, XSD

import logging
import time
import datetime

import sys
import os

# Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent
data_dir = cwd.parent / "data"
ttl_dir = cwd / "ttl_files"
log_dir = cwd / "logs"
# print(f"Current working directory:      {cwd}")
# print(f"Github repos and namespaces.py: {ns_dir}")
# print(f"Data (input) directory:         {data_dir}")
# print(f"Turtle (output) directory:      {ttl_dir}")
# print(f"Logging directory:              {log_dir}")

# Modify the system path to find namespaces.py
# sys.path.insert(1, 'G:/My Drive/Laptop/SAWGraph/Data Sources')
sys.path.insert(0, str(ns_dir))
from namespaces import _PREFIX

# Set the current directory to this file's directory
os.chdir(cwd)

### HUCxx VPU ###
vpunums = [ '10L', '11', '13', '14' ]
# Valid codes: 01, 02, 03N, 03S, 03W, 04, 05, 06, 07, 08, 09, 10U, 10L, 11, 12, 13, 14, 15, 16, 17, 18, 20

### INPUT Filenames ###
# Sometimes there are bad geometries in the NHDWaterbody.shp file
# The path looks for a "fixed" version first but defaults to the original version if a "fixed" version does not exist
waterbody_file = data_dir / f'Hydrofabric/reference_CONUS.gpkg'
waterbody_layer = 'reference_waterbody'
epsg_in = 5070
epsg_out = 4326

### OUTPUT Filename ###
ttl_files = [ ]
for vpunum in vpunums:
    ttl_files.append(ttl_dir / f"hydrofabric_waterbody_huc{vpunum}.ttl")

logname = log_dir / f"log_HydrofabricWaterbody2ttl.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')

def load_waterbody_layer(filename: Path, layer: str, epsg_in: int, epsg_out: int) -> gpd.GeoDataFrame:
    logger.info(f'Load water bodies from {layer} layer of {filename} to GeoDataFrame')
    gdf = gpd.read_file(filename, layer=layer, use_arrow=True)
    logger.info(f'Convert CRS from EPSG:{epsg_in} to EPSG:{epsg_out}')
    gdf.set_crs(epsg=epsg_in, inplace=True)
    gdf.to_crs(epsg=epsg_out, inplace=True)
    return gdf


def get_vpu_waterbodies(vpunum: str, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    logger.info(f'Get HUC{vpunum} water bodies')
    df = df[df.vpu == vpunum]
    return df


def initial_kg(_PREFIX: dict) -> Graph:
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    logger.info('Intialize RDFLib Graph')
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def build_iris(cid: str, _PREFIX: dict) -> tuple:
    """Create IRIs for a water body and its geometry

    This varies from Geoconnex notation which currently contains no water bodies beyond mainstems
        They have a mainstem URI; e.g., https://geoconnex.us/ref/mainstems/######
        The connected geometry is a blank node that connects to the geo:asWKT object

    :param cid: The COMID value for a water body
    :param _PREFIX:
    :return: a tuple with the two IRIs
    """
    return _PREFIX["gcx_cid"][cid], _PREFIX["gcx_cid"][cid + '.geometry']


def process_waterbodies_2ttl(vpunum: str, df: gpd.GeoDataFrame, outfile: Path) -> None:
    """Triplifies the water body data in a .shp file and saves the result as a .ttl file

    :param vpunum: A VPU (2-digit HUC) number
    :param df: A GeoDataFrame containing water bodies for the VPU
    :param outfile: A path to a .ttl file
    :return:
    """
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    logger.info(f'Triplify HUC{vpunum} water bodies')
    for row in df.itertuples():
        if '{' in row.comid:
            continue
        # Get IRIs for the current NHDWaterbody and its geometry
        bodyiri, geomiri = build_iris(row.comid, _PREFIX)
        if 'estuary' in row.ftype.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Estuary']))
        elif 'lake' in row.ftype.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Lake']))
        elif 'reservoir' in row.ftype.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Impoundment']))
        else:
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_WaterBody']))

        # Triplify the geometry for the current NHDWaterbody
        kg.add((bodyiri, GEO.hasGeometry, geomiri))
        kg.add((bodyiri, GEO.defaultGeometry, geomiri))
        kg.add((geomiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg.add((geomiri, RDF.type, GEO.Geometry))

        # Triplify current NHDWaterbody attributes
        if not pd.isnull(row.gnis_name):
            kg.add((bodyiri, SDO.name, Literal(row.gnis_name, datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasCOMID'], Literal(str(row.comid), datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasFTYPE'], Literal(str(row.ftype), datatype=XSD.string)))
        # kg.add((bodyiri, _PREFIX['nhdplusv2']['hasFCODE'], Literal(str(row.fcode), datatype=XSD.string)))
        # kg.add((bodyiri, _PREFIX['nhdplusv2']['hasReachCode'], Literal(str(row.reachcode), datatype=XSD.string)))
        # if row.reachcode is not None:
        #     kg.add((bodyiri, _PREFIX['wbd']['containingHUC'], _PREFIX['wbd_data']['d.HUC8.' + str(row.reachcode)[:8]]))
    logger.info(f'Write HUC{vpunum} water body triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: HUC/VPU set = {vpunums}')
    gdf = load_waterbody_layer(waterbody_file, waterbody_layer, epsg_in, epsg_out)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    for vpunum, outfile in zip(vpunums, ttl_files):
        start_time = time.time()
        logger.info('')
        logger.info(f'Processing HUC/VPU {vpunum}')
        gdf_vpu = get_vpu_waterbodies(vpunum, gdf)
        process_waterbodies_2ttl(vpunum, gdf_vpu, outfile)
        logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
