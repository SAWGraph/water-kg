"""Create a .ttl file of flowlines and their connectivity from a .gpkg file

Under ### HUCxx VPU ###, enter
    a list of the VPU codes for the desired HUC2 regions (valid codes listed below)
Under ### INPUT Filenames ###, modify (if necessary)
    the name (and path) of the input .gpkg file (reference_flowline.gpkg)
Under ### OUTPUT Filename ###, modify (if necessary)
    the name (and path) of the main output .ttl file

Required:
    * geopandas
    * pandas
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, SDO, and XSD)
    * networkx
    * pathlib (Path)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * load_flowline_file - loads a .shp file of NHDPlus v2 flowlines as a GeoPandas geodataframe
    * get_mainstem_lookup_table - loads crosswalk from LevelPathIDs to MainStem IDs
    * create_digraph - takes a flowline dictionary and a PlusFlow dictionary and returns a directed graph
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a flowline and its geometry
    * triplify_huc_flowlines - takes a digraph of NHDPlus v2 flowlines and creates a .ttl file representing the digraph
"""

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
# vpunums = [ '01' ]
vpunums = [ '01', '10L', '11', '13', '14' ]
# Valid codes: 01, 02, 03N, 03S, 03W, 04, 05, 06, 07, 08, 09, 10U, 10L, 11, 12, 13, 14, 15, 16, 17, 18, 20

### INPUT Filenames ###
flowline_file = data_dir / f'Hydrofabric/reference_flowline.gpkg'
mainstem_lookup_url = 'https://github.com/internetofwater/ref_rivers/releases/download/v2.1/mainstem_lookup.csv'

### OUTPUT Filenames ###
ttl_files = [ ]
for vpunum in vpunums:
    ttl_files.append(ttl_dir / f'hydrofabric_flowline_huc{vpunum}.ttl')

logname = log_dir / f'log_HydrofabricFlowline2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_flowline_file(filename: Path) -> gpd.GeoDataFrame:
    logger.info(f'Load flowlines from {filename} to GeoDataFrame')
    flowline_columns = [ 'COMID', 'REACHCODE', 'LevelPathI', 'toCOMID', 'TerminalFl', 'Divergence', 'FCODE', 'FTYPE',
                         'LENGTHKM', 'slope', 'gnis_name', 'gnis_id', 'VPUID', 'wbareatype', 'WBAREACOMI' ]
    gdf = gpd.read_file(filename, columns=flowline_columns, use_arrow=True)
    gdf = gdf[gdf.FTYPE != 'Coastline']
    gdf[['COMID', 'LevelPathI', 'toCOMID', 'WBAREACOMI']] = gdf[['COMID', 'LevelPathI', 'toCOMID', 'WBAREACOMI']].astype(int).astype(str)
    # print(gdf.columns)
    # for row in gdf.itertuples():
    #     gdf._set_value(row.Index, 'geometry', shapely.wkb.loads(shapely.wkb.dumps(row.geometry, output_dimension=2)))
    return gdf


def get_vpu_flowlines(vpunum: str, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    logger.info(f'Get HUC{vpunum} flowlines')
    gdf = df[df.VPUID == vpunum]
    return gdf


def get_mainstem_lookup_table(url: str) -> pd.DataFrame:
    logger.info(f'Get mainstem lookup table from {url}')
    return gpd.read_file(url)


def create_digraph(df: gpd.GeoDataFrame) -> nx.DiGraph:
    logger.info(f'Create and populate networkx DiGraph representing HUC{vpunum} flowline network')
    dg = nx.DiGraph()
    for row in df.itertuples():
        dg.add_node(row.COMID)
        dg.nodes[row.COMID]['reachcode'] = row.REACHCODE
        dg.nodes[row.COMID]['levelpathi'] = row.LevelPathI
        if row.TerminalFl != '1':
            dg.add_edge(row.COMID, row.toCOMID)
        dg.nodes[row.COMID]['terminalfl'] = row.TerminalFl
        if row.Divergence > 0:
            if row.Divergence == 1:
                dg.nodes[row.COMID]['divergence'] = 'minor-path'
            elif row.Divergence == 2:
                dg.nodes[row.COMID]['divergence'] = 'main-path'
            else:
                dg.nodes[row.COMID]['divergence'] = 'unexpected-value-at-import'
        dg.nodes[row.COMID]['fcode'] = row.FCODE
        dg.nodes[row.COMID]['ftype'] = row.FTYPE
        dg.nodes[row.COMID]['lengthkm'] = row.LENGTHKM
        dg.nodes[row.COMID]['slope'] = row.slope
        dg.nodes[row.COMID]['gnis_name'] = row.gnis_name
        dg.nodes[row.COMID]['gnis_id'] = row.gnis_id
        dg.nodes[row.COMID]['vpuid'] = row.VPUID
        dg.nodes[row.COMID]['wbareatype'] = row.wbareatype
        dg.nodes[row.COMID]['wbareacomi'] = row.WBAREACOMI
        dg.nodes[row.COMID]['geometry'] = row.geometry
    return dg


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


def triplify_huc_flowlines(vpunum: str, dg: nx.DiGraph, outfile: str):
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    mainstem_csv = get_mainstem_lookup_table(mainstem_lookup_url)
    logger.info(f'Triplify HUC{vpunum} flowlines')
    for node in dg.nodes(data=True):
        if 'geometry' not in dg.nodes[node[0]]:
            logger.info(f'COMID {node[0]} in HUC{vpunum} has no geometry')
            continue
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
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasCOMID'], Literal(str(node[0]), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasReachCode'], Literal(str(node[1]['reachcode']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['wbd']['containingHUC'], _PREFIX['wbd_data']['d.HUC8.' + str(node[1]['reachcode'][:8])]))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasLevelPathId'], Literal(node[1]['levelpathi'], datatype=XSD.string)))
        if str(node[1]['levelpathi']) in mainstem_csv['lp_mainstem'].values:
            msid = mainstem_csv.loc[mainstem_csv["lp_mainstem"] == str(node[1]['levelpathi'])]["ref_mainstem_id"].iloc[0]
            kg.add((fl_iri, _PREFIX['nhdplusv2']['hasMainStemId'], Literal(msid, datatype=XSD.string)))
            kg.add((fl_iri, _PREFIX['nhdplusv2']['hasMainStem'], _PREFIX['gcx_ms'][msid]))
        if 'divergence' in dg.nodes[node[0]]:
            kg.add((fl_iri, _PREFIX['nhdplusv2']['divergence'], Literal(node[1]['divergence'], datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasFCODE'], Literal(str(node[1]['fcode']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasFTYPE'], Literal(str(node[1]['ftype']), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasFlowPathLength'], fl_len_iri))
        if node[1]['slope'] > -9998:
            slope_str = f'{node[1]['slope']:.20f}'.rstrip('0').rstrip('.')
            kg.add((fl_iri, _PREFIX['nhdplusv2']['hasSlope'], Literal(slope_str, datatype=XSD.decimal)))
        if not pd.isnull(node[1]['gnis_name']) and node[1]['gnis_name'] != '':
            kg.add((fl_iri, SDO.name, Literal(node[1]['gnis_name'], datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['inVPU'], Literal(str(node[1]['vpuid']), datatype=XSD.string)))
        if int(node[1]['wbareacomi']) > 0:
            kg.add((fl_iri, _PREFIX['nhdplusv2']['wbAreaHasCOMID'], Literal(node[1]['wbareacomi'], datatype=XSD.string)))
        if len(node[1]['wbareatype']) > 0:
            kg.add((fl_iri, _PREFIX['nhdplusv2']['wbAreaHasType'], Literal(node[1]['wbareatype'], datatype=XSD.string)))

        kg.add((fl_len_iri, RDF.type, _PREFIX['nhdplusv2']['FlowPathLength']))
        kg.add((fl_len_iri, _PREFIX['qudt']['quantityValue'], fl_qv_iri))
        kg.add((fl_qv_iri, RDF.type, _PREFIX['qudt']['QuantityValue']))
        kg.add((fl_qv_iri, _PREFIX['qudt']['numericValue'], Literal(node[1]['lengthkm'], datatype=XSD.decimal)))
        kg.add((fl_qv_iri, _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['KiloM']))

        # Triplify the downstream connectivity, including a reflexive statement for the current NHDFlowline
        kg.add((fl_iri, _PREFIX['nhdplusv2']['downstreamFlowPath'], fl_iri))
        for key in dg.successors(node[0]):
            kg.add((fl_iri, _PREFIX['nhdplusv2']['downstreamFlowPath'], _PREFIX['gcx_cid'][key]))
    logger.info(f'Write HUC{vpunum} flowline triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: HUC/VPU set = {vpunums}')
    df_flowlines = load_flowline_file(flowline_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    for vpunum, outfile in zip(vpunums, ttl_files):
        start_time = time.time()
        logger.info('')
        logger.info(f'Processing HUC/VPU {vpunum}')
        df_vpu = get_vpu_flowlines(vpunum, df_flowlines)
        G = create_digraph(df_vpu)
        triplify_huc_flowlines(vpunum, G, outfile)
        logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
