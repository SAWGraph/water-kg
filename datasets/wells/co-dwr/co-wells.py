"""Create a .ttl file of water wells in Colorado

Under ### file paths ###, modify (if necessary)
    the name (and path) of the input .zip file for well permit applications in Colorado
The output file ...

Required:
    *

Functions:
    *
"""

from datetime import date, datetime, timedelta
import geopandas as gpd
import logging
import pandas as pd
from pathlib import Path

from pandocfilters import Null
from rdflib.namespace import RDF, RDFS, XSD
from rdflib import Graph, Literal, Namespace, URIRef
from shapely import is_valid, is_valid_reason, wkt
import sys
import time

## Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent.parent
data_dir = cwd.parent.parent / 'data/CO_groundwater'
ttl_dir = cwd / 'ttl_files'
log_dir = cwd / 'logs'
# print(f"Current working directory:      {cwd}")
# print(f"Github repos and namespaces.py: {ns_dir}")
# print(f"Data (input) directory:         {data_dir}")
# print(f"Turtle (output) directory:      {ttl_dir}")
# print(f"Logging directory:              {log_dir}")

# Modify the system path to find namespaces.py
sys.path.insert(0, str(ns_dir))
from namespaces import _PREFIX

## INPUT Filename ###
wells_file = data_dir / 'WellPermitPublic.zip'
epsg_in = 26913
epsg_out = 4326

### OUTPUT Filename ###
output_file = ttl_dir / 'co-dwr_wells.ttl'

logname = log_dir / f"log_co-wells.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_wells(filename: str, epsg_in: int, epsg_out: int) -> gpd.GeoDataFrame:
    logger.info(f'Load shapefile to GeoDataFrame')
    gdf = gpd.read_file(f'zip://{filename}')
    logger.info(f'Convert CRS from EPSG:{epsg_in} to EPSG:{epsg_out}')
    gdf.set_crs(epsg=epsg_in, inplace=True)
    gdf.to_crs(epsg=epsg_out, inplace=True)
    return gdf


def initial_kg(_PREFIX: dict) -> Graph:
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    logger.info('Intialize RDFLib Graph')
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def build_iris(well_id: str, _PREFIX: dict) -> tuple:
    well_id = '_'.join(well_id.split())
    return (_PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}'],
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.geometry'],
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.depth'],
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.depth.QV'],
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.yield'],
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.yield.QV'])


def triplify_well_data(gdf: gpd.GeoDataFrame, _PREFIX: dict) -> None:
    kg = initial_kg(_PREFIX)
    logger.info(f'Triplify well data')
    for row in gdf.itertuples():
        well_iri, geom_iri, depth_iri, depth_qv_iri, yield_iri, yield_qv_iri = build_iris(row.Receipt, _PREFIX)
        kg.add((well_iri, RDF.type, _PREFIX['co_dwr']['CODWR-Well']))
        kg.add((well_iri, RDFS['label'], Literal(row.Receipt, datatype=XSD.string)))
        kg.add((well_iri, _PREFIX['co_dwr']['moreInfo'], Literal(row.MoreInfo, datatype=XSD.anyURI)))
        if isinstance(row.CurrStatus, str):
            kg.add((well_iri,
                    _PREFIX['co_dwr']['hasStatus'],
                    _PREFIX['co_dwr'][f'CODWR-WellStatus.{''.join(row.CurrStatus.split())}']))
        if isinstance(row.LocAccurac, str):
            kg.add((well_iri,
                    _PREFIX['co_dwr']['locAccuracy'],
                    _PREFIX['co_dwr'][f'CODWR-LocAccuracy.{''.join(row.LocAccurac.split())}']))
        if isinstance(row.Use1, str):
            kg.add((well_iri,
                    _PREFIX['co_dwr']['hasWaterUse'],
                    _PREFIX['co_dwr'][f'CODWR-WaterUse.{''.join(row.Use1.split())}']))
        if isinstance(row.Aquifer1, str):
            kg.add((well_iri,
                    _PREFIX['co_dwr']['drawsFromAquifer'],
                    _PREFIX['co_dwr'][f'CODWR-Aquifer.{''.join(row.Aquifer1.split())}']))
        if row.WellDepth > 0:
            kg.add((well_iri, _PREFIX['co_dwr']['hasDepth'], depth_iri))
            kg.add((depth_iri, RDF.type, _PREFIX['co_dwr']['CODWR-WellDepth']))
            kg.add((depth_iri, _PREFIX['qudt']['quantityValue'], depth_qv_iri))
            kg.add((depth_qv_iri, RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((depth_qv_iri, _PREFIX['qudt']['numericValue'], Literal(row.WellDepth, datatype=XSD.integer)))
            kg.add((depth_qv_iri, _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
        if row.Yield > 0:
            kg.add((well_iri, _PREFIX['co_dwr']['hasYield'], yield_iri))
            kg.add((yield_iri, RDF.type, _PREFIX['co_dwr']['CODWR-WellYield']))
            kg.add((yield_iri, _PREFIX['qudt']['quantityValue'], yield_qv_iri))
            kg.add((yield_qv_iri, RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((yield_qv_iri, _PREFIX['qudt']['numericValue'], Literal(row.Yield, datatype=XSD.integer)))
            kg.add((yield_qv_iri, _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['GAL_US-PER-MIN']))
        kg.add((well_iri, _PREFIX['geo']['hasGeometry'], geom_iri))
        kg.add((well_iri, _PREFIX['geo']['defaultGeometry'], geom_iri))
        kg.add((geom_iri, _PREFIX["geo"]["asWKT"], Literal(row.geometry, datatype=_PREFIX['geo']['wktLiteral'])))
        kg.add((geom_iri, RDF.type, _PREFIX['geo']['Geometry']))
    logger.info(f'Write triples to {output_file}')
    kg.serialize(output_file, format='turtle')


if __name__ == "__main__":
    start_time = time.time()
    logger.info(f'Launching Colorado wells script')
    gdf = load_wells(wells_file, epsg_in, epsg_out)
    triplify_well_data(gdf, _PREFIX)
    logger.info(f'Processing complete in {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
