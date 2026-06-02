"""Create a .ttl file of public water systems and their service areas from .csv files and a .gpkg file

Under ### states to process ###, enter
    a list of the two character abbreviations of the states to be processed
Under ### file paths ###, modify (if necessary)
    the name (and path) of the input .csv file for public water systems (SDWA_PUB_WATER_SYSTEMS.csv)
    the name (and path) of the input .csv file for public water system service areas (SDWA_SERVICE_AREAS.csv)
    the name (and path) of the input .gpkg file and layer for community water system service area geometries
        (PWS_Boundaries_3.0/Service_Areas_V_3_0.gpkg & CWS)
    the name (and path) of the input .gpkg file and layer for non-community water system service area geometries
        (PWS_Boundaries_3.0/Service_Areas_V_3_0.gpkg & T_NTNC)
    the name (and path) of the input .csv file for Safe Drinking Water Act reference codes (SDWA_REF_CODE_VALUES.csv)
The output file and path are in the main() function

Required:
    * namedtuple from collections
    * datetime & timedelta from datetime
    * geopandas
    * logging
    * pandas
    * Path from pathlib
    * Graph, Literal, Namespace, & URIRef from rdflib
    * RDF, RDFS, & XSD from rdflib.namespace
    * is_valid, is_valid_reason, & wkt from shapely
    * sys
    * time

Functions:
    * main - controls the script execution, looping through the states of interest and creating the output .ttl files
    * load_files - loads each full US dataset; sets geometries to EPSG 4326 and converts them to wkt
    * initialize_kg - creates an empty Graph with namespaces from the prefixes dictionary
    * get_iris - creates iris for public water systems, their service areas, the service area geometries, and where
                 relevant, service area types (controlled vocabulary)
    * process_pws_data - controls the processing of public water system data for a state
    * triplify_pws_data - controls the addition of public water system data for a state to a Graph
    * get_pws_attributes - add available attributes of interest for a public water system to a dictionary
    * get_pws_activity - determine and return a public water system's activity code (controlled vocabulary)
    * get_pws_owner_type - determine and return a public water system's owner type code (controlled vocabulary)
    * get_pws_primary_source - determine and return a public water system's primary water source code
                               (controlled vocabulary)
    * process_service_area_data - controls the processing of public water system service area data for a state
    * filter_service_area_data_by_state - takes public water system service area data and returns only those rows that
                                          are relevant to a desired state
    * triplify_service_area_data - controls the addition of public water system service area data for a state to a Graph
    * get_service_area_attributes - add available attributes of interest for a public water system service area to a
                                    dictionary
    * create_refcode_lookup - load SDWA reference code data to use as a lookup table
    * process_cws_geo_data - controls the processing of community water system geometry data for a state
    * filter_cws_geo_data_by_state - takes community water system service area geometry data and returns only those rows
                                     that are relevant to a desired state
    * triplify_cws_geo_data - controls the addition of community water system geometry data for a state to a Graph
    * get_cws_attributes - add available attributes of interest for a community water system's geometry to a dictionary
    * process_ncws_geo_data - controls the processing of non-community water system geometry data for a state
    * filter_ncws_geo_data_by_state - takes non-community water system service area geometry data and returns only those
                                      rows that are relevant to a desired state
    * triplify_ncws_geo_data - controls the addition of non-community water system geometry data for a state to a Graph
    * get_ncws_attributes - add available attributes of interest for a non-community water system's geometry to a
                            dictionary
"""
from collections import namedtuple
from datetime import datetime, timedelta
import geopandas as gpd
import logging
import pandas as pd
from pathlib import Path
from rdflib.namespace import RDF, RDFS, XSD
from rdflib import Graph, Literal, Namespace, URIRef
from shapely import is_valid, is_valid_reason, wkt
import sys
import time

## states to process
stateslist = ['ME', 'NH', 'MA', 'IL', 'IN', 'KS', 'MN', 'CO']

## directories
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent
data_dir = cwd.parent / 'data/SDWIS'
ttl_dir = cwd / 'ttl_files'
log_dir = cwd / 'logs'

## file paths
pws_data_file = data_dir / 'SDWA_PUB_WATER_SYSTEMS.csv'
service_area_data_file = data_dir / 'SDWA_SERVICE_AREAS.csv'
cws_data_file_layer = (data_dir / 'PWS_Boundaries_3.0/Service_Areas_V_3_0.gpkg', 'CWS')
ncws_data_file_layer = (data_dir / 'PWS_Boundaries_3.0/Service_Areas_V_3_0.gpkg', 'T_NTNC')
sdwa_ref_code_values_file = data_dir / 'SDWA_REF_CODE_VALUES.csv'

## namespaces
ontologyIRI = URIRef('http://sawgraph.spatialai.org/v1/us-sdwis-data')
prefixes = {'coso': Namespace(f'http://w3id.org/coso/v1/contaminoso#'),
            'geo': Namespace(f'http://www.opengis.net/ont/geosparql#'),
            'gcx': Namespace(f'http://geoconnex.us/'),
            'qudt': Namespace(f'http://qudt.org/schema/qudt/'),
            'sosa': Namespace(f'http://www.w3.org/ns/sosa/'),
            'us_sdwis': Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis#'),
            'us_sdwis_data': Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis-data#')}

## initiate log file
logname = log_dir / 'log_pws_serviceAreas_cws-ncws.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def main() -> None:
    """
        Calls loads_files to load primary data files,
        loops through states processing different public water system data and adding it to a Graph, and
        writes a .ttl file for each state

        :return:
    """
    df_pws, df_pwssa, df_cwsgeom, df_ncwsgeom = load_files()
    states = [state.upper() for state in stateslist]
    for state in states:
        start_time = time.time()
        logger.info(f'Processing PWS and SA for {state}')
        kg = initialize_kg()
        kg = process_pws_data(kg, df_pws, state)
        kg = process_service_area_data(kg, df_pwssa, state)
        kg = process_cws_geo_data(kg, df_cwsgeom, state)
        kg = process_ncws_geo_data(kg, df_ncwsgeom, state)
        output_turtle_file = ttl_dir / f'us-sdwis_pws-serviceareas-{state.strip()}.ttl'
        # kg.serialize(output_turtle_file, format='turtle')
        logger.info(f'Finished triplifying PWS and SA for {state} in {str(timedelta(seconds=time.time() - start_time))} HMS')


def load_files() -> tuple:
    """
        Loads the four data files specified above under ## file paths,
        sets coordinate reference systems to EPSG 4326,
        converts coordinates to wkt, and
        returns a dataframe or geodataframe for each, as appropriate, as a tuple

        :return: tuple of dataframes and geodataframes
    """
    start_time = time.time()
    logger.info('Loading data')
    logger.info('   Loading PWS data')
    df_pws = pd.read_csv(pws_data_file, dtype=str)
    logger.info('   Loading PWS service area data')
    df_pwssa = pd.read_csv(service_area_data_file)
    logger.info('   Loading CWS geometry data')
    df_cwsgeom = gpd.read_file(cws_data_file_layer[0], layer=cws_data_file_layer[1])
    df_cwsgeom['geometry'] = df_cwsgeom['geometry'].make_valid(method='structure')
    df_cwsgeom = df_cwsgeom.to_crs(crs='EPSG:4326')
    df_cwsgeom = df_cwsgeom.to_wkt()
    logger.info('   Loading NCWS geometry data')
    df_ncwsgeom = gpd.read_file(ncws_data_file_layer[0], layer=ncws_data_file_layer[1])
    df_ncwsgeom['geometry'] = df_ncwsgeom['geometry'].make_valid(method='structure')
    df_ncwsgeom = df_ncwsgeom.to_crs(crs='EPSG:4326')
    df_ncwsgeom = df_ncwsgeom.to_wkt()
    logger.info(f'Data loaded in {str(timedelta(seconds=time.time() - start_time))} HMS')
    return df_pws, df_pwssa, df_cwsgeom, df_ncwsgeom


def initialize_kg() -> Graph:
    """
        Creates an empty Graph,
        binds namespaces defined under ## namespaces, and
        returns the resulting Graph

        :return: empty Graph with bound namespaces
    """
    logger.info('   Initializing kg')
    kg = Graph()
    for prefix in prefixes:
        kg.bind(prefix, prefixes[prefix])
    return kg


def get_iris(attributes: dict, ref_codes: pd.DataFrame = None) -> dict:
    """
        Takes a dictionary of attributes and an optional dataframe that serves as a SDWA reference code lookup,
        creates IRIs for the current public water system, its service area, and the geometry of the service area,
        optionally creates an IRI for the service area type using the SDWA reference code lookup if necessary,
        returns a dictionary with the IRIs

        :param attributes: a dictionary of attributes for a public water system, its service area, or its service area geometry
        :param ref_codes: a dataframe that serves as a lookup table to find standard reference codes based on attribute values
        :return: dictionary of IRIs
    """
    iris = {'pws': prefixes['gcx']['ref/pws/' + attributes['pwsid']],
            'sa': prefixes['us_sdwis_data']['d.PWS-ServiceArea.' + attributes['pwsid']],
            'sageom': prefixes['us_sdwis_data']['d.PWS-ServiceArea.geometry.' + attributes['pwsid']]}
    if 'satype' in attributes:
        satypecode = ref_codes.loc[ref_codes['VALUE_DESCRIPTION'] == attributes['satype'], 'VALUE_CODE'].values[0]
        iris['satype'] = prefixes['us_sdwis']['PWS-ServiceArea-' + satypecode]
    return iris


def process_pws_data(kg: Graph, df: pd.DataFrame, state: str) -> Graph:
    """
        Takes a Graph, a dataframe of public water system data, and a two-character (uppercase) state code,
        calls a function to filter the dataframe to the given state,
        adds data to the Graph,
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param df: a dataframe of public water system data
        :param state: a two-character state code (uppercase)
        :return: an updated Graph
    """
    logger.info('   Processing PWS data')
    df = filter_pws_data_by_state(df, state)
    kg = triplify_pws_data(kg, df)
    logger.info('   PWS data processed')
    return kg


def filter_pws_data_by_state(df: pd.DataFrame, state: str) -> pd.DataFrame:
    """
        Takes a dataframe of public water system data and a two-character state code (uppercase),
        returns a dataframe with only the rows for the given state

        :param df: a dataframe of public water system data
        :param state: a two-character state code (uppercase)
        :return: a dataframe with only the rows for the given state
    """
    logger.info(f'      Filtering PWS data to {state}')
    df = df[df['PRIMACY_AGENCY_CODE'] == state]
    logger.info(f'      PWS data filtered to {state} ')
    return df


def triplify_pws_data(kg: Graph, df: pd.DataFrame) -> Graph:
    """
        Takes a Graph and a dataframe of public water system data for a specific state,
        writes new triples for each row (public water system) to the Graph, and
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param df: a dataframe of public water system data
        :return: an updated Graph
    """
    logger.info('      Triplifying PWS data')
    for row in df.itertuples():
        attributes = get_pws_attributes(row)
        iris = get_iris(attributes)
        kg.add((iris['pws'], RDF.type, prefixes['us_sdwis'][f'PublicWaterSystem-{attributes['pwstype']}']))
        kg.add((iris['pws'], RDFS.isDefinedBy, ontologyIRI))
        # kg.add((iris['pws'], prefixes['us_sdwis']['pwsId'], Literal(attributes['pwsid'], datatype=XSD.string)))
        kg.add((iris['pws'], prefixes['us_sdwis']['hasActivity'], Literal(attributes['activity'], datatype=XSD.string)))
        kg.add((iris['pws'], prefixes['us_sdwis']['populationServed'], Literal(attributes['popserved'], datatype=XSD.integer)))
        if 'name' in attributes:
            kg.add((iris['pws'], prefixes['us_sdwis']['pwsName'], Literal(attributes['name'], datatype=XSD.string)))
            kg.add((iris['pws'], RDFS.label, Literal(attributes['name'], datatype=XSD.string)))
        else:
            kg.add((iris['pws'], RDFS.label, Literal(attributes['pwsid'], datatype=XSD.string)))
        if 'deactive_date' in attributes:
            kg.add((iris['pws'], prefixes['us_sdwis']['deactivationDate'], Literal(attributes['deactive_date'], datatype=XSD.date)))
        if 'gwsw' in attributes:
            kg.add((iris['pws'], RDF.type, prefixes['us_sdwis'][f'PublicWaterSystem-{attributes['gwsw']}']))
        if 'ownertype' in attributes:
            kg.add((iris['pws'], prefixes['us_sdwis']['hasOwnership'], Literal(attributes['ownertype'], datatype=XSD.string)))
        if 'source' in attributes:
            kg.add((iris['pws'], prefixes['us_sdwis']['primarySourceType'], prefixes['us_sdwis'][f'PWS-WaterSourceType.{row.PRIMARY_SOURCE_CODE}']))
        #     kg.add((iris['pws'], prefixes['us_sdwis']['primarySource'], Literal(attributes['source'], datatype=XSD.string)))
        if 'connections' in attributes:
            kg.add((iris['pws'], prefixes['us_sdwis']['serviceConnections'], Literal(attributes['connections'], datatype=XSD.integer)))
        if 'firstreport' in attributes:
            kg.add((iris['pws'], prefixes['us_sdwis']['firstReport'], Literal(attributes['firstreport'], datatype=XSD.date)))
        if 'lastreport' in attributes:
            kg.add((iris['pws'], prefixes['us_sdwis']['lastReport'], Literal(attributes['lastreport'], datatype=XSD.date)))
        # if 'sourceprotection' in attributes:
        #     kg.add((iris['pws'], prefixes['us_sdwis']['sourceProtection'], Literal(attributes['sourceprotection'], datatype=XSD.date)))
        # if 'cdsid' in attributes:
        #     kg.add((iris['pws'], prefixes['us_sdwis']['cdsId'], Literal(attributes['cdsid'], datatype=XSD.date)))
    logger.info(f'      PWS data triplified')
    return kg


def get_pws_attributes(row: namedtuple) -> dict:
    """
        Takes a dataframe row as a tuple (from itertuples),
        write desired attributes to a dictionary where possible, and
        returns the dictionary

        :param row: a tuple of public water system data (from itertuples)
        :return: a dictionary with desired public water system attributes
    """
    attributes = {'pwsid': row.PWSID,
                  'state': row.STATE_CODE,
                  'pwstype': row.PWS_TYPE_CODE,
                  'activity': get_pws_activity(row.PWS_ACTIVITY_CODE),
                  'popserved': row.POPULATION_SERVED_COUNT}
    if pd.notnull(row.PWS_NAME):
        attributes['name'] = row.PWS_NAME
    if pd.notnull(row.PWS_DEACTIVATION_DATE):
        strdate = datetime.strptime(row.PWS_DEACTIVATION_DATE, '%m/%d/%Y')
        xsddate = strdate.strftime('%Y-%m-%d')
        attributes['deactive_date'] = xsddate
    if pd.notnull(row.GW_SW_CODE):
        attributes['gwsw'] = row.GW_SW_CODE
    if pd.notnull(row.OWNER_TYPE_CODE):
        attributes['ownertype'] = get_pws_owner_type(row.OWNER_TYPE_CODE)
    if pd.notnull(row.PRIMARY_SOURCE_CODE):
        attributes['source'] = get_pws_primary_source(row.PRIMARY_SOURCE_CODE)
    if pd.notnull(row.SERVICE_CONNECTIONS_COUNT):
        attributes['connections'] = row.SERVICE_CONNECTIONS_COUNT
    if pd.notnull(row.FIRST_REPORTED_DATE):
        strdate = datetime.strptime(row.FIRST_REPORTED_DATE, '%m/%d/%Y')
        xsddate = strdate.strftime('%Y-%m-%d')
        attributes['firstreport'] = xsddate
    if pd.notnull(row.LAST_REPORTED_DATE):
        strdate = datetime.strptime(row.LAST_REPORTED_DATE, '%m/%d/%Y')
        xsddate = strdate.strftime('%Y-%m-%d')
        attributes['lastreport'] = xsddate
    # if pd.notnull(row.SOURCE_WATER_PROTECTION_CODE):
    #     attributes['sourceprotection'] = row.SOURCE_WATER_PROTECTION_CODE
    # if pd.notnull(row.CDS_ID):
    #     attributes['cdsid'] = row.CDS_ID
    return attributes


def get_pws_activity(code: str) -> str:
    """
        Takes a public water system activity code and returns its full text value

        :param code: a public water system activity code
        :return: the full text activity description for a public water system
    """
    match code.lower():
        case 'a':
            return 'active'
        case 'i':
            return 'inactive'
        case 'n':
            return 'changed from public to non-public'
        case 'm':
            return 'merged with another system'
        case 'p':
            return 'potential future system to be regulated'
        case _:
            raise Exception(f'Unexpected PWS activity code ({code}) in {pws_data_file}')


def get_pws_owner_type(code: str) -> str:
    """
        Takes a public water system owner type code and returns its full text value

        :param code: a public water system owner type code
        :return: the full text owner type description for a public water system
    """
    match code.lower():
        case 'f':
            return 'federal government'
        case 'l':
            return 'local government'
        case 'm':
            return 'public/private'
        case 'n':
            return 'Native American'
        case 'p':
            return 'private'
        case 's':
            return 'state government'
        case _:
            raise Exception(f'Unexpected PWS owner type code ({code}) in {pws_data_file}')


def get_pws_primary_source(code: str) -> str:
    """
        Takes a public water system primary source code and returns its full text value

        :param code: a public water system primary source code
        :return: the full text primary source description for a public water system
    """
    match code.lower():
        case 'gw':
            return 'groundwater'
        case 'gwp':
            return 'groundwater purchased'
        case 'sw':
            return 'surface water'
        case 'swp':
            return 'surface water purchased'
        case 'gu':
            return 'groundwater under influence of surface water'
        case 'gup':
            return 'purchased groundwater under influence of surface water source'
        case _:
            raise Exception(f'Unexpected PWS primary source code ({code}) in {pws_data_file}')


def process_service_area_data(kg: Graph, df: pd.DataFrame, state: str) -> Graph:
    """
        Takes a Graph, a dataframe of public water system service area data, and a two-character (uppercase) state code,
        calls a function to filter the dataframe to the given state,
        adds data to the Graph,
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param df: a dataframe of public water system service area data
        :param state: a two-character state code (uppercase)
        :return: an updated Graph
    """
    logger.info('   Processing PWS service area data')
    df = filter_service_area_data_by_state(df, state)
    kg = triplify_service_area_data(kg, df)
    logger.info('   PWS service area data processed')
    return kg


def filter_service_area_data_by_state(df: pd.DataFrame, state: str) -> pd.DataFrame:
    """
        Takes a dataframe of public water system service area data and a two-character state code (uppercase),
        creates a new column with two-character state codes (uppercase), and
        returns a dataframe with only the rows for the given state

        :param df: a dataframe of public water system service area data
        :param state: a two-character state code (uppercase)
        :return: a dataframe with only the rows for the given state
    """
    logger.info(f'      Filtering PWS service area data to {state} ')
    df['state'] = df['PWSID'].astype(str).str[0:2]
    df = df[df['state'] == state]
    logger.info(f'      Service area data filtered to {state} .')
    return df


def triplify_service_area_data(kg: Graph, df: pd.DataFrame) -> Graph:
    """
        Takes a Graph and a dataframe of public water system service area data for a specific state,
        writes new triples for each row (public water system) to the Graph, and
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param df: a dataframe of public water system service area data
        :return: an updated Graph
    """
    logger.info('      Triplifying PWS service area data')
    ref_codes = create_refcode_lookup()
    for row in df.itertuples():
        attributes = get_service_area_attributes(row)
        iris = get_iris(attributes, ref_codes)
        kg.add((iris['pws'], RDF.type, prefixes['us_sdwis']['PublicWaterSystem']))
        kg.add((iris['pws'], RDFS.isDefinedBy, ontologyIRI))
        kg.add((iris['pws'], prefixes['us_sdwis']['serviceArea'], iris['sa']))
        kg.add((iris['sa'], RDF.type, prefixes['us_sdwis']['PWS-ServiceArea']))
        if 'satype' in attributes:
            kg.add((iris['sa'], prefixes['us_sdwis']['serviceAreaType'], iris['satype']))
    logger.info(f'      PWS service area data triplified')
    return kg


def get_service_area_attributes(row: namedtuple) -> dict:
    """
        Takes a dataframe row as a tuple (from itertuples),
        writes desired attributes to a dictionary where possible, and
        returns the dictionary

        :param row: a tuple of public water system service area data (from itertuples)
        :return: a dictionary with desired public water system service area attributes
    """
    attributes = {'pwsid': row.PWSID,
                  'state': row.state,
                  'type': row.SERVICE_AREA_TYPE_CODE,
                  'primary': bool(row.IS_PRIMARY_SERVICE_AREA_CODE),
                  'first': row.FIRST_REPORTED_DATE,
                  'last': row.LAST_REPORTED_DATE}
    return attributes


def create_refcode_lookup() -> pd.DataFrame:
    """
        Read SDWA reference code data into a dataframe and return it

        :return: a dataframe containing reference codes for use as a lookup table
    """
    return pd.read_csv(sdwa_ref_code_values_file)


def process_cws_geo_data(kg: Graph, gdf: gpd.GeoDataFrame, state: str) -> Graph:
    """
        Takes a Graph, geodataframe of community water system service area geometry data, and a two-character (uppercase) state code,
        calls a function to filter the geodataframe to the given state,
        adds data to the Graph,
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param gdf: a dataframe of community water system service area geometry data
        :param state: a two-character state code (uppercase)
        :return: an updated Graph
    """
    logger.info('   Processing CWS service area geometry data')
    gdf = filter_cws_geo_data_by_state(gdf, state)
    kg = triplify_cws_geo_data(kg, gdf)
    logger.info('   CWS service area geometry data processed')
    return kg


def filter_cws_geo_data_by_state(gdf: gpd.GeoDataFrame, state: str) -> gpd.GeoDataFrame:
    """
        Takes a geodataframe of community water system service area geometry data and a two-character state code (uppercase) and
        returns a geodataframe with only the rows for the given state

        :param gdf: a geodataframe of community water system service area geometry data
        :param state: a two-character state code (uppercase)
        :return: a geodataframe with only the rows for the given state
    """
    logger.info(f'      Filter CWS service area geometry data to {state} ')
    gdf = gdf[gdf['Primacy_Agency'] == state]
    logger.info(f'      CWS service area geometry data filtered to {state} ')
    return gdf


def triplify_cws_geo_data(kg: Graph, gdf: gpd.GeoDataFrame) -> Graph:
    """
        Takes a Graph and a geodataframe of community water system service area geometry data for a specific state,
        writes new triples for each row (community water system) to the Graph, and
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param gdf: a geodataframe of community water system service area geometry data
        :return: an updated Graph
    """
    logger.info('      Triplifying CWS service area geometry data')
    ref_codes = create_refcode_lookup()
    for row in gdf.itertuples():
        attributes = get_cws_attributes(row)
        iris = get_iris(attributes, ref_codes)
        kg.add((iris['pws'], RDF.type, prefixes['us_sdwis']['PublicWaterSystem-CWS']))
        kg.add((iris['pws'], RDFS.isDefinedBy, ontologyIRI))
        kg.add((iris['pws'], prefixes['us_sdwis']['serviceArea'], iris['sa']))
        kg.add((iris['pws'], prefixes['us_sdwis']['pwsName'], Literal(attributes['name'], datatype=XSD.string)))
        kg.add((iris['sa'], RDF.type, prefixes['us_sdwis']['PWS-ServiceArea']))
        if 'satype' in attributes:
            kg.add((iris['sa'], prefixes['us_sdwis']['serviceAreaType'], iris['satype']))
        if 'method' in attributes:
            kg.add((iris['sa'], prefixes['us_sdwis']['hasMethod'], Literal(attributes['method'], datatype=XSD.string)))
            # Note: A service area with a method but no geometry implies a bad geometry
        if is_valid(wkt.loads(str(attributes['geometry']))):
            kg.add((iris['sa'], prefixes['geo']['hasGeometry'], iris['sageom']))
            kg.add((iris['sa'], prefixes['geo']['defaultGeometry'], iris['sageom']))
            kg.add((iris['sageom'], RDF.type, prefixes['geo']['Geometry']))
            kg.add((iris['sageom'], prefixes['geo']['asWKT'], Literal(attributes['geometry'], datatype=prefixes['geo']['wktLiteral'])))
        else:
            logger.info(f'      {iris['sa']} has invalid geometry ({is_valid_reason(wkt.loads(str(attributes['geometry'])))}).')
    logger.info(f'      CWS service area geometry data triplified')
    return kg


def get_cws_attributes(row: namedtuple):
    """
        Takes a geodataframe row as a tuple (from itertuples),
        writes desired attributes to a dictionary where possible, and
        returns the dictionary

        :param row: a tuple of community water system service area geometry data (from itertuples)
        :return: a dictionary with desired community water system service area geometry attributes
    """
    attributes = {'pwsid': row.PWSID,
                  'state': row.Primacy_Agency,
                  'geometry': row.geometry}
    if pd.notnull(row.PWS_Name):
        attributes['name'] = row.PWS_Name
    if pd.notnull(row.Service_Area_Type):
        attributes['satype'] = row.Service_Area_Type
    if pd.notnull(row.Model_Method):
        attributes['method'] = row.Model_Method
    return attributes


def process_ncws_geo_data(kg: Graph, gdf: gpd.GeoDataFrame, state: str) -> Graph:
    """
        Takes a Graph, geodataframe of non-community water system service area geometry data, and a two-character (uppercase) state code,
        calls a function to filter the geodataframe to the given state,
        adds data to the Graph,
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param gdf: a dataframe of non-community water system service area geometry data
        :param state: a two-character state code (uppercase)
        :return: an updated Graph
    """
    logger.info('   Processing NCWS data')
    gdf = filter_ncws_geo_data_by_state(gdf, state)
    kg = triplify_ncws_geo_data(kg, gdf)
    logger.info('   NCWS service area geometry data processed')
    return kg


def filter_ncws_geo_data_by_state(gdf: gpd.GeoDataFrame, state: str) -> gpd.GeoDataFrame:
    """
        Takes a geodataframe of non-community water system service area geometry data and a two-character state code (uppercase) and
        returns a geodataframe with only the rows for the given state

        :param gdf: a geodataframe of non-community water system service area geometry data
        :param state: a two-character state code (uppercase)
        :return: a geodataframe with only the rows for the given state
    """
    logger.info(f'      Filter NCWS service area geometry data to {state} ')
    gdf = gdf[gdf['PRIMACY_AGENCY_CODE'] == state]
    logger.info(f'      NCWS service area geometry data filtered to {state} ')
    return gdf


def triplify_ncws_geo_data(kg: Graph, gdf: gpd.GeoDataFrame) -> Graph:
    """
        Takes a Graph and a geodataframe of non-community water system service area geometry data for a specific state,
        writes new triples for each row (non-community water system) to the Graph, and
        returns the updated Graph

        :param kg: a Graph of public water system triples for a given state
        :param gdf: a geodataframe of non-community water system service area geometry data
        :return: an updated Graph
    """
    logger.info('      Triplifying NCWS service area geometry data')
    ref_codes = create_refcode_lookup()
    for row in gdf.itertuples():
        attributes = get_ncws_attributes(row)
        iris = get_iris(attributes, ref_codes)
        kg.add((iris['pws'], RDF.type, prefixes['us_sdwis'][f'PublicWaterSystem-{attributes['pwstype']}']))
        kg.add((iris['pws'], RDFS.isDefinedBy, ontologyIRI))
        kg.add((iris['pws'], prefixes['us_sdwis']['serviceArea'], iris['sa']))
        kg.add((iris['pws'], prefixes['us_sdwis']['pwsName'], Literal(attributes['name'], datatype=XSD.string)))
        kg.add((iris['sa'], RDF.type, prefixes['us_sdwis']['PWS-ServiceArea']))
        if 'satype' in attributes:
            kg.add((iris['sa'], prefixes['us_sdwis']['serviceAreaType'], iris['satype']))
        if is_valid(wkt.loads(str(attributes['geometry']))):
            kg.add((iris['sa'], prefixes['geo']['hasGeometry'], iris['sageom']))
            kg.add((iris['sa'], prefixes['geo']['defaultGeometry'], iris['sageom']))
            kg.add((iris['sageom'], RDF.type, prefixes['geo']['Geometry']))
            kg.add((iris['sageom'], prefixes['geo']['asWKT'], Literal(attributes['geometry'], datatype=prefixes['geo']['wktLiteral'])))
        else:
            logger.info(f'      {iris['sa']} has invalid geometry ({is_valid_reason(wkt.loads(str(attributes['geometry'])))}).')
    logger.info(f'      NCWS service area geometry data triplified')
    return kg


def get_ncws_attributes(row: namedtuple):
    """
        Takes a geodataframe row as a tuple (from itertuples),
        writes desired attributes to a dictionary where possible, and
        returns the dictionary

        :param row: a tuple of nono-community water system service area geometry data (from itertuples)
        :return: a dictionary with desired non-community water system service area geometry attributes
    """
    attributes = {'pwsid': row.PWSID,
                  'state': row.PRIMACY_AGENCY_CODE,
                  'geometry': row.geometry}
    if pd.notnull(row.PWS_Name):
        attributes['name'] = row.PWS_Name
    if pd.notnull(row.SERVICE_AREA_TYPE):
        attributes['satype'] = row.SERVICE_AREA_TYPE
    if pd.notnull(row.PWS_TYPE_CODE):
        attributes['pwstype'] = row.PWS_TYPE_CODE
    return attributes


if __name__ == '__main__':
    main()
