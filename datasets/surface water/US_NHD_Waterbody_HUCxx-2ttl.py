"""Create a .ttl file for water bodies from a .shp file

Under ### HUCxx VPU ###, enter
    the VPU code for the current HUC2 region (valid codes listed below)
Under ### INPUT Filenames ###, define
    the name (and path) of the input .shp file (NHDWaterbody)
Under ### OUTPUT Filename ###, define
    the name (and path) of the output .ttl file

Required:
    * geopandas
    * pandas
    * shapely (LineString, Point, and Polygon)
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, and XSD)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a water body and its geometry
    * process_waterbodies_shp2ttl - takes a .shp file and an output file name and creates and saves a .ttl file
"""

import geopandas as gpd
import pandas as pd
import shapely
from rdflib import Graph, Literal
from rdflib.namespace import GEO, OWL, PROV, RDF, RDFS, SDO, XSD

import logging
import time
import datetime

import sys
import os

# Modify the system path to find namespaces.py
sys.path.insert(1, 'G:/My Drive/Laptop/SAWGraph/Data Sources')
from namespaces import _PREFIX

# Set the current directory to this file's directory
os.chdir('G:/My Drive/Laptop/SAWGraph/Data Sources/Hydrology/Surface Water')

### HUCxx VPU ###
vpu = 'MS_07'
vpunum = vpu[3:]
# Valid codes: NE_01, MA_02, SA_03N, SA_03S, SA_03W, GL_04, MS_05, MS_06, MS_07, MS_08, SR_09,
#              MS_10U, MS_10L, MS_11, TX_12, RG_13, CO_14, CO_15, GB_16, PN_17, CA_18, HI_20

### INPUT Filenames ###
# Sometimes there are bad geometries in the NHDWaterbody.shp file
# The path assumes a "fixed" version but defaults to the original version if the "fixed" version does not exist
waterbody_file = '../../Geospatial/HUC' + vpunum + '/' + vpu + '_NHDSnapshot/NHDWaterbody-fixed.shp'
if not os.path.isfile(waterbody_file):
    waterbody_file = '../../Geospatial/HUC' + vpunum + '/' + vpu + '_NHDSnapshot/NHDWaterbody.shp'

### OUTPUT Filename ###
ttl_file = 'ttl_files/us_nhd_waterbody_huc' + vpunum + '.ttl'

logname = 'logs/log_US_NHD_Waterbody_HUCxx-2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
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


def build_iris(cid, _PREFIX):
    """Create IRIs for a water body and its geometry

    This varies from Geoconnex notation which currently contains no water bodies beyond mainstems
        They have a mainstem URI; e.g., https://geoconnex.us/ref/mainstems/######
        The connected geometry is a blank node that connects to the geo:asWKT object

    :param cid: The COMID value for a water body
    :param _PREFIX:
    :return: a tuple with the two IRIs
    """
    return _PREFIX["gcx-cid"][str(cid)], _PREFIX["gcx-cid"][str(cid) + '.geometry']


def process_waterbodies_shp2ttl(infile, outfile):
    """Triplifies the water body data in a .shp file and saves the result as a .ttl file

    :param infile: a .shp file with NHD water body data
    :param outfile: the path and name for the .ttl file
    :return:
    """
    logger.info(f'Load {vpu} water body shapefile from {infile}')

    # Read NHDWaterbody to a GeoDataframe
    gdf_waterbody = gpd.read_file(infile)

    # KWG script doesn't like 3D polygons so this forces them all to 2D
    #   The Z value is set to 0 in NHDWaterbody so nothing is lost from this process
    logger.info('Force geometries to 2D')
    for row in gdf_waterbody.itertuples():
        gdf_waterbody._set_value(row.Index, 'geometry',
                                 shapely.wkb.loads(shapely.wkb.dumps(row.geometry, output_dimension=2)))

    logger.info('Intialize RDFLib Graph')
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    count = 1  # For processing updates printed to terminal
    n = len(gdf_waterbody.index)  # For processing updates printed to terminal
    logger.info(f'Triplify {vpu} water bodies')
    for row in gdf_waterbody.itertuples():
        # Get IRIs for the current NHDWaterbody and its geometry
        bodyiri, geomiri = build_iris(row.COMID, _PREFIX)
        if 'estuary' in row.FTYPE.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Estuary']))
        elif 'lake' in row.FTYPE.lower():
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_Lake']))
        else:
            kg.add((bodyiri, RDF.type, _PREFIX['hyf']['HY_WaterBody']))

        # Triplify the geometry for the current NHDWaterbody
        kg.add((bodyiri, GEO.hasGeometry, geomiri))
        kg.add((bodyiri, GEO.defaultGeometry, geomiri))
        kg.add((geomiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg.add((geomiri, RDF.type, GEO.Geometry))

        # Triplify current NHDWaterbody attributes
        if not pd.isnull(row.GNIS_NAME):
            kg.add((bodyiri, SDO.name, Literal(row.GNIS_NAME, datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasCOMID'], Literal(str(row.COMID), datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasReachCode'], Literal(str(row.REACHCODE), datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasFTYPE'], Literal(str(row.FTYPE), datatype=XSD.string)))
        kg.add((bodyiri, _PREFIX['nhdplusv2']['hasFCODE'], Literal(str(row.FCODE), datatype=XSD.string)))

        # Update the processing status to the terminal
        print(f'Processing row {count:5} of {n} : COMID {str(row.COMID):9}', end='\r', flush=True)
        count += 1
    logger.info(f'Write {vpu} water body triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: HUC/VPU = {vpu}')
    process_waterbodies_shp2ttl(waterbody_file, ttl_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    print(f'\nRuntime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
