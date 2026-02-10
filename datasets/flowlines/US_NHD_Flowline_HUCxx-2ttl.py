"""Create a .ttl file of flowlines and their connectivity from a .shp file and a .dbf file

Under ### HUCxx VPU ###, enter
    the VPU code for the current HUC2 region (valid codes listed below)
Under ### INPUT Filenames ###, modify (if necessary)
    the name (and path) of the input .shp file (NHDFlowline)
    the name (and path) of the input .dbf file (PlusFlow)
Under ### OUTPUT Filename ###, modify (if necessary)
    the name (and path) of the main output .ttl file

Required:
    * simpledbf (DBf5)
    * geopandas
    * pandas
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, SDO, and XSD)
    * networkx
    * pathlib (Path)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * load_flowline_file - loads a .shp file of NHDPlus v2 flowlines as a GeoPandas geodataframe
    * create_simple_flowline_dict - takes a Pandas dataframe of NHDPlus v2 flowline data and creates a dictionary where
                                    a flowline COMID is a key and values are a triple of flowline attributes
    * load_plusflow_file - loads a .dbf file of NHDPlus v2 PlusFlow attributes as a Pandas dataframe
    * create_simple_plusflow_dict - takes a Pandas dataframe of NHDPlus v2 PlusFlow data and creates a dictionary where
                                    a flowline COMID is a key and values are a list of connected downstream flowlines
    * create_digraph - takes a flowline dictionary and a PlusFlow dictionary and returns a directed graph
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a flowline and its geometry
    * triplify_huc_flowlines - takes a digraph of NHDPlus v2 flowlines and creates a .ttl file representing the digraph
    * count_by_degree - takes a DegreeView object and returns a dictionary of degrees (key) and counts (values)
    * print_digraph_stats - takes a digraph and prints a set of statistics describing its structure
    * print_dictionary_stats - takes a dictionary of PlusFlow data and prints statistics about flowline connectivity
    * print_root_and_leaf_counts - takes a digraph and prints counts of root nodes and leaf nodes
    * analyze_paths_from_source_to_outlet - takes a digraph and two nodes (COMIDs) and prints the number of paths
                                            connecting the nodes and the length of each such path
"""

from simpledbf import Dbf5
import geopandas as gpd
import shapely
import pandas as pd
import networkx as nx
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
vpunum = '10L'
# Valid codes: 01, 02, 03N, 03S, 03W, 04, 05, 06, 07, 08, 09, 10U, 10L, 11, 12, 13, 14, 15, 16, 17, 18, 20

### INPUT Filenames ###
plusflow_file = data_dir / f'NHDFlowline/HUC{vpunum}_PlusFlow.dbf'
flowline_file = data_dir / f'NHDFlowline/HUC{vpunum}_NHDFlowline.shp'

### OUTPUT Filename ###
main_ttl_file = ttl_dir / f'us_nhd_flowline_huc{vpunum}.ttl'

logname = log_dir / f'log_US_NHD_Flowline_HUCxx-2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_flowline_file(filename: str) -> gpd.GeoDataFrame:
    logger.info(f'Load HUC{vpunum} flowline shapefile from {filename}')
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
    return gdf


def create_simple_flowline_dict(df: pd.DataFrame) -> dict:
    logger.info(f'Create simple flowline dictionary for HUC{vpunum}')
    dct = {}
    for row in df.itertuples():
        dct[row.COMID] = (row.FCODE, row.FTYPE, row.GNIS_NAME, row.LENGTHKM, row.REACHCODE, row.geometry)
    return dct


def load_plusflow_file(filename: str) -> pd.DataFrame:
    logger.info(f'Load HUC{vpunum} plusflow file from {filename}')
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
    return df


def create_simple_plusflow_dict(df: pd.DataFrame) -> dict:
    logger.info(f'Create simple plusflow dictionary for HUC{vpunum}')
    dct = {}
    for row in df.itertuples():
        if row.FROMCOMID in dct.keys():
            dct[row.FROMCOMID].append(row.TOCOMID)
        else:
            dct[row.FROMCOMID] = [row.TOCOMID]
    dct.pop('0')
    return dct


def create_digraph(flowline_dict: dict, plusflow_dict: dict) -> nx.DiGraph:
    logger.info(f'Create and populate networkx DiGraph representing HUC{vpunum} flowline network')
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
    for key in plusflow_dict.keys():
        if len(plusflow_dict[key]) == 1:
            counts[0] += 1
        elif len(plusflow_dict[key]) == 2:
            counts[1] += 1
        elif len(plusflow_dict[key]) == 3:
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
    paths_list = []
    haspath = nx.has_path(dg, source=src, target=out)
    if haspath:
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
    logger.info('Initialize RDFLib Graph')
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
    flowline_iri = _PREFIX['gcx_cid'][cid]
    flowline_geo_iri = _PREFIX['gcx_cid'][cid + '.geometry']
    flowline_length_iri = _PREFIX['gcx_cid'][cid + '.flowPathLength']
    flowline_quantval_iri = _PREFIX['gcx_cid'][cid + '.flowPathLength.quantityValue']
    return flowline_iri, flowline_geo_iri, flowline_length_iri, flowline_quantval_iri


def triplify_huc_flowlines(dg):
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    logger.info(f'Triplify HUC{vpunum} flowlines')
    for node in dg.nodes(data=True):
        # Get IRIs for the current NHDFlowline, its geometry, its length object, and the length's qudt:QuantityValue
        fl_iri, fl_geo_iri, fl_len_iri, fl_qv_iri = build_iris(node[0], _PREFIX)

        # Instantiate the current NHDFlowline
        kg.add((fl_iri, RDF.type, _PREFIX['nhdplusv2']['FlowLine']))

        # Triplify the geometry for the current NHDFlowline
        kg.add((fl_geo_iri, RDF.type, GEO.Geometry))
        kg.add((fl_iri, GEO.defaultGeometry, fl_geo_iri))
        kg.add((fl_iri, GEO.hasGeometry, fl_geo_iri))
        kg.add((fl_geo_iri, GEO.asWKT, Literal(node[1]['geometry'], datatype=GEO.wktLiteral)))

        # Triplify current NHDFlowline attributes
        if not pd.isnull(node[1]['gnis_name']):
            kg.add((fl_iri, SDO.name, Literal(node[1]['gnis_name'], datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasCOMID'], Literal(str(node[0]), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasReachCode'], Literal(str(node[1]['reachcode']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['wbd']['containingHUC'], _PREFIX['wbd_data']['d.HUC8.' + str(node[1]['reachcode'][:8])]))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasFTYPE'], Literal(str(node[1]['ftype']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasFCODE'], Literal(str(node[1]['fcode']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasFlowPathLength'], fl_len_iri))
        kg.add((fl_len_iri, RDF.type, _PREFIX['nhdplusv2']['FlowPathLength']))
        kg.add((fl_len_iri, _PREFIX['qudt']['quantityValue'], fl_qv_iri))
        kg.add((fl_qv_iri, RDF.type, _PREFIX['qudt']['QuantityValue']))
        kg.add((fl_qv_iri, _PREFIX['qudt']['numericValue'], Literal(node[1]['lengthkm'], datatype=XSD.decimal)))
        kg.add((fl_qv_iri, _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['KiloM']))

        # Triplify the downstream connectivity, including a reflexive statement for the current NHDFlowline
        kg.add((fl_iri, _PREFIX['nhdplusv2']['downstreamFlowPath'], fl_iri))
        for key in dg.successors(node[0]):
            kg.add((fl_iri, _PREFIX['nhdplusv2']['downstreamFlowPath'], _PREFIX['gcx_cid'][key]))
    logger.info(f'Write HUC{vpunum} flowline triples to {main_ttl_file}')
    kg.serialize(main_ttl_file, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: HUC/VPU = {vpunum}')
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