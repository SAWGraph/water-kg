"""Create a .ttl file of Watershed Boundary Dataset data.
    Include HUC levels 2, 4, 6, 8, 10, and 12

Setup instructions

Required packages:
* geopandas
* shapely
* pandas
* zip
* rdflib (Graph and Literal)
* rdflib.namespace (GEO, OWL, PROV, RDF, RDFS, SDO, and XSD)
* pathlib (Path)
* namespaces (a local .py file with a dictionary of project namespaces)

Functions:
*
"""

import geopandas as gpd
import shapely
import pandas as pd
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
vpunum = '01'
# Valid codes: 01 to 22

### INPUT File and GPKG names ###
wbd_file = data_dir / f"HUC{vpunum}/WBD_{vpunum}_HU2_GPKG.zip"
gpkg_name = f'WBD_{vpunum}_HU2_GPKG.gpkg'

### OUTPUT Filename ###
main_ttl_file = ttl_dir / f"us_wbd_huc{vpunum}.ttl"

logname = log_dir / f"log_US_WBD_HUCxx-2ttl.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_huc_layer(gpkg_uri: str, level: int) -> gpd.GeoDataFrame:
    try:
        gdf = gpd.read_file(gpkg_uri, layer=f'WBDHU{level}')
        print(f'Level {level} has {gdf.shape[0]} rows')
        return gdf
    except Exception as e:
        print(f'Error loading layer: {e}')


def initial_kg(_PREFIX):
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def build_iris():
    pass


def process_huc_level_2_to_8(gpkg, huclevel):
    gdf = load_huc_layer(gpkg, huclevel)


def process_huc_level_10(gpkg):
    gdf = load_huc_layer(gpkg, '10')


def process_huc_level_12(gpkg):
    gdf = load_huc_layer(gpkg, '12')


def write_data_to_ttl():
    pass


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: VPU = {vpunum}')
    gpkg_handle = f'/vsizip/{wbd_file}/{gpkg_name}'
    for level in [2, 4, 6, 8]:
        process_huc_level_2_to_8(gpkg_handle, level)
    process_huc_level_10(gpkg_handle)
    process_huc_level_12(gpkg_handle)
    write_data_to_ttl()
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    print(f'\nRuntime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
