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
import shapely
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
shp_files = [ ]
for vpunum in vpunums:
    file = data_dir / f'NHDWaterbody/HUC{vpunum}_NHDWaterbody-fixed.shp'
    if not os.path.isfile(file):
        file = data_dir / f'NHDWaterbody/HUC{vpunum}_NHDWaterbody.shp'
    shp_files.append(file)

### OUTPUT Filename ###
ttl_files = [ ]
for vpunum in vpunums:
    ttl_files.append(ttl_dir / f"us_nhd_waterbody_huc{vpunum}.ttl")

logname = log_dir / f"log_US_NHD_Waterbody_HUCxx-2ttl.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_waterbodies(vpunum: str, filename: Path) -> gpd.GeoDataFrame:
    logger.info(f'Load VPU {vpunum} water bodies from {filename} to GeoDataFrame')
    gdf = gpd.read_file(filename, use_arrow=True)
    gdf.columns = gdf.columns.str.upper()
    return gdf


def initial_kg(_PREFIX: dict) -> Graph:
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def build_iris(cid: int | str, _PREFIX: dict) -> tuple:
    """Create IRIs for a water body and its geometry

    This varies from Geoconnex notation which currently contains no water bodies beyond mainstems
        They have a mainstem URI; e.g., https://geoconnex.us/ref/mainstems/######
        The connected geometry is a blank node that connects to the geo:asWKT object

    :param cid: The COMID value for a water body
    :param _PREFIX:
    :return: a tuple with the two IRIs
    """
    return _PREFIX["gcx_cid"][str(cid)], _PREFIX["gcx_cid"][str(cid) + '.geometry']


def process_waterbodies_shp2ttl(vpunum, infile, outfile):
    """Triplifies the water body data in a .shp file and saves the result as a .ttl file

    :param infile: a .shp file with NHD water body data
    :param outfile: the path and name for the .ttl file
    :return:
    """
    # Read NHDWaterbody to a GeoDataframe
    gdf_waterbody = load_waterbodies(vpunum, infile)

    # KWG script doesn't like 3D polygons so this forces them all to 2D
    #   The Z value is set to 0 in NHDWaterbody so nothing is lost from this process
    logger.info('Force geometries to 2D')
    for row in gdf_waterbody.itertuples():
        gdf_waterbody._set_value(row.Index, 'geometry',
                                 shapely.wkb.loads(shapely.wkb.dumps(row.GEOMETRY, output_dimension=2)))

    logger.info('Intialize RDFLib Graph')
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    logger.info(f'Triplify HUC{vpunum} water bodies')
    for row in gdf_waterbody.itertuples():
        # Get IRIs for the current NHDWaterbody and its geometry
        bodyiri, geomiri = build_iris(row.COMID, _PREFIX)
        if 'estuary' in row.FTYPE.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Estuary']))
        elif 'lake' in row.FTYPE.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Lake']))
        elif 'reservoir' in row.FTYPE.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Impoundment']))
        else:
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_WaterBody']))

        # Triplify the geometry for the current NHDWaterbody
        kg.add((bodyiri, GEO.hasGeometry, geomiri))
        kg.add((bodyiri, GEO.defaultGeometry, geomiri))
        kg.add((geomiri, GEO.asWKT, Literal(row.GEOMETRY, datatype=GEO.wktLiteral)))
        kg.add((geomiri, RDF.type, GEO.Geometry))

        # Triplify current NHDWaterbody attributes
        if not pd.isnull(row.GNIS_NAME):
            kg.add((bodyiri, SDO.name, Literal(row.GNIS_NAME, datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasCOMID'], Literal(str(row.COMID), datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasFTYPE'], Literal(str(row.FTYPE), datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasFCODE'], Literal(str(row.FCODE), datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasReachCode'], Literal(str(row.REACHCODE), datatype=XSD.string)))
        if row.REACHCODE is not None:
            kg.add((bodyiri, _PREFIX['wbd']['containingHUC'], _PREFIX['wbd_data']['d.HUC8.' + str(row.REACHCODE)[:8]]))

    logger.info(f'Write HUC{vpunum} water body triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    logger.info(f'Launching script: HUC/VPU set = {vpunums}')
    for vpunum, infile, outfile in zip(vpunums, shp_files, ttl_files):
        start_time = time.time()
        logger.info('')
        logger.info(f'Processing HUC/VPU {vpunum}')
        process_waterbodies_shp2ttl(vpunum, infile, outfile)
        logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
