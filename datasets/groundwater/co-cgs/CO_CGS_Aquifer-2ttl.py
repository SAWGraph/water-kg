"""Create a .ttl file for Colorado's alluvial aquifers from a .shp file containing aquifer geometries

Under ### INPUT Filename ###, define
    the name (and path) of the input .shp file
Under ### OUTPUT Filenames ###, define
    the name (and path) of the output .shp file (for the processed aquifer layer)
    the name (and path) of the output .ttl file for aquifers
    the name (and path) of the output .ttl file for aquifer systems

Required:
    * geopandas
    * pandas
    * shapely (LineString, Point, and Polygon)
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, and XSD)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * read_shp_2_gdf - takes a .shp file and returns a gdf
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for an aquifer and its geometry
    * process_aquifers_shp2ttl - takes two .shp files (aquifers and S2 cells), an output file name, and a dictionary
                                 of dissolved ids to lists of original ids, and creates and saves a .ttl file
"""

import geopandas as gpd
from pathlib import Path
from rdflib import Graph, Literal
from rdflib.namespace import GEO, DCTERMS, OWL, PROV, RDF, RDFS, SDO, XSD

import logging
import time
import datetime

import sys
import os

# Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent.parent
data_dir = cwd.parent.parent / "data"
ttl_dir = cwd / "ttl_files"
log_dir = cwd / "logs"
# print(f"Current working directory:      {cwd}")
# print(f"Github repos and namespaces.py: {ns_dir}")
# print(f"Data (input) directory:         {data_dir}")
# print(f"Turtle (output) directory:      {ttl_dir}")
# print(f"Logging directory:              {log_dir}")

# Modify the system path to find namespaces.py
sys.path.insert(0, str(ns_dir))
from namespaces import _PREFIX, find_s2_intersects_poly

# Set the current directory to this file's directory
os.chdir(cwd)

### INPUT Filename ###
# aquifer_shp_path: QGIS was used to export the aquifer layer to .shp from a .gdb found online
aquifer_shp_path = data_dir / 'CO_Groundwater/Colorado_Alluvial_Aquifer.shp'
epsg_in = 26913
epsg_out = 4326

### OUTPUT Filenames ###
# aq_ttl_file: the resulting (output) .ttl file
aq_ttl_file = ttl_dir / 'co_08_cgs_alluvial_aquifers.ttl'

logname = log_dir / 'log_CO_CGS_Alluvial_Aquifers2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_aquifers_file(filename: Path, epsg_in: int, epsg_out: int) -> gpd.GeoDataFrame:
    logger.info(f'Load aquifers from {filename} to GeoDataFrame')
    gdf = gpd.read_file(filename)
    gdf[['OBJECTID']] = gdf[['OBJECTID']].astype(int).astype(str)
    logger.info(f'Convert CRS from EPSG:{epsg_in} to EPSG:{epsg_out}')
    gdf.set_crs(epsg=epsg_in, inplace=True)
    gdf.to_crs(epsg=epsg_out, inplace=True)
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


def build_cgs_iris(cgsid: int, _PREFIX: dict, max_id_length = 3) -> tuple:
    """Create IRIs for an aquifer and its geometry

    :param cgsid: The object id value for an aquifer
    :param _PREFIX: a dictionary of prefixes
    :return: a tuple with two IRIs
    """
    return (_PREFIX["co_cgs_data"]['d.CGS-AlluvialAquifer.' + str(cgsid).zfill(max_id_length)],
            _PREFIX["co_cgs_data"]['d.CGS-AlluvialAquifer.Geometry.' + str(cgsid).zfill(max_id_length)])


def process_aquifers_shp2ttl(infile: Path, outfile: Path, epsg_in: int, epsg_out: int, max_id_length = 3) -> None:
    """Triplifies the aquifer data in a .shp file and saves the result as a .ttl file

    :param infile: a zipped file containing a .gdb folder
    :param infolder: the name of the zipped .gdb folder
    :param outfile: the path and name for the aquifer .ttl file
    :return:
    """
    gdf_aq = load_aquifers_file(infile, epsg_in, epsg_out)
    logger.info('Intialize the knowledge graph')
    kg_aq = initial_kg(_PREFIX)
    logger.info('Triplify the aquifers')
    for row in gdf_aq.itertuples():
        aqiri, geoiri = build_cgs_iris(row.OBJECTID, _PREFIX)
        kg_aq.add((aqiri, RDF.type, _PREFIX['gwml2']['GW_Aquifer']))
        kg_aq.add((aqiri, _PREFIX['co_cgs']['alluvialAquiferId'], Literal(str(row.OBJECTID).zfill(max_id_length), datatype=XSD.string)))
        kg_aq.add((aqiri, _PREFIX['co_cgs']['riverBasin'], Literal(row.River_Basi, datatype=XSD.string)))
        kg_aq.add((aqiri, GEO.hasGeometry, geoiri))
        kg_aq.add((aqiri, GEO.defaultGeometry, geoiri))
        kg_aq.add((geoiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg_aq.add((geoiri, RDF.type, GEO.Geometry))
    logger.info(f'Write aquifer triples to {outfile}')
    kg_aq.serialize(outfile, format='turtle')


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: Colorado Alluvial Aquifers')
    process_aquifers_shp2ttl(aquifer_shp_path, aq_ttl_file, epsg_in, epsg_out)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
