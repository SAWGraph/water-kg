"""Create a .ttl file of Watershed Boundary Dataset data.
    Include HUC levels 2, 4, 6, 8, 10, and 12

Setup instructions

Required packages:
* geopandas
* zip
* rdflib (Graph and Literal)
* rdflib.namespace (GEO, RDF, SDO, and XSD)
* pathlib (Path)
* namespaces (a local .py file with a dictionary of project namespaces)

Functions:
*
"""

import geopandas as gpd
from pathlib import Path
from rdflib import Graph, Literal
from rdflib.namespace import GEO, RDF, SDO, XSD

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
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_huc_layer(gpkg_uri: str, level: int):
    try:
        gdf = gpd.read_file(gpkg_uri, layer=f'WBDHU{level}')
        # print(f'Level {level} has {gdf.shape[0]} rows (from {gpkg_uri}).')
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


def build_iris(hid, level, _PREFIX):
    huc_iri = f'd.HUC{level}.' + str(hid)
    return _PREFIX["wbd_data"][huc_iri], _PREFIX["wbd_data"][huc_iri + '.geometry']


def process_huc(gpkg, level, graph, _PREFIX):
    logger.info(f'Load HUC{level} boundary file from {gpkg}.')
    gdf = load_huc_layer(gpkg, level)
    gdf.rename(columns={f'huc{level}': 'huc_num'}, inplace=True)
    logger.info(f'Triplify HUC{level} boundary data.')
    for row in gdf.itertuples():
        huciri, geomiri = build_iris(row.huc_num, level, _PREFIX)
        if ' ' not in huciri:
            graph.add((huciri, RDF.type, _PREFIX["wbd"][f'HUC{level}']))
            graph.add((huciri, _PREFIX["wbd"]['hucCode'], Literal(row.huc_num, datatype=XSD.string)))
            graph.add((huciri, SDO.name, Literal(row.name, datatype=XSD.string)))
            graph.add((huciri, GEO.hasGeometry, geomiri))
            graph.add((huciri, GEO.defaultGeometry, geomiri))
            graph.add((geomiri, RDF.type, GEO.Geometry))
            graph.add((geomiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
            for state in [ st.strip() for st in row.states.split(',') ]:
                graph.add((huciri, _PREFIX["wbd"]['hucState'], Literal(state, datatype=XSD.string)))
                # This could also be done as an object property linking to AR1 instances from the Spatial repo
            if level > 8:  # That is, HUCs 10 or 12 only
                graph.add((huciri, _PREFIX["wbd"]['hucType'], Literal(row.hutype, datatype=XSD.string)))
                graph.add((huciri, _PREFIX["wbd"]['hucTypeDescription'], Literal(row.hutype_description, datatype=XSD.string)))
            if level > 10 and row.tohuc.lower() != 'closed basin':  # That is, HUC 12 only
                    tohuciri, tohucgeomiri = build_iris(row.tohuc, level, _PREFIX)
                    graph.add((huciri, _PREFIX["wbd"]['toHUC'], tohuciri))
            if level > 2:
                containing_huciri, containing_hucgeomiri = build_iris(row.huc_num[:-2], level - 2, _PREFIX)
                graph.add((huciri, _PREFIX["wbd"]['containingHUC'], containing_huciri))
    return graph


def write_graph_to_ttl(graph, outfile):
    logger.info(f'Serialize the triples to {outfile}')
    graph.serialize(outfile, format='ttl')


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: VPU = {vpunum}')
    gpkg_handle = f'/vsizip/{wbd_file}/{gpkg_name}'
    kg = initial_kg(_PREFIX)
    for huclevel in [2, 4, 6, 8, 10, 12]: # Only triplify up to level 12 as it is the last conterminous level
        kg = process_huc(gpkg_handle, huclevel, kg, _PREFIX)
    write_graph_to_ttl(kg, main_ttl_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    print(f'\nRuntime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
