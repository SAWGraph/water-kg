"""Create a .ttl file of flowlines and their connectivity from a .shp file and a .dbf file

Under ### INPUT Filenames ###, define
    the name (and path) of the input .shp file
    the name (and path) of the input .dbf file
Under ### OUTPUT Filenames ###, define
    the name (and path) of the main output .ttl file
    the name (and path) of the output .ttl file for the head/outlet data

Required:
    * simpledbf (DBf5)
    * geopandas
    * pandas
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, SDO, and XSD)
    * shapely (to_geojson)
    * variable (a local .py file with a dictionary of project namespaces)

Functions:
    * load_dbf_file -
    * load_shp_file -
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a waterbody and its geometry
    * create_flow_dict -
    * process_flowline_shp2ttl -
"""

from simpledbf import Dbf5
import geopandas as gpd
import pandas as pd
from rdflib import Graph, Literal
from rdflib.namespace import GEO, OWL, PROV, RDF, RDFS, SDO, XSD
import json
from shapely import to_geojson

import logging
import time
import datetime

import sys
import os

# Modify the system path to find variable.py
sys.path.insert(1, 'G:/My Drive/UMaine Docs from Laptop/SAWGraph/Data Sources')
from variable import _PREFIX

# Set the current directory to this file's directory
os.chdir('G:/My Drive/UMaine Docs from Laptop/SAWGraph/Data Sources/Surface Water')

### INPUT Filenames ###
flowplus_file = r'../Geospatial/HUC01/NE_01_NHDPlusAttributes/PlusFlow.dbf'
flowline_file = r'../Geospatial/HUC01/NE_01_NHDSnapshot/NHDFLowline.shp'
# flowline_file = r'../Geospatial/Maine/NHDFLowline_BBox.shp'

### OUTPUT Filenames ###
main_ttl_file = 'us_nhd_flowline_huc01.ttl'
headoutlet_ttl_file = 'us_nhd_flowline_huc01_headoutlet.ttl'

# ttl_file = '../ttl files/me_reaches_bbox.ttl'

logname = 'log_US_NHD_Flowline_HUC01-2-tto.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_dbf_file(filename):
    """

    :param filename:
    :return:
    """
    logger.info('Loading the dbf file (PlusFlow from the NHD)')
    dbf = Dbf5(filename)
    df = dbf.to_dataframe()
    df.drop(['FROMHYDSEQ',
             'FROMLVLPAT',
             'TOHYDSEQ',
             'TOLVLPAT',
             'NODENUMBER',
             'DELTALEVEL',
             'DIRECTION',
             'GAPDISTKM',
             'HasGeo',
             'TotDASqKM',
             'DivDASqKM'],
            axis=1,
            inplace=True)
    df[['FROMCOMID', 'TOCOMID']] = df[['FROMCOMID', 'TOCOMID']].astype(str)
    # print(df.dtypes)
    return df


def load_shp_file(filename):
    """

    :param filename:
    :return:
    """
    logger.info('Loading the shp file (NHDFlowline from the NHD)')
    df = gpd.read_file(filename)
    df.drop(['FLOWDIR',
             'WBAREACOMI',
             'ENABLED',
             'GNIS_NBR'],
            axis=1,
            inplace=True)
    df[['COMID', 'REACHCODE']] = df[['COMID', 'REACHCODE']].astype(str)
    # print(df.dtypes)
    return df


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
    """

    :param cid:
    :param _PREFIX:
    :return:
    """
    # logger.info('Building the IRIs')
    flowlineIRI = _PREFIX['gcx-cid'][cid]
    flowlineGeoIRI = _PREFIX['gcx-cid'][cid + '.geometry']
    # The following are a fudge for now.
    # These points need to be connected to their COMIDs for better integration with Geoconnex
    outletIRI = _PREFIX['gcx-cid'][cid + '.outlet']
    outletGeoIRI = _PREFIX['gcx-cid'][cid + '.outlet.geometry']
    headIRI = _PREFIX['gcx-cid'][cid + '.head']
    headGeoIRI = _PREFIX['gcx-cid'][cid + '.head.geometry']
    return flowlineIRI, flowlineGeoIRI, outletIRI, outletGeoIRI, headIRI, headGeoIRI


def create_flow_dict(dbf) -> dict:
    """

    :param dbf:
    :return:
    """
    logger.info('Creating dictionary of flowline connectivity')
    df = load_dbf_file(dbf)
    dct = {}
    for row in df.itertuples():
        if row.FROMCOMID in dct.keys():
            dct[row.FROMCOMID].append(row.TOCOMID)
        else:
            dct[row.FROMCOMID] = [row.TOCOMID]
    return dct


def process_flowline_shp2ttl(shpfile, dbffile, main_outfile, headoutlet_outfile, _PREFIX):
    """

    :param shpfile:
    :param dbffile:
    :param outfile:
    :param _PREFIX:
    :return:
    """
    logger.info('Begin processing flowlines and connectivity')
    flow_dict = create_flow_dict(dbffile)
    flowline_df = load_shp_file(shpfile)
    grouping = str.maketrans('[]', '()')
    logger.info('Intializing the knowledge graph')
    kg1 = initial_kg(_PREFIX)  # flowlines
    kg2 = initial_kg(_PREFIX)  # head and outlet points

    logger.info('Begin triplifying the data')
    for row in flowline_df.itertuples():
        flowlineIRI, flowlineGeoIRI, outletIRI, outletGeoIRI, headIRI, headGeoIRI = build_iris(row.COMID, _PREFIX)

        # There's an assumption that all flowlines are drawn from head to outlet
        #    Based on a very small sample it is correct
        #    This should be verified more concretely
        geom_json = json.loads(to_geojson(row.geometry))
        head = str(geom_json['coordinates'][0]).translate(grouping)
        outlet = str(geom_json['coordinates'][-1]).translate(grouping)

        # Create triples for current COMID
        #    Note: ReachCodes are not unique in NHDFlowline
        # This is based on Geoconnex as much as possible
        kg1.add((flowlineIRI, RDF.type, SDO.Place))
        kg1.add((flowlineIRI, RDF.type, _PREFIX['hyf']['HY_FlowPath']))
        kg1.add((flowlineIRI, RDF.type, _PREFIX['hyf']['HY_Waterbody']))

        kg1.add((flowlineGeoIRI, RDF.type, GEO.Geometry))
        kg1.add((flowlineIRI, GEO.defaultGeometry, flowlineGeoIRI))
        kg1.add((flowlineIRI, GEO.hasGeometry, flowlineGeoIRI))
        kg1.add((flowlineGeoIRI, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg1.add((flowlineGeoIRI, RDF.type, _PREFIX['sf']['LineString']))
        # Skipping schema:geo

        if not pd.isnull(row.GNIS_NAME):
            kg1.add((flowlineIRI, SDO.name, Literal(row.GNIS_NAME, lang='en')))
        kg1.add((flowlineIRI, _PREFIX['saw_water']['hasCOMID'], Literal(str(row.COMID), datatype=XSD.string)))
        kg1.add((flowlineIRI, _PREFIX['saw_water']['hasReachCode'], Literal(str(row.REACHCODE), datatype=XSD.string)))
        kg1.add((flowlineIRI, _PREFIX['saw_water']['hasFTYPE'], Literal(str(row.FTYPE), datatype=XSD.string)))
        kg1.add((flowlineIRI, _PREFIX['saw_water']['hasFCODE'], Literal(str(row.FCODE), datatype=XSD.string)))

        # TODO: Add a unit (km) to P2043 via Q1978718
        kg1.add((flowlineIRI, _PREFIX['wdp']['P2043'], Literal(row.LENGTHKM, datatype=XSD.float)))
        # Skipping P2053 since this data is not in NHDFlowline

        # In Geoconnex, P403 and P885 point to COMID objects (LineString objects), not nodes
        #    as well as HUC12 objects (Point objects). But not all point to HUC12 objects.
        # This creates new points:
        #    1: Create the point as a geo:Feature
        #    2: Assign the object a geo:Geometry
        #    3: Assign the geometry geo:asWKT coordinates
        #    4: Assign the feature to P403/P885 as the flowline's outlet/head (see note above)
        kg2.add((outletIRI, RDF.type, GEO.Feature))
        kg2.add((outletIRI, GEO.defaultGeometry, outletGeoIRI))
        kg2.add((outletIRI, GEO.hasGeometry, outletGeoIRI))
        kg2.add((outletGeoIRI, GEO.asWKT, Literal('POINT ' + outlet, datatype=GEO.wktLiteral)))
        kg2.add((flowlineIRI, _PREFIX['wdp']['P403'], outletIRI))

        kg2.add((headIRI, RDF.type, GEO.Feature))
        kg2.add((headIRI, GEO.defaultGeometry, headGeoIRI))
        kg2.add((headIRI, GEO.hasGeometry, headGeoIRI))
        kg2.add((headGeoIRI, GEO.asWKT, Literal('POINT ' + head, datatype=GEO.wktLiteral)))
        kg2.add((flowlineIRI, _PREFIX['wdp']['P885'], headIRI))

        if row.COMID in flow_dict.keys():
            for cid in flow_dict[row.COMID]:
                kg1.add((flowlineIRI, _PREFIX['hyf']['downstreamWaterbody'], _PREFIX['gcx-cid'][cid]))
        kg1.add((flowlineIRI, _PREFIX['hyf']['downstreamWaterbody'], flowlineIRI))
        # Skipping hyf:encompassingCatchment

    logger.info('Write the triples to a .ttl file')
    kg1.serialize(main_outfile, format='turtle')
    kg2.serialize(headoutlet_outfile, format='turtle')


if __name__ == '__main__':
    start_time = time.time()
    process_flowline_shp2ttl(flowline_file, flowplus_file, main_ttl_file, headoutlet_ttl_file, _PREFIX)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    print(f'\nRuntime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
