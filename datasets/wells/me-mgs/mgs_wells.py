import geopandas as gpd
import pandas as pd
from pathlib import Path
from rdflib import Namespace, Graph, Literal, URIRef
from rdflib.namespace import GEO, OWL, PROV, RDF, RDFS, SDO, XSD
from shapely.affinity import translate
# import math
# import json

import logging
import time
import datetime
# from datetime import date

import sys
import os

## Variables
ttl_issued_date = '2025-07-07'
ttl_modified_date = '2026-09-03'
ttl_version = '0.1'
unlocated_data_issued_date = '2026-01-26'
located_data_issued_date = '2026-01-26'

# Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent.parent
data_dir = cwd.parent.parent / 'data'
ttl_dir = cwd / 'ttl_files'
log_dir = cwd / 'logs'
# print(f'Current working directory:      {cwd}')
# print(f'Github repos and namespaces.py: {ns_dir}')
# print(f'Data (input) directory:         {data_dir}')
# print(f'Turtle (output) directory:      {ttl_dir}')
# print(f'Logging directory:              {log_dir}')

# Modify the system path to find namespaces.py
sys.path.insert(0, str(ns_dir))
from namespaces import _PREFIX
ontologyStem = 'http://sawgraph.spatialai.org/v1/me-mgs-data'
ontologyIRI = URIRef(ontologyStem)

# Set the current directory to this file's directory
os.chdir(cwd)

### INPUT Filenames ###
unlocated_infile = data_dir / 'mgs_wells/MGS_Wells_Database_-Unlocated.csv'
located_infile = data_dir / 'mgs_wells/MGS_Wells_Database_-Located.csv'

### OUTPUT Filenames ###
unlocated_outfile = ttl_dir / 'mgs_wells_unlocated.ttl'
unlocated_towns_outfile = ttl_dir / 'mgs_wells_unlocated_towns.ttl'
located_outfile = ttl_dir / 'mgs_wells_located.ttl'
located_towns_outfile = ttl_dir / 'mgs_wells_located_towns.ttl'

## Setup and initiate logging
logname = log_dir / f'log_US_NHD_Waterbody_HUCxx-2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def process_unlocated_wells():
    logger.info('Load MGS unlocated wells to dataframe')
    unlocated_df = pd.read_csv(unlocated_infile, low_memory=False)
    logger.info('Triplify MGS unlocated wells')
    kg, towns = triplify_well_data(unlocated_df, _PREFIX, 'unlocated')
    logger.info(f'Write MGS unlocated wells triples to {unlocated_outfile}')
    kg.serialize(unlocated_outfile, format='turtle')
    # logger.info(f'Write MGS unlocated wells town triples to {unlocated_towns_outfile}')
    # towns.serialize(unlocated_towns_outfile, format='turtle')


def process_located_wells():
    logger.info('Load MGS located wells to geodataframe')
    located_df = pd.read_csv(located_infile, encoding='ISO-8859-1', low_memory=False)
    columns = {'Well Number': 'WELLNO',
               'Well Use': 'WELL_USE',
               'Well Type': 'WELL_TYPE',
               'Well Depth (ft)': 'WELL_DEPTH_FT',
               'Overburden Thickness (ft)': 'OVERBURDEN_THICKNESS_FT',
               'Town': 'WELL_LOCATION_TOWN'}
    located_df = located_df.rename(columns=columns)
    located_gdf = gpd.GeoDataFrame(located_df, geometry=gpd.points_from_xy(located_df.Longitude, located_df.Latitude))
    located_gdf = fix_longitude(located_gdf)
    logger.info('Triplify MGS located wells')
    kg, towns = triplify_well_data(located_gdf, _PREFIX, 'located')
    logger.info(f'Write MGS located wells triples to {located_outfile}')
    kg.serialize(located_outfile, format='turtle')
    # logger.info(f'Write MGS located wells town triples to {located_towns_outfile}')
    # towns.serialize(located_towns_outfile, format='turtle')


def fix_longitude(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # A couple of entries in the MGS located database have
    # longitudes given in 0 to 360 E format
    # instead of -180 to 180 W/E format
    mask = gdf.geometry.x > 180
    gdf.loc[mask, 'geometry'] = gdf.loc[mask, 'geometry'].apply(lambda geom: translate(geom, xoff=-360))
    return gdf


def initial_kg(_PREFIX: dict) -> Graph:
    kg = Graph()
    for prefix in _PREFIX:
        kg.bind(prefix, _PREFIX[prefix])
    return kg


def add_provenance(kg: Graph, dataset: str) -> Graph:
    ontologyIRI = URIRef(f'{ontologyStem}/{dataset}')
    kg.add((ontologyIRI, RDF.type, OWL.Ontology))
    kg.add((ontologyIRI, _PREFIX['dcterms']['issued'], Literal(ttl_issued_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['dcterms']['modified'], Literal(ttl_modified_date, datatype=XSD.date)))
    kg.add((ontologyIRI, OWL.versionInfo, Literal(ttl_version, datatype=XSD.string)))
    kg.add((ontologyIRI, _PREFIX['prov']['wasDerivedFrom'], _PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}']))
    kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], RDF.type, _PREFIX['stad']['Dataset']))
    kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], _PREFIX['stad']['hasSpatialCoverage'], _PREFIX['kwgr']['admininstrativeRegion.USA.23']))
    if dataset == 'unlocated':
        kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], RDFS.label, Literal('Maine Well Database - Unlocated Wells', datatype=XSD.string)))
        kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], _PREFIX['dcterms']['issued'], Literal(unlocated_data_issued_date, datatype=XSD.date)))
        kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], _PREFIX['dcterms']['source'], URIRef('https://mgs-maine.opendata.arcgis.com/datasets/maine-well-database-unlocated-wells')))
    else:
        kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], RDFS.label, Literal('Maine Well Database - Well Depth', datatype=XSD.string)))
        kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], _PREFIX['dcterms']['issued'], Literal(located_data_issued_date, datatype=XSD.date)))
        kg.add((_PREFIX['me_mgs_data'][f'sourceDataset{dataset.capitalize()}'], _PREFIX['dcterms']['source'], URIRef('https://mgs-maine.opendata.arcgis.com/datasets/maine-well-database-well-depth')))
    return kg


def get_attributes(row: tuple, _PREFIX: dict) -> dict:
    # this attribute schema works for MGS well data
    att_dict = {}
    att_dict['well_no'] = row.WELLNO  # well number
    att_dict['well_use'] = str(row.WELL_USE).lower().title().replace(', ', '')  # well use
    att_dict['well_type'] = str(row.WELL_TYPE).lower().title().replace(' ', '')  # well type
    att_dict['well_depth'] = row.WELL_DEPTH_FT
    att_dict['well_overburden'] = row.OVERBURDEN_THICKNESS_FT
    att_dict['well_iri'] = _PREFIX['me_mgs_data'][f'd.MGS-Well.{att_dict['well_no']}']

    # town
    att_dict['town_name_formatted'] = str(row.WELL_LOCATION_TOWN)

    return att_dict


## triplify the abox
def triplify_well_data(df: pd.DataFrame, _PREFIX: dict, dataset: str) -> tuple:
    kg = initial_kg(_PREFIX)
    kg = add_provenance(kg, dataset)
    kg2 = initial_kg(_PREFIX)

    # get_towns = False
    # if get_towns:
    #     # get dcids for each unique town
    #     towns = df.WELL_LOCATION_TOWN.unique()
    #     town_dcid = {}
    #     for town in towns:
    #         town_name_formatted = str(town)+' town, MAINE'
    #         resp = utilities.resolvePlaceName(town_name_formatted)
    #         #print(town_name_formatted, resp.text)
    #         try:
    #             dcids = resp.json()['entities'][0]['resolvedIds']
    #         except:
    #             dcids = []
    #         town_dcid[town] = dcids
    #     with open('towns.txt', 'w') as town_dictionary:
    #         town_dictionary.write(json.dumps(town_dcid))
    # else:
    #     with open('towns.txt', 'r') as town_file:
    #         town_dcid = json.load(town_file)
    #         # print(town_dcid)
    # for town in town_dcid.keys():
    #     # print(town, town_dcid[town])
    #     if town_dcid[town] != []:
    #         for place in town_dcid[town]:
    #             kg2.add((_PREFIX['dc'][place], RDF.type, _PREFIX['kwg-ont']['AdministrativeRegion_3']))

    for row in df.itertuples():
        attribute_dict = get_attributes(row, _PREFIX)
        well_iri = attribute_dict['well_iri']

        # well instance
        kg.add((well_iri, RDF.type, _PREFIX['me_mgs']['MGS-Well']))
        kg.add((well_iri, RDFS.isDefinedBy, ontologyIRI))
        kg.add((well_iri, RDFS.label, Literal(f'MGS well {str(attribute_dict['well_no'])}')))
        if attribute_dict['well_type'] != 'Nan':
            kg.add((well_iri, _PREFIX['me_mgs']['ofWellType'], _PREFIX['me_mgs_data'][f'd.wellType.{attribute_dict['well_type']}']))
        if attribute_dict['well_use'] != 'Nan':
            kg.add((well_iri, _PREFIX['me_mgs']['hasUse'], _PREFIX['me_mgs_data'][f'd.wellUse.{attribute_dict['well_use']}']))
        kg.add((well_iri, _PREFIX['me_mgs']['wellDepth'], _PREFIX['me_mgs_data'][f'd.WellDepthInFt.MGS-Well.{str(attribute_dict['well_no'])}']))
        kg.add((_PREFIX['me_mgs_data'][f'd.WellDepthInFt.MGS-Well.{str(attribute_dict['well_no'])}'], _PREFIX['qudt']['numericValue'], Literal(float(attribute_dict['well_depth']), datatype=XSD.float)))
        kg.add((_PREFIX['me_mgs_data'][f'd.WellDepthInFt.MGS-Well.{str(attribute_dict['well_no'])}'], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
        if pd.isna(attribute_dict['well_overburden']) == False:
            kg.add((well_iri, _PREFIX['me_mgs']['wellOverburden'], _PREFIX['me_mgs_data'][f'd.WellOverburdenInFt.MGS-Well.{str(attribute_dict['well_no'])}']))
            kg.add((_PREFIX['me_mgs_data'][f'd.WellOverburdenInFt.MGS-Well.{str(attribute_dict['well_no'])}'], _PREFIX['qudt']['numericValue'], Literal(float(attribute_dict['well_overburden']), datatype=XSD.float)))
            kg.add((_PREFIX['me_mgs_data'][f'd.WellOverburdenInFt.MGS-Well.{str(attribute_dict['well_no'])}'], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))

        # well geometry
        if hasattr(row, 'geometry') and -71.1 <= row.geometry.x <= -66.9 and 42.9 <= row.geometry.y <= 47.5:
            # A few entries in the MGS located database have coordinates placing them considerably outside of Maine
            # The well attributes are triplified, but the geometries are not
            well_geometry_iri = _PREFIX['me_mgs_data'][f'd.MGS-Well-Geometry.{attribute_dict['well_no']}']
            kg.add((well_iri, GEO.hasGeometry, well_geometry_iri))
            kg.add((well_iri, GEO.defaultGeometry, well_geometry_iri))
            kg.add((well_geometry_iri, _PREFIX['geo']['asWKT'], Literal(row.geometry, datatype=GEO.wktLiteral)))
            kg.add((well_geometry_iri, RDF.type, GEO.Geometry))

        # todo lookup FIPS code for town
        #kg.add((well_iri, _PREFIX['aik-pfas']['locatedIn'], town_iri))
        # if town_name_formatted in town_dcid.keys():
        #     for place in town_dcid[town_name_formatted]:
        #             kg.add((well_iri, _PREFIX['kwg-ont']['sfWithin'], _PREFIX['dc'][place]))

        #if idx == 5:
            #break

    # T-box lists
    f_type = open(f'well_types_{dataset}.txt', 'w')
    logger.info(f'Write well types to {f_type}')
    well_types = df.WELL_TYPE.unique().tolist()
    for t in well_types:
        wt = str(t).lower().title().replace(' ', '')
        if wt != 'Nan':
            f_type.write(f'{wt}\n')
    f_type.close()

    f_use = open(f'well_uses_{dataset}.txt', 'w')
    logger.info(f'Write well uses to {f_use}')
    well_use = df.WELL_USE.unique().tolist()
    for u in well_use:
        wu = str(u).lower().title().replace(', ', '')
        if wu != 'Nan':
            f_use.write(f'{wu}\n')
    f_use.close()

    return kg, kg2


## utility functions

# def is_valid(value):
#     if math.isnan(float(value)):
#         return False
#     else:
#         return True
#
#
# def rem_time(d):
#     s = date(d.year, d.month, d.day)
#     return s


if __name__ == '__main__':
    start_time = time.time()
    process_unlocated_wells()
    process_located_wells()
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
