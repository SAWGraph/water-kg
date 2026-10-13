'''Create a .ttl file for USGS alluvial/glacial aquifers from a .shp file

Under ### INPUT Filenames ###, modify (if necessary)
    the name (and path) of the input .shp file (alluvial)
Under ### OUTPUT Filename ###, modify (if necessary)
    the name (and path) of the output .ttl file

Required:
    * geopandas
    * pandas
    * rdflib (Graph, Literal, URIRef)
    * rdflib.namespace (GEO, OWL, PROV, RDF, RDFS, and XSD)
    * pathlib (Path)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a water body and its geometry
    * process_aquifers_shp2ttl - takes a .shp file and an output file name and creates and saves a .ttl file
'''

import geopandas as gpd
import pandas as pd
from pathlib import Path
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import GEO, OWL, PROV, RDF, RDFS, XSD

import logging
import time
import datetime

import sys
import os

## Variables
ttl_issued_date = '2025-10-03'
ttl_modified_date = '2026-10-13'
ttl_version = '0.1'
data_issued_date = '2023-09-15'

# Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent.parent.parent
data_dir = cwd.parent.parent.parent / 'data'
ttl_dir = cwd / 'ttl_files'
log_dir = cwd / 'logs'
# print(f'Current working directory:      {cwd}')
# print(f'Github repos and namespaces.py: {ns_dir}')
# print(f'Data (input) directory:         {data_dir}')
# print(f'Turtle (output) directory:      {ttl_dir}')
# print(f'Logging directory:              {log_dir}')

# Modify the system path to find namespaces.py
# sys.path.insert(1, 'G:/My Drive/Laptop/SAWGraph/Data Sources')
sys.path.insert(0, str(ns_dir))
from namespaces2 import _PREFIX
ontologyIRI = URIRef('http://w3id.org/hyfo/usgs/v1/principal-aquifers-data')

# Set the current directory to this file's directory
os.chdir(cwd)

### INPUT Filenames ###
aquifers_file = data_dir / f'US_Aquifers/alluvial.shp'

### OUTPUT Filename ###
ttl_file = ttl_dir / f'us_usgs-alluvialglacial-aquifers2.ttl'

logname = log_dir / f'log_US_USGS-AlluvialGlacial-Aquifers2ttl.txt'
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
    prefix = 'us_aqs_data'
    dataset = 'sourceDataset.AlluvialGlacialAquifers'
    kg.add((ontologyIRI, RDF.type, OWL.Ontology))
    kg.add((ontologyIRI, _PREFIX['dcterms']['issued'], Literal(ttl_issued_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['dcterms']['modified'], Literal(ttl_modified_date, datatype=XSD.date)))
    kg.add((ontologyIRI, PROV.wasDerivedFrom, _PREFIX[prefix][dataset]))
    kg.add((ontologyIRI, OWL.versionInfo, Literal(ttl_version, datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], RDF.type, _PREFIX['stad']['Dataset']))
    kg.add((_PREFIX[prefix][dataset], RDFS.label, Literal('Alluvial and Glacial Aquifers of the US', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['issued'], Literal(data_issued_date, datatype=XSD.date)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['source'], URIRef('https://www.sciencebase.gov/catalog/item/63140610d34e36012efa3859')))
    kg.add((_PREFIX[prefix][dataset], RDFS.comment, Literal('Alluvial and Glacial Aquifers', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['stad']['hasSpatialCoverage'], _PREFIX['kwgr']['admininstrativeRegion.USA']))
    return kg


def build_iris(objectid, _PREFIX):
    '''Create IRIs for an aquifer and its geometry

    :param objectid: The unique identifying value for an aquifer
    :param _PREFIX:
    :return: a tuple with the two IRIs
    '''
    base_iri = f'd.USGS_AlluvialGlacialAquifer_{str(objectid).zfill(4)}'
    return _PREFIX['us_aqs_data'][base_iri], _PREFIX['us_aqs_data'][base_iri + '.geometry']


def get_lithology(lith):
    if lith == 'Carbonate-rock aquifers':
        return 'CarbonateRock'
    elif lith == 'Crystalline':
        return 'Crystalline'
    elif lith == 'Igneous and metamorphic-rock aquifers':
        return 'IgneousMetamorphic'
    elif lith == 'Mixed':
        return 'Mixed'
    elif lith == 'Sandstone and carbonate-rock aquifers':
        return 'SandstoneCarbonateRock'
    elif lith == 'Sandstone aquifers':
        return 'Sandstone'
    elif lith == 'Sedimentary':
        return 'Sedimentary'
    elif lith == 'Semiconsolidated sand aquifers':
        return 'SemiconsolidatedSand'
    elif lith == 'Unconsolidated sand and gravel aquifers':
        return 'UnconsolidatedSandGravel'
    elif lith == 'Volcanic':
        return 'Volcanic'
    elif lith == None or pd.isna(lith):
        return 'Unspecified'
    else:
        raise ValueError(f'Unexpected ROCK_NAME {lith} from alluvial & glacial aquifers shape file')


def process_aquifers_shp2ttl(infile, outfile):
    '''Triplifies the principal aquifer data in a .shp file and saves the result as a .ttl file

    :param infile: a .shp file with NHD water body data
    :param outfile: the path and name for the .ttl file
    :return:
    '''
    logger.info(f'Load alluvial & glacial aquifer shapefile from {infile}')

    # Read alluvial & glacial aquifers to a GeoDataframe
    gdf_aquifers = gpd.read_file(infile)

    logger.info('Intialize RDFLib Graph')
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    kg = add_provenance(kg)
    # count = 1  # For processing updates printed to terminal
    # n = len(gdf_aquifers.index)  # For processing updates printed to terminal
    logger.info(f'Triplify principal aquifers')
    for row in gdf_aquifers.itertuples():
        # Get IRIs for the current principal aquifer and its geometry
        aqiri, geomiri = build_iris(row.ALLUVIAL_, _PREFIX)
        kg.add((aqiri, RDF.type, _PREFIX['gwml2']['GW_Aquifer']))

        # Triplify the geometry for the current principal aquifer
        kg.add((aqiri, GEO.hasGeometry, geomiri))
        kg.add((aqiri, GEO.defaultGeometry, geomiri))
        kg.add((geomiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg.add((geomiri, RDF.type, GEO.Geometry))

        # Triplify current principal aquifer attributes
        kg.add((aqiri, _PREFIX['us_aqs']['hasAlluvialGlacialId'], Literal(str(row.ALLUVIAL_).zfill(4), datatype=XSD.string)))
        kg.add((aqiri, _PREFIX['us_aqs']['hasLithology'], _PREFIX['us_aqs'][f'Lithology.{get_lithology(row.ROCK_NAME)}']))
        kg.add((aqiri, _PREFIX['us_aqs']['hasAqName'], Literal(row.AQ_NAME, datatype=XSD.string)))

        # Update the processing status to the terminal
        # print(f'Processing row {count:4} of {n} : OBJECTID {str(row.ALLUVIAL_):4}', end='\r', flush=True)
        # count += 1
    logger.info(f'Write alluvial & glacial aquifer triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script')
    process_aquifers_shp2ttl(aquifers_file, ttl_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
