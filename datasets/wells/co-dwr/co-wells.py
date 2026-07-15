from datetime import timedelta
import geopandas as gpd
import logging
import pandas as pd
from pathlib import Path
from rdflib.namespace import OWL, RDF, RDFS, XSD
from rdflib import Graph, Literal, URIRef
from sodapy import Socrata
import sys
import time

## Variables
inputtype = 'api' # api, csv, or shp - preferred in that order (note: shp does not offer a unique key)
ttl_issued_date = '2026-07-08'
ttl_modified_date = '2026-07-08'
ttl_version = '0.1'
date_issued_date = '2026-07-08'

## Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent.parent
data_dir = cwd.parent.parent / 'data/CO_groundwater'
ttl_dir = cwd / 'ttl_files'
log_dir = cwd / 'logs'

# Modify the system path to find namespaces.py
sys.path.insert(0, str(ns_dir))
from namespaces import _PREFIX
ontologyIRI = URIRef('http://sawgraph.spatialai.org/v1/co-dwr-data')

## INPUT Filename ###
wells_file_shp = data_dir / 'WellPermitPublic.zip'
wells_file_csv = data_dir / 'DWR_Well_Application_Permit_20260708.csv' # Preferred due to unique IDKey field
api_domain = 'data.colorado.gov'
api_dataset = 'wumm-7awb'
epsg_shp = 26913
epsg_csv = 4326
epsg_out = 4326

### OUTPUT Filename ###
output_file_shp = ttl_dir / 'co-dwr_wells_from-shp.ttl'
output_file_csv = ttl_dir / 'co-dwr_wells_from-csv.ttl'
output_file_api = ttl_dir / 'co-dwr_wells_from-api.ttl'

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
    df = pd.read_csv(filename)
    return df_from_csv_to_gdf(df, epsg_csv, epsg_out)


def load_wells_api(domain: str, dataset: str, epsg_in: int, epsg_out: int) -> gpd.GeoDataFrame:
    logger.info(f'Download wells from API endpoint to DataFrame')
    client = Socrata(domain, None)
    limit = 1000 # API default limit
    offset = 0
    logging_interval = 50000
    all_data = []
    while True:
        if offset % logging_interval == 0:
            logger.info(f'    Pulling rows {offset+1:,} to {offset + logging_interval:,} from API')
        results = client.get(dataset, limit=limit, offset=offset)
        if len(results) == 0:
            logger.info(f'{offset - limit + all_data[-1].shape[0]:,} rows pulled from API')
            break
        temp_df = pd.DataFrame(results)
        all_data.append(temp_df)
        offset += limit
    df = pd.concat(all_data, ignore_index=True)
    return df_from_csv_to_gdf(df, epsg_in, epsg_out)


def df_from_csv_to_gdf(df: pd.DataFrame, epsg_in: int, epsg_out: int) -> gpd.GeoDataFrame:
    logger.info(f'Convert DataFrame to GeoDataFrame (EPSG:{epsg_out})')
    select_columns = ['receipt',
                      'current_status',
                      'latitude',
                      'longitude',
                      'location_accuracy',
                      'associated_aquifers',
                      'associated_uses',
                      'well_depth',
                      'yield',
                      'static_water_level',
                      'more_information',
                      'idkey']
    new_columns = {'receipt': 'Receipt',
                   'current_status': 'CurrStatus',
                   'latitude': 'Latitude',
                   'longitude': 'Longitude',
                   'location_accuracy': 'LocAccurac',
                   'associated_aquifers': 'Aquifer1',
                   'associated_uses': 'Use1',
                   'well_depth': 'WellDepth',
                   'yield': 'Yield',
                   'static_water_level': 'StaticWL',
                   'more_information': 'MoreInfo',
                   'idkey': 'IDKey'}
    df = df[select_columns]
    df = df.rename(columns=new_columns)
    df['WellDepth'] = pd.to_numeric(df['WellDepth'], errors='coerce')
    df['Yield'] = pd.to_numeric(df['Yield'], errors='coerce')
    df['StaticWL'] = pd.to_numeric(df['StaticWL'], errors='coerce')
    df['MoreInfo'] = df['MoreInfo'].apply(lambda x: x['url'])
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs=f'EPSG:{str(epsg_in)}')
    gdf = gdf.rename(columns=new_columns)
    if epsg_in != epsg_out:
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


def build_iris(well_id: str, _PREFIX: dict) -> dict:
    well_id = '_'.join(well_id.split())
    return {'well': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}'],
            'geom': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.geometry'],
            'depth': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.depth'],
            'depth_qv': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.depth.QV'],
            'yield': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.yield'],
            'yield_qv': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.yield.QV'],
            'swl': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.staticwaterlevel'],
            'swl_qv': _PREFIX['co_dwr_data'][f'CODWR-Well.{well_id}.staticwaterlevel.QV']}


def get_well_status(status: str) -> str:
    if 'pump' in status.lower():
        if 'expired' in status.lower():
            return ''.join(status.split()).replace('(', '').replace(')', '')
        elif 'without' in status.lower():
            return ''.join(status.split()).replace('inWellWithouta', 'Without')
        else:
            return ''.join(status.split()).replace(',', '').replace('Received', '')
    return '.'.join(status.split(' - ')).replace(' ', '').replace(',', '')


def get_loc_accuracy(accuracy: str) -> str:
    return ''.join(accuracy.title().split())


def add_provenance(kg: Graph) -> Graph:
    kg.add((ontologyIRI, RDF.type, OWL.Ontology))
    kg.add((ontologyIRI, _PREFIX['dcterms']['issued'], Literal(ttl_issued_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['dcterms']['modified'], Literal(ttl_modified_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['prov']['wasDerivedFrom'], _PREFIX['co_dwr']['sourceDataset']))
    kg.add((ontologyIRI, OWL.versionInfo, Literal(ttl_version, datatype=XSD.string)))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], RDF.type, _PREFIX['stad']['Dataset']))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], RDFS.label, Literal('CO DWR Well Application Permits', datatype=XSD.string)))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['dcterms']['issued'], Literal(date_issued_date, datatype=XSD.date)))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['dcterms']['source'], URIRef('https://data.colorado.gov/Water/DWR-Well-Application-Permit/wumm-7awb/data_preview')))
    # kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['dcterms']['source'], URIRef('https://cdss.colorado.gov/gis-data/gis-data-by-category')))
    kg.add((_PREFIX['co_dwr']['sourceDataset'], _PREFIX['stad']['hasSpatialCoverage'], _PREFIX['kwgr']['admininstrativeRegion.USA.08']))
    return kg


def triplify_well_data(gdf: gpd.GeoDataFrame, _PREFIX: dict, inputtype: str) -> None:
    kg = initial_kg(_PREFIX)
    logger.info(f'Triplify well data')
    kg = add_provenance(kg)
    for row in gdf.itertuples():
        if inputtype.lower() == 'shp':
            iris = build_iris(str(row.Receipt), _PREFIX)
            kg.add((iris['well'], _PREFIX['co_dwr']['hasReceipt'], Literal(row.Receipt, datatype=XSD.string)))
            kg.add((iris['well'], RDFS.label, Literal(f'Receipt: {row.Receipt}', datatype=XSD.string)))
        else:
            iris = build_iris(str(row.IDKey), _PREFIX)
            kg.add((iris['well'], _PREFIX['co_dwr']['hasIDKey'], Literal(row.IDKey, datatype=XSD.string)))
            kg.add((iris['well'], RDFS.label, Literal(f'IDKey: {row.IDKey}', datatype=XSD.string)))
            kg.add((iris['well'], _PREFIX['co_dwr']['hasReceipt'], Literal(row.Receipt, datatype=XSD.string)))
        kg.add((iris['well'], RDF.type, _PREFIX['co_dwr']['CODWR-Well']))
        kg.add((iris['well'], RDFS.isDefinedBy, ontologyIRI))
        kg.add((iris['well'], RDFS.seeAlso, Literal(row.MoreInfo, datatype=XSD.anyURI)))
        if isinstance(row.CurrStatus, str):
            kg.add((iris['well'],
                    _PREFIX['hyfo']['hasWellStatus'],
                    _PREFIX['co_dwr'][f'CODWR-WellStatus.{get_well_status(row.CurrStatus)}']))
        if isinstance(row.LocAccurac, str):
            kg.add((iris['well'],
                    _PREFIX['co_dwr']['locAccuracy'],
                    _PREFIX['co_dwr'][f'CODWR-LocAccuracy.{get_loc_accuracy(row.LocAccurac)}']))
        if isinstance(row.Use1, str):
            kg.add((iris['well'],
                    _PREFIX['hyfo']['hasWaterUse'],
                    Literal(row.Use1, datatype=XSD.string)))
        if isinstance(row.Aquifer1, str):
            kg.add((iris['well'],
                    _PREFIX['co_dwr']['hasAquifer'],
                    Literal(row.Aquifer1, datatype=XSD.string)))
        if row.WellDepth > 0:
            kg.add((iris['well'], _PREFIX['hyfo']['hasTotalDepth'], iris['depth']))
            kg.add((iris['depth'], RDF.type, _PREFIX['co_dwr']['CODWR-WellDepth']))
            kg.add((iris['depth'], _PREFIX['qudt']['quantityValue'], iris['depth_qv']))
            kg.add((iris['depth_qv'], RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((iris['depth_qv'], _PREFIX['qudt']['numericValue'], Literal(row.WellDepth, datatype=XSD.integer)))
            kg.add((iris['depth_qv'], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
        if row.Yield > 0:
            kg.add((iris['well'], _PREFIX['hyfo']['hasYield'], iris['yield']))
            kg.add((iris['yield'], RDF.type, _PREFIX['co_dwr']['CODWR-WellYield']))
            kg.add((iris['yield'], _PREFIX['qudt']['quantityValue'], iris['yield_qv']))
            kg.add((iris['yield_qv'], RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((iris['yield_qv'], _PREFIX['qudt']['numericValue'], Literal(row.Yield, datatype=XSD.decimal)))
            kg.add((iris['yield_qv'], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['GAL_US-PER-MIN']))
        if row.StaticWL > 0:
            kg.add((iris['well'], _PREFIX['hyfo']['hasStaticWaterDepth'], iris['swl']))
            kg.add((iris['swl'], RDF.type, _PREFIX['co_dwr']['CODWR-StaticWaterLevel']))
            kg.add((iris['swl'], _PREFIX['qudt']['quantityValue'], iris['swl_qv']))
            kg.add((iris['swl_qv'], RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((iris['swl_qv'], _PREFIX['qudt']['numericValue'], Literal(row.StaticWL, datatype=XSD.integer)))
            kg.add((iris['swl_qv'], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
        kg.add((iris['well'], _PREFIX['geo']['hasGeometry'], iris['geom']))
        kg.add((iris['well'], _PREFIX['geo']['defaultGeometry'], iris['geom']))
        kg.add((iris['geom'], _PREFIX["geo"]["asWKT"], Literal(row.geometry, datatype=_PREFIX['geo']['wktLiteral'])))
        kg.add((iris['geom'], RDF.type, _PREFIX['geo']['Geometry']))
    if inputtype.lower() == 'shp':
        logger.info(f'Write triples to {output_file_shp}')
        kg.serialize(output_file_shp, format='turtle')
    elif inputtype.lower() == 'csv':
        logger.info(f'Write triples to {output_file_csv}')
        kg.serialize(output_file_csv, format='turtle')
    else:
        logger.info(f'Write triples to {output_file_api}')
        kg.serialize(output_file_api, format='turtle')


if __name__ == "__main__":
    start_time = time.time()
    if inputtype.lower() == 'shp':
        logger.info(f'Process Colorado wells shapefile')
        gdf = load_wells_shp(wells_file_shp, epsg_shp, epsg_out)
        triplify_well_data(gdf, _PREFIX, inputtype.lower())
    elif inputtype.lower() == 'csv':
        logger.info(f'Process Colorado wells csv file')
        gdf = load_wells_csv(wells_file_csv, epsg_csv, epsg_out)
        triplify_well_data(gdf, _PREFIX, inputtype.lower())
    elif inputtype.lower() == 'api':
        logger.info(f'Process Colorado wells via API')
        gdf = load_wells_api(api_domain, api_dataset, epsg_csv, epsg_out)
        triplify_well_data(gdf, _PREFIX, inputtype.lower())
    else:
        logger.warning(f'Invalid input type - not in ["shp", "csv", "api"]')
    logger.info(f'Processing complete in {str(timedelta(seconds=time.time() - start_time))} HMS')
