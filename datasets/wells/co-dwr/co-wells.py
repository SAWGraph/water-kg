"""Create a .ttl file of water wells in Colorado

Under ### file paths ###, modify (if necessary)
    the name (and path) of the input .zip file for well permit applications in Colorado
The output file ...

Required:
    *

Functions:
    *
"""

from datetime import date, timedelta
import geopandas as gpd
import logging
import pandas as pd
from pathlib import Path
from rdflib.namespace import OWL, RDF, RDFS, XSD
from rdflib import Graph, Literal, URIRef
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
ontologyIRI = URIRef('http://sawgraph.spatialai.org/v1/co-dwr-data')

## INPUT Filename ###
inputtype = 'shp'
wells_file_shp = data_dir / 'WellPermitPublic.zip'
wells_file_csv = data_dir / 'DWR_Well_Application_Permit_20260708.csv'
epsg_shp = 26913
epsg_csv = 4326
epsg_out = 4326

### OUTPUT Filename ###
output_file_shp = ttl_dir / 'co-dwr_wells_from-shp.ttl'
output_file_csv = ttl_dir / 'co-dwr_wells_from-csv.ttl'

logname = log_dir / f'log_co-wells.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_wells_shp(filename: Path, epsg_shp: int, epsg_out: int) -> gpd.GeoDataFrame:
    logger.info(f'Load shapefile to GeoDataFrame')
    gdf = gpd.read_file(f'zip://{filename}')
    logger.info(f'Convert CRS from EPSG:{epsg_shp} to EPSG:{epsg_out}')
    gdf.set_crs(epsg=epsg_shp, inplace=True)
    gdf.to_crs(epsg=epsg_out, inplace=True)
    return gdf


def load_wells_csv(filename: Path, epsg_csv: int, epsg_out: int) -> gpd.GeoDataFrame:
    logger.info(f'Load select csv columns to DataFrame')
    select_columns = ['Receipt', 'Current Status', 'Latitude', 'Longitude', 'Location Accuracy', 'Associated Aquifers',
                      'Associated Uses', 'Well Depth', 'Yield', 'Static Water Level', 'More Information', 'IDKey']
    new_columns = {'Current Status': 'CurrStatus', 'Location Accuracy': 'LocAccurac', 'Associated Aquifers': 'Aquifer1',
                   'Associated Uses': 'Use1', 'Well Depth': 'WellDepth', 'Static Water Level': 'StaticWL',
                   'More Information': 'MoreInfo'}
    df = pd.read_csv(filename, usecols=select_columns)
    logger.info(f'Convert DataFrame to GeoDataFrame, rename columns, and convert CRS to {epsg_out} if necessary')
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs=f'EPSG:{str(epsg_csv)}')
    gdf = gdf.rename(columns=new_columns)
    if epsg_csv != epsg_out:
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
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.yield.QV'],
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.staticwaterlevel'],
            _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.staticwaterlevel.QV'])


def get_well_status(status: str) -> str:
    if 'pump' in status.lower():
        if 'expired' in status.lower():
            return ''.join(status.split()).replace('(', '').replace(')', '')
        elif 'without' in status.lower():
            return ''.join(status.split()).replace('inWellWithouta', 'Without')
        else:
            return ''.join(status.split()).replace(',', '').replace('Received', '')
    return '.'.join(status.split(' - ')).replace(' ', '')


def get_loc_accuracy(accuracy: str) -> str:
    return ''.join(accuracy.title().split())


def add_provenance(kg: Graph) -> Graph:
    kg.add((ontologyIRI, RDF.type, OWL.Ontology))
    kg.add((ontologyIRI, _PREFIX['dcterms']['issued'], Literal(date.today().isoformat(), datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['dcterms']['modified'], Literal(date.today().isoformat(), datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['prov']['wasDerivedFrom'], _PREFIX['co_dwr']['sourceDataset']))
    kg.add((ontologyIRI, OWL.versionInfo, Literal('0.1', datatype=XSD.string)))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], RDF.type, _PREFIX['stad']['Dataset']))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], RDFS.label, Literal('CO DWR Well Application Permits', datatype=XSD.string)))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['dcterms']['issued'], Literal('2026-07-07', datatype=XSD.date)))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['dcterms']['source'], URIRef('https://data.colorado.gov/Water/DWR-Well-Application-Permit/wumm-7awb/data_preview')))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['dcterms']['source'], URIRef('https://cdss.colorado.gov/gis-data/gis-data-by-category')))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['stad']['hasSpatialCoverage'], _PREFIX['kwgr']['admininstrativeRegion.USA.08']))
    return kg


def triplify_well_data(gdf: gpd.GeoDataFrame, _PREFIX: dict, inputtype: str) -> None:
    kg = initial_kg(_PREFIX)
    logger.info(f'Triplify well data')
    kg = add_provenance(kg)
    for row in gdf.itertuples():
        if inputtype.lower() == 'shp':
            well_iri, geom_iri, depth_iri, depth_qv_iri, yield_iri, yield_qv_iri, swl_iri, swl_qv_iri = build_iris(str(row.Receipt), _PREFIX)
            kg.add((well_iri, RDFS.label, Literal(row.Receipt, datatype=XSD.string)))
        else:
            well_iri, geom_iri, depth_iri, depth_qv_iri, yield_iri, yield_qv_iri, swl_iri, swl_qv_iri = build_iris(str(row.IDKey), _PREFIX)
            kg.add((well_iri, RDFS.label, Literal(row.IDKey, datatype=XSD.string)))
        kg.add((well_iri, RDF.type, _PREFIX['co_dwr']['CODWR-Well']))
        kg.add((well_iri, _PREFIX['co_dwr']['hasReceipt'], Literal(row.Receipt, datatype=XSD.string)))
        kg.add((well_iri, RDFS.isDefinedBy, ontologyIRI))
        kg.add((well_iri, RDFS.label, Literal(row.Receipt, datatype=XSD.string)))
        kg.add((well_iri, RDFS.seeAlso, Literal(row.MoreInfo, datatype=XSD.anyURI)))
        if isinstance(row.CurrStatus, str):
            kg.add((well_iri,
                    _PREFIX['hyfo']['hasWellStatus'],
                    _PREFIX['co_dwr'][f'CODWR-WellStatus.{get_well_status(row.CurrStatus)}']))
        if isinstance(row.LocAccurac, str):
            kg.add((well_iri,
                    _PREFIX['co_dwr']['locAccuracy'],
                    _PREFIX['co_dwr'][f'CODWR-LocAccuracy.{get_loc_accuracy(row.LocAccurac)}']))
        if isinstance(row.Use1, str):
            kg.add((well_iri,
                    _PREFIX['hyfo']['hasWaterUse'],
                    Literal(row.Use1, datatype=XSD.string)))
        if isinstance(row.Aquifer1, str):
            kg.add((well_iri,
                    _PREFIX['co_dwr']['hasAquifer'],
                    Literal(row.Aquifer1, datatype=XSD.string)))
        if row.WellDepth > 0:
            kg.add((well_iri, _PREFIX['hyfo']['hasTotalDepth'], depth_iri))
            kg.add((depth_iri, RDF.type, _PREFIX['co_dwr']['CODWR-WellDepth']))
            kg.add((depth_iri, _PREFIX['qudt']['quantityValue'], depth_qv_iri))
            kg.add((depth_qv_iri, RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((depth_qv_iri, _PREFIX['qudt']['numericValue'], Literal(row.WellDepth, datatype=XSD.integer)))
            kg.add((depth_qv_iri, _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
        if row.Yield > 0:
            kg.add((well_iri, _PREFIX['hyfo']['hasYield'], yield_iri))
            kg.add((yield_iri, RDF.type, _PREFIX['co_dwr']['CODWR-WellYield']))
            kg.add((yield_iri, _PREFIX['qudt']['quantityValue'], yield_qv_iri))
            kg.add((yield_qv_iri, RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((yield_qv_iri, _PREFIX['qudt']['numericValue'], Literal(row.Yield, datatype=XSD.decimal)))
            kg.add((yield_qv_iri, _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['GAL_US-PER-MIN']))
        if row.StaticWL > 0:
            kg.add((well_iri, _PREFIX['hyfo']['hasStaticWaterDepth'], swl_iri))
            kg.add((swl_iri, RDF.type, _PREFIX['co_dwr']['CODWR-StaticWaterLevel']))
            kg.add((swl_iri, _PREFIX['qudt']['quantityValue'], swl_qv_iri))
            kg.add((swl_qv_iri, RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((swl_qv_iri, _PREFIX['qudt']['numericValue'], Literal(row.StaticWL, datatype=XSD.integer)))
            kg.add((swl_qv_iri, _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
        kg.add((well_iri, _PREFIX['geo']['hasGeometry'], geom_iri))
        kg.add((well_iri, _PREFIX['geo']['defaultGeometry'], geom_iri))
        kg.add((geom_iri, _PREFIX["geo"]["asWKT"], Literal(row.geometry, datatype=_PREFIX['geo']['wktLiteral'])))
        kg.add((geom_iri, RDF.type, _PREFIX['geo']['Geometry']))
    if inputtype.lower() == 'shp':
        logger.info(f'Write triples to {output_file_shp}')
        kg.serialize(output_file_shp, format='turtle')
    else:
        logger.info(f'Write triples to {output_file_csv}')
        kg.serialize(output_file_csv, format='turtle')


if __name__ == "__main__":
    start_time = time.time()
    if inputtype.lower() == 'shp':
        logger.info(f'Process Colorado wells shapefile')
        gdf = load_wells_shp(wells_file_shp, epsg_shp, epsg_out)
        triplify_well_data(gdf, _PREFIX, inputtype.lower())
    else:
        logger.info(f'Process Colorado wells csv file')
        gdf = load_wells_csv(wells_file_csv, epsg_csv, epsg_out)
        triplify_well_data(gdf, _PREFIX, inputtype.lower())
    logger.info(f'Processing complete in {str(timedelta(seconds=time.time() - start_time))} HMS')
