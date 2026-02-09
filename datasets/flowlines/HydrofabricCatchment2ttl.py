"""Create a .ttl file of catchments referenced to flowlines from a .gpkg file

Under ### HUCxx VPU ###, enter
    a list of the VPU codes for the desired HUC2 regions (valid codes listed below)
Under ### INPUT Filenames ###, modify (if necessary)
    the name (and path) of the input .gpkg file (reference_catchments.gpkg)
Under ### OUTPUT Filename ###, modify (if necessary)
    the name (and path) of the main output .ttl file

Required:
    * geopandas
    * pandas
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, SDO, and XSD)
    * pathlib (Path)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * load_catchments_file - loads Hydrofabric catchments .gpkg as a GeoPandas geodataframe
    * get_vpu_catchments - creates a filtered versioin of the GeoPandas geodataframe with just a single VPU worth of catchments
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a flowline and its geometry
    * triplify_catchments - takes a digraph of NHDPlus v2 flowlines and creates a .ttl file representing the digraph
"""

import geopandas as gpd
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
vpunums = [ '01' ]
# vpunums = [ '10L', '11', '13', '14' ]
# Valid codes: 01, 02, 03N, 03S, 03W, 04, 05, 06, 07, 08, 09, 10U, 10L, 11, 12, 13, 14, 15, 16, 17, 18, 20

### INPUT Filenames ###
catchment_file = data_dir / f'Hydrofabric/reference_catchments.gpkg'

### OUTPUT Filenames ###
ttl_files = [ ]
for vpunum in vpunums:
    ttl_files.append(ttl_dir / f'hydrofabric_catchment_huc{vpunum}.ttl')

logname = log_dir / f'log_HydrofabricCatchment2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_catchments_file(filename: Path) -> gpd.GeoDataFrame:
    logger.info(f'Load catchments from {filename} to GeoDataFrame')
    gdf = gpd.read_file(filename, use_arrow=True)
    gdf['fid'] = gdf.index
    gdf[['fid', 'featureid']] = gdf[['fid', 'featureid']].astype(int).astype(str)
    return gdf


def get_vpu_catchments(vpunum: str, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    logger.info(f'Get HUC{vpunum} catchments')
    gdf = df[df.vpuid == vpunum]
    return gdf


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


def build_iris(cid, _PREFIX, max_id_length):
    """

    :param cid:
    :param _PREFIX:
    :return:
    """
    return _PREFIX['nhdplusv2'][f'd.Catchment.{cid}'], _PREFIX['nhdplusv2'][f'd.Catchment.{cid}.geometry']


def triplify_catchments(vpunum: str, df: gpd.GeoDataFrame, outfile: str, max_id_length = 7):
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    logger.info(f'Triplify HUC{vpunum} catchments')
    for row in df.itertuples():
        # Get IRIs for the current Hydrofabric catchment and its geometry
        fl_iri, fl_geo_iri = build_iris(row.fid.zfill(max_id_length), _PREFIX, max_id_length)

        # Instantiate the current NHDFlowline
        kg.add((fl_iri, RDF.type, _PREFIX['hyf']['HY_DendriticCatchment']))

        # Triplify the geometry for the current NHDFlowline
        kg.add((fl_geo_iri, RDF.type, GEO.Geometry))
        kg.add((fl_iri, GEO.defaultGeometry, fl_geo_iri))
        kg.add((fl_iri, GEO.hasGeometry, fl_geo_iri))
        kg.add((fl_geo_iri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))

        # Triplify current catchment attributes
        kg.add((fl_iri, _PREFIX['nhdplusv2']['hasCatchmentId'], Literal(row.fid.zfill(max_id_length), datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['containsFlowline'], Literal(row.featureid, datatype=XSD.string)))
        kg.add((fl_iri, _PREFIX['nhdplusv2']['inVPU'], Literal(row.vpuid, datatype=XSD.string)))
    logger.info(f'Write HUC{vpunum} catchment triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: HUC/VPU set = {vpunums}')
    df_catchments = load_catchments_file(catchment_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    for vpunum, outfile in zip(vpunums, ttl_files):
        start_time = time.time()
        logger.info('')
        logger.info(f'Processing HUC/VPU {vpunum}')
        df_vpu = get_vpu_catchments(vpunum, df_catchments)
        triplify_catchments(vpunum, df_vpu, outfile)
        logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
