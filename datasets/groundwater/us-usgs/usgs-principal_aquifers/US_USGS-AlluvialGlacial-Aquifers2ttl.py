"""Create a .ttl file for USGS alluvial/glacial aquifers from a .shp file

Under ### INPUT Filenames ###, modify (if necessary)
    the name (and path) of the input .shp file (alluvial)
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
    * process_aquifers_shp2ttl - takes a .shp file and an output file name and creates and saves a .ttl file
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
ns_dir = cwd.parent.parent.parent.parent.parent
data_dir = cwd.parent.parent.parent / "data"
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

### INPUT Filenames ###
aquifers_file = data_dir / f"US_Aquifers/alluvial.shp"

### OUTPUT Filename ###
ttl_file = ttl_dir / f"us_usgs-alluvialglacial-aquifers.ttl"

logname = log_dir / f"log_US_USGS-AlluvialGlacial-Aquifers2ttl.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')

def initial_kg(_PREFIX):
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def build_iris(objectid, _PREFIX):
    """Create IRIs for an aquifer and its geometry

    :param objectid: The unique identifying value for an aquifer
    :param _PREFIX:
    :return: a tuple with the two IRIs
    """
    base_iri = f'd.USGS_AlluvialGlacialAquifer_{str(objectid).zfill(4)}'
    return _PREFIX["usgs_data"][base_iri], _PREFIX["usgs_data"][base_iri + '.geometry']


def get_rock_name(rockname):
    if rockname == 'Unconsolidated sand and gravel aquifers':
        return 'UnconsolidatedSandGravel'
    elif rockname == None:
        return 'Unspecified'
    else:
        raise ValueError("Unexpected ROCK_NAME from alluvial & glacial aquifers shape file")


def process_aquifers_shp2ttl(infile, outfile):
    """Triplifies the principal aquifer data in a .shp file and saves the result as a .ttl file

    :param infile: a .shp file with NHD water body data
    :param outfile: the path and name for the .ttl file
    :return:
    """
    logger.info(f'Load alluvial & glacial aquifer shapefile from {infile}')

    # Read alluvial & glacial aquifers to a GeoDataframe
    gdf_aquifers = gpd.read_file(infile)

    logger.info('Intialize RDFLib Graph')
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    count = 1  # For processing updates printed to terminal
    n = len(gdf_aquifers.index)  # For processing updates printed to terminal
    logger.info(f'Triplify principal aquifers')
    for row in gdf_aquifers.itertuples():
        # Get IRIs for the current principal aquifer and its geometry
        aqiri, geomiri = build_iris(row.ALLUVIAL_, _PREFIX)
        kg.add((aqiri, RDF.type, _PREFIX['gwml2']['GW_Aquifer']))

        # Triplify the geometry for the current principal aquifer
        kg.add((aqiri, GEO.hasGeometry, geomiri))
        kg.add((aqiri, GEO.defaultGeometry, geomiri))
        kg.add((geomiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg.add((geomiri, RDF.type, GEO.Geometry))

        # Triplify current principal aquifer attributes
        kg.add((aqiri, _PREFIX['usgs']['hasAlluvialGlacialId'], Literal(str(row.ALLUVIAL_).zfill(4), datatype=XSD.string)))
        kg.add((aqiri, _PREFIX['usgs']['hasRockName'], _PREFIX['usgs'][f'RockName.{get_rock_name(row.ROCK_NAME)}']))
        kg.add((aqiri, _PREFIX['usgs']['hasAqName'], Literal(row.AQ_NAME, datatype=XSD.string)))

        # Update the processing status to the terminal
        print(f'Processing row {count:4} of {n} : OBJECTID {str(row.ALLUVIAL_):4}', end='\r', flush=True)
        count += 1
    logger.info(f'Write alluvial & glacial aquifer triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script')
    process_aquifers_shp2ttl(aquifers_file, ttl_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
