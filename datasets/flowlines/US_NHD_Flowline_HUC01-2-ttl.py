"""Create a .ttl file of flowlines and their connectivity from a .shp file and a .dbf file

Under ### INPUT Filenames ###, define
    the name (and path) of the input .shp file (NHDFlowline)
    the name (and path) of the input .dbf file (PlusFlow)
Under ### OUTPUT Filename ###, define
    the name (and path) of the main output .ttl file

Required:
    * simpledbf (DBf5)
    * geopandas
    * pandas
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, SDO, and XSD)
    * networkx
    * variable (a local .py file with a dictionary of project namespaces)

Functions:
    * load_flowline_file -
    * load_plusflow_file -
    * create_simple_flowline_dict -
    * create_simple_plusflow_dict -
    * create_digraph -
    * count_by_degree -
    * print_digraph_stats -
    * print_dictionary_stats -
    * print_root_and_leaf_counts -
    * analyze_paths_from_source_to_outlet -
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a waterbody and its geometry
    * create_flow_dict -
    * process_flowline_shp2ttl -
"""

from simpledbf import Dbf5
import geopandas as gpd
import shapely
import pandas as pd
import networkx as nx
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
os.chdir('G:/My Drive/Laptop/SAWGraph/Data Sources/Surface Water')

### INPUT Filenames ###
plusflow_file = r'../Geospatial/HUC01/NE_01_NHDPlusAttributes/PlusFlow.dbf'
flowline_file = r'../Geospatial/HUC01/NE_01_NHDSnapshot/NHDFlowline.shp'

### OUTPUT Filename ###
main_ttl_file = 'ttl_files/us_nhd_flowline_huc01.ttl'

logname = 'logs/log_US_NHD_Flowline_HUC01-2-ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_flowline_file(filename: str) -> gpd.GeoDataFrame:
    logger.info('Begin loading flowline file')
    gdf = gpd.read_file(filename)
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
    logger.info('Finish loading flowline file')
    return gdf


def create_simple_flowline_dict(df: pd.DataFrame) -> dict:
    logger.info('Begin creating simple flowline dictionary')
    dct = {}
    for row in df.itertuples():
        dct[row.COMID] = (row.FCODE, row.FTYPE, row.GNIS_NAME, row.LENGTHKM, row.REACHCODE, row.geometry)
    logger.info('Finish creating simple flowline dictionary')
    return dct


def load_plusflow_file(filename: str) -> pd.DataFrame:
    logger.info('Begin loading plusflow file')
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
    logger.info('Finish loading plusflow file')
    return df


def create_simple_plusflow_dict(df: pd.DataFrame) -> dict:
    logger.info('Begin creating simple plusflow dictionary')
    dct = {}
    for row in df.itertuples():
        if row.FROMCOMID in dct.keys():
            dct[row.FROMCOMID].append(row.TOCOMID)
        else:
            dct[row.FROMCOMID] = [row.TOCOMID]
    dct.pop('0')
    logger.info('Finish creating simple plusflow dictionary')
    return dct


def create_digraph(flowline_dict: dict, plusflow_dict: dict) -> nx.DiGraph:
    logger.info('Begin creating digraph')
    dg = nx.DiGraph()
    for key in flowline_dict.keys():
        dg.add_node(key)
        dg.nodes[key]['fcode'] = flowline_dict[key][0]
        dg.nodes[key]['ftype'] = flowline_dict[key][1]
        dg.nodes[key]['gnis_name'] = flowline_dict[key][2]
        dg.nodes[key]['lengthkm'] = flowline_dict[key][3]
        dg.nodes[key]['reachcode'] = flowline_dict[key][4]
        dg.nodes[key]['geometry'] = flowline_dict[key][5]
    for key in plusflow_dict.keys():
        for val in plusflow_dict[key]:
            if key in flowline_dict.keys() and val in flowline_dict.keys() and val != '0':
                dg.add_edge(key, val)
    logger.info('Finish creating digraph')
    return dg


def count_by_degree(deg_list: list) -> dict:
    deg_counts = {}
    for node in deg_list:
        if node[1] not in deg_counts.keys():
            deg_counts[node[1]] = 1
        else:
            deg_counts[node[1]] += 1
    return dict(sorted(deg_counts.items()))


def print_digraph_stats(dg: nx.DiGraph):
    print()
    print(f'The digraph has {dg.number_of_nodes()} nodes.')
    print(f'The digraph has {dg.number_of_edges()} edges')
    print()
    print(f'Nodes by degree (degree, number of nodes): {count_by_degree(dg.degree)}')
    print(f'Nodes by in-degree (degree, number of nodes): {count_by_degree(dg.in_degree)}')
    print(f'Nodes by out-degree (degree, number of nodes): {count_by_degree(dg.out_degree)}')
    print()


def print_dictionary_stats(plusflow_dict: dict):
    counts = [0, 0, 0]
    for key in simple_plusflow_dict.keys():
        if len(simple_plusflow_dict[key]) == 1:
            counts[0] += 1
        elif len(simple_plusflow_dict[key]) == 2:
            counts[1] += 1
        elif len(simple_plusflow_dict[key]) == 3:
            counts[2] += 1
        else:
            print('COMID found with more than 3 downstream flowlines')
    print(f'The plusflow dictionary has {counts[0]} COMIDs with 1 downstream flowline')
    print(f'The plusflow dictionary has {counts[1]} COMIDs with 2 downstream flowlines')
    print(f'The plusflow dictionary has {counts[2]} COMIDs with 3 downstream flowlines')
    print(f'The plusflow dictionary has {counts[0] + counts[1] + counts[2]} COMIDs total')
    print()


def print_root_and_leaf_counts(dg: nx.DiGraph):
    roots = (v for v, d in dg.in_degree() if d == 0)
    leaves = (v for v, d in dg.out_degree() if d == 0)
    print(f'The digraph has {len(list(roots))} roots.')
    print(f'The digraph has {len(list(leaves))} leaves.')
    print()


def analyze_paths_from_source_to_outlet(dg: nx.DiGraph, src: str, out: str):
    haspath = nx.has_path(dg, source=src, target=out)
    if haspath:
        paths_list = []
        num_paths = 0
        for path in nx.all_simple_paths(dg, source=src, target=out):
            paths_list.append(path)
            num_paths += 1
        if num_paths > 1:
            print(f'There are {num_paths} paths from {src} to {out}')
        else:
            print(f'There is {num_paths} path from {src} to {out}')
    else:
        print(f'There is no path from {src} to {out}')
    path_count = 1
    for path in paths_list:
        print(f'   Path {path_count}: {len(path)} flowlines')
        path_count += 1
    print()


def initial_kg(_PREFIX):
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    logger.info('Begin initializing knowledge graph')
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    logger.info('Finish initializing knowledge graph')
    return graph


def build_iris(cid, _PREFIX):
    """

    :param cid:
    :param _PREFIX:
    :return:
    """
    flowlineIRI = _PREFIX['gcx-cid'][cid]
    flowlineGeoIRI = _PREFIX['gcx-cid'][cid + '.geometry']
    return flowlineIRI, flowlineGeoIRI


def triplify_huc_flowlines(dg):
    logger.info('BEGIN TRIPLIFICATION')
    kg = initial_kg(_PREFIX)
    logger.info('Begin creating triples')
    for node in dg.nodes(data=True):
        fl_iri, fl_geo_iri = build_iris(node[0], _PREFIX)
        kg.add((fl_iri, RDF.type, SDO.Place))
        kg.add((fl_iri, RDF.type, _PREFIX['hyf']['HY_FlowPath']))
        kg.add((fl_iri, RDF.type, _PREFIX['hyf']['HY_WaterBody']))

        kg.add((fl_geo_iri, RDF.type, GEO.Geometry))
        kg.add((fl_iri, GEO.defaultGeometry, fl_geo_iri))
        kg.add((fl_iri, GEO.hasGeometry, fl_geo_iri))
        kg.add((fl_geo_iri, GEO.asWKT, Literal(node[1]['geometry'], datatype=GEO.wktLiteral)))
        kg.add((fl_geo_iri, RDF.type, _PREFIX['sf']['LineString']))

        if not pd.isnull(node[1]['gnis_name']):
            kg.add((fl_iri, SDO.name, Literal(node[1]['gnis_name'], datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['saw_water']['hasCOMID'], Literal(str(node[0]), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['saw_water']['hasReachCode'], Literal(str(node[1]['reachcode']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['saw_water']['hasFTYPE'], Literal(str(node[1]['ftype']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['saw_water']['hasFCODE'], Literal(str(node[1]['fcode']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['wdp']['P2043'], Literal(node[1]['lengthkm'], datatype=XSD.float)))

        kg.add((fl_iri, _PREFIX['hyf']['downstreamWaterbody'], fl_iri))
        for key in dg.successors(node[0]):
            kg.add((fl_iri, _PREFIX['hyf']['downstreamWaterbody'], _PREFIX['gcx-cid'][key]))
    logger.info('Finish creating triples')
    logger.info('Begin writing triples to file')
    kg.serialize(main_ttl_file, format='turtle')
    logger.info('Finish writiing triples to file')
    logger.info('FINISH TRIPLIFICATION')


if __name__ == '__main__':
    start_time = time.time()
    df_flowline = load_flowline_file(flowline_file)
    simple_flowline_dict = create_simple_flowline_dict(df_flowline)
    df_plusflow = load_plusflow_file(plusflow_file)
    simple_plusflow_dict = create_simple_plusflow_dict(df_plusflow)
    G = create_digraph(simple_flowline_dict, simple_plusflow_dict)
    # print_digraph_stats(G)
    # print_dictionary_stats(simple_plusflow_dict)
    # print_root_and_leaf_counts(G)
    # analyze_paths_from_source_to_outlet(G, source_comid, outlet_comid)
    triplify_huc_flowlines(G)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    print(f'\nRuntime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')