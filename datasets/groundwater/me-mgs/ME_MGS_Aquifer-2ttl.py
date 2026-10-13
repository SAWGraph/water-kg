'''Create a .ttl file for Maine's aquifers from a .shp file containing fixed aquifer geometries

Under ### INPUT Filename ###, define
    the name (and path) of the input .shp file
Under ### OUTPUT Filenames ###, define
    the name (and path) of the output .ttl file for aquifers

Required:
    * geopandas
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, and XSD)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * add_provenance - add simple provenance info for the Illinois aquifer data to the knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for an aquifer and its geometry
    * process_aquifers_shp2ttl - takes two .shp files (aquifers and S2 cells), an output file name, and a dictionary
                                 of dissolved ids to lists of original ids, and creates and saves a .ttl file
'''

import geopandas as gpd
from pathlib import Path
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import GEO, OWL, PROV, RDF, RDFS, XSD

import logging
import time
import datetime

import sys
import os

## Variables
ttl_issued_date = '2025-07-18'
ttl_modified_date = '2026-10-12'
ttl_version = '0.1'
data_issued_date = '2019-10-03'
# aquifer id values are padded with leading zeros so they are all a fixed length
# max_id_length should be set to the maximum expected length of an id value (or longer)
max_id_length = 5

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
from namespaces2 import _PREFIX
ontologyIRI = URIRef('http://w3id.org/hyfo/me-mgs/v1/me-mgs-data')

# Set the current directory to this file's directory
os.chdir(cwd)

### INPUT Filename and related variables###
# mgs_aquifer_shp_path: This is a fixed version of the file from the Maine Geological Survey (MGS)
# s2_file: Level 13 S2 cells that overlap/are within Maine
mgs_aquifer_shp_path = data_dir / 'Maine_Aquifers-shp/Maine_Aquifers-fixed.shp'
# epsg_working is an equidistant CRS for working with buffers
# epsg_final is WGS 84, the default CRS for GeoSPARQL
epsg_working = 26919  # UTM zone 19N for Maine
epsg_final = 4326
# The SYMBOLOGY attribute has three values: '10-50 GPM', '>50 GPM', and 'Non-plotting water'
# This script excludes the third from triplification
# The third corresponds to an ATYPE value of 3, which is defined as an
#   "island of non-aquifer material within an area mapped as an aquifer" according to
#   https://www.maine.gov/dacf/mgs/pubs/digital/aquifers.htm
flow_rates = ['10-50 GPM', '>50 GPM']

### OUTPUT Filename ###
# aq_ttl_file: the resulting (output) .ttl file
aq_ttl_file = ttl_dir / 'me_23_mgs_aquifers2.ttl'

logname = log_dir / 'log_ME_MGS_Aquifers-2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def initial_kg(_PREFIX):
    '''Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    '''
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def add_provenance(kg: Graph) -> Graph:
    prefix = 'me_mgs_data'
    dataset = 'sourceDataset.SandGravelAquifers'
    kg.add((ontologyIRI, RDF.type, OWL.Ontology))
    kg.add((ontologyIRI, _PREFIX['dcterms']['issued'], Literal(ttl_issued_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['dcterms']['modified'], Literal(ttl_modified_date, datatype=XSD.date)))
    kg.add((ontologyIRI, PROV.wasDerivedFrom, _PREFIX[prefix][dataset]))
    kg.add((ontologyIRI, OWL.versionInfo, Literal(ttl_version, datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], RDF.type, _PREFIX['stad']['Dataset']))
    kg.add((_PREFIX[prefix][dataset], RDFS.label, Literal('Maine Significant Sand and Gravel Aquifers', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['issued'], Literal(data_issued_date, datatype=XSD.date)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['source'], URIRef('https://www.maine.gov/dacf/mgs/pubs/digital/aquifers.htm')))
    kg.add((_PREFIX[prefix][dataset], RDFS.comment, Literal('Significant Sand and Gravel Aquifer Maps Digital Data', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['stad']['hasSpatialCoverage'], _PREFIX['kwgr']['admininstrativeRegion.USA.23']))
    return kg


def build_mgs_iris(mgsid, _PREFIX):
    '''Create IRIs for an aquifer and its geometry

    :param mgsid: The aquifer id value for an aquifer
    :param _PREFIX: a dictionary of prefixes
    :return: a tuple with the two IRIs
    '''
    return (_PREFIX['me_mgs_data']['d.MGS-Aquifer.' + str(mgsid).zfill(max_id_length)],
            _PREFIX['me_mgs_data']['d.MGS-Aquifer.Geometry.' + str(mgsid).zfill(max_id_length)])


def process_aquifers_shp2ttl(mgs_infile, rates, outfile):
    '''Triplifies the aquifer data in a .shp file and saves the result as a .ttl file

    :param mgs_infile: a processed .shp file with aquifer data
    :param rates:
    :param outfile: the path and name for the aquifer .ttl file
    :return:
    '''
    logger.info('BEGIN TRIPLIFYING THE PROCESSED AQUIFERS')
    logger.info('Loading the shapefile')
    gdf_mgs_aquifers = gpd.read_file(mgs_infile)
    # See the notes above about flow rates for info on why the geodataframe is filtered next
    gdf_mgs_aquifers = gdf_mgs_aquifers[gdf_mgs_aquifers['SYMBOLOGY'].isin(rates)]
    logger.info('Intializing the knowledge graph')
    kg_aq = initial_kg(_PREFIX)
    kg_aq = add_provenance(kg_aq)
    logger.info('Creating the triples')
    for row in gdf_mgs_aquifers.itertuples():
        aquiferiri, polyiri = build_mgs_iris(row.AQUIFERID, _PREFIX)
        kg_aq.add((aquiferiri, RDF.type, _PREFIX['gwml2']['GW_Aquifer']))
        kg_aq.add((aquiferiri, _PREFIX['me_mgs']['meMgsAqId'], Literal(row.AQUIFERID, datatype=XSD.string)))
        kg_aq.add((aquiferiri, _PREFIX['hyfoplus']['aquiferType'], Literal('sand_gravel', datatype=XSD.string)))
        kg_aq.add((aquiferiri, RDFS.label, Literal('A sand and gravel aquifer in Maine', datatype=XSD.string)))
        kg_aq.add((aquiferiri, GEO.hasGeometry, polyiri))
        kg_aq.add((aquiferiri, GEO.defaultGeometry, polyiri))
        kg_aq.add((polyiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg_aq.add((polyiri, RDF.type, GEO.Geometry))
        # if 'multipolygon' in str(row.geometry).lower():
        #     kg_aq.add((polyiri, RDF.type, _PREFIX['sf']['MultiPolygon']))
        # else:
        #     kg_aq.add((polyiri, RDF.type, _PREFIX['sf']['Polygon']))
    kg_aq.serialize(outfile, format='turtle')
    logger.info('TRIPLIFYING COMPLETE AND .ttl FILE CREATED')


if __name__ == '__main__':
    start_time = time.time()
    process_aquifers_shp2ttl(mgs_aquifer_shp_path, flow_rates, aq_ttl_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
