'''Create a .ttl file for USGS hydrogeologic settings from a .shp file

Under ### INPUT Filenames ###, modify (if necessary)
    the name (and path) of the input .shp file (HG_Settings)
Under ### OUTPUT Filename ###, modify (if necessary)
    the name (and path) of the output .ttl file

Required:
    * geopandas
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, and XSD)
    * pathlib (Path)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for a water body and its geometry
    * process_aquifers_shp2ttl - takes a .shp file and an output file name and creates and saves a .ttl file
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
ttl_issued_date = '2026-02-10'
ttl_modified_date = '2026-10-13'
ttl_version = '0.1'
data_issued_date = '2026-01-06'

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
ontologyIRI = URIRef('http://w3id.org/hyfo/usgs/v1/hg-settings-data')

# Set the current directory to this file's directory
os.chdir(cwd)

### INPUT Filenames ###
hgsettings_file = data_dir / f'USGS_Depth_of_Groundwater_Data/HG_Settings.shp'
epsg_in = 5070
epsg_out = 4326

### OUTPUT Filename ###
ttl_file = ttl_dir / f'us_usgs-hydrogeologic-settings2.ttl'

logname = log_dir / f'log_US_USGS-Hydrogeologic-Settings2ttl.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')

def initial_kg(_PREFIX: dict) -> Graph:
    '''Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    '''
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def add_provenance(kg: Graph) -> Graph:
    prefix = 'us_hg_set_data'
    dataset = 'sourceDataset.HydrogeologicSettings'
    kg.add((ontologyIRI, RDF.type, OWL.Ontology))
    kg.add((ontologyIRI, _PREFIX['dcterms']['issued'], Literal(ttl_issued_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['dcterms']['modified'], Literal(ttl_modified_date, datatype=XSD.date)))
    kg.add((ontologyIRI, PROV.wasDerivedFrom, _PREFIX[prefix][dataset]))
    kg.add((ontologyIRI, OWL.versionInfo, Literal(ttl_version, datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], RDF.type, _PREFIX['stad']['Dataset']))
    kg.add((_PREFIX[prefix][dataset], RDFS.label, Literal('Hydrogeologic Settings of the Conterminous US', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['issued'], Literal(data_issued_date, datatype=XSD.date)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['source'], URIRef('https://www.sciencebase.gov/catalog/item/5e43efc3e4b0edb47be84c3d')))
    kg.add((_PREFIX[prefix][dataset], RDFS.comment, Literal('part of "Data for depth of groundwater used for drinking-water supplies in the United States"', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['stad']['hasSpatialCoverage'], _PREFIX['kwgr']['admininstrativeRegion.USA']))
    return kg


def build_iris(objectid: int | str, _PREFIX: dict) -> tuple:
    '''Create IRIs for an aquifer and its geometry

    :param objectid: The unique id value for an aquifer
    :param _PREFIX:
    :return: a tuple with the two IRIs
    '''
    base_iri = f'd.USGS_HG_Setting_{str(objectid)}'
    return _PREFIX['us_hg_set_data'][base_iri], _PREFIX['us_hg_set_data'][base_iri + '.geometry']


def get_lithology(lith: str) -> str:
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
    elif lith == None:
        return 'Unspecified'
    else:
        raise ValueError('Unexpected Lithology from hydrogeologic settings shape file')


def process_hgsetting_shp2ttl(infile: Path, outfile: Path, epsg_in: int, epsg_out: int):
    '''Triplifies the hydrogeologic setting data in a .shp file and saves the result as a .ttl file

    :param infile: a .shp file with NHD water body data
    :param outfile: the path and name for the .ttl file
    :return:
    '''
    logger.info(f'Load hydrogeologic setting shapefile from {infile}')
    gdf_hgsettings = gpd.read_file(infile)
    logger.info(f'Convert CRS from EPSG:{epsg_in} to EPSG:{epsg_out}')
    gdf_hgsettings.set_crs(epsg=epsg_in, inplace=True)
    gdf_hgsettings.to_crs(epsg=epsg_out, inplace=True)

    logger.info('Intialize RDFLib Graph')
    kg = initial_kg(_PREFIX)  # Create an empty Graph() with SAWGraph namespaces
    kg = add_provenance(kg)
    logger.info(f'Triplify hydrogeologic settings')
    for row in gdf_hgsettings.itertuples():
        # Get IRIs for the current HG setting and its geometry
        hgsiri, geomiri = build_iris(row.PASHR_ID + '-' + row.Overlay, _PREFIX)
        kg.add((hgsiri, RDF.type, _PREFIX['gwml2']['GW_Aquifer']))

        # Triplify the geometry for the current HG settings
        kg.add((hgsiri, GEO.hasGeometry, geomiri))
        kg.add((hgsiri, GEO.defaultGeometry, geomiri))
        kg.add((geomiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg.add((geomiri, RDF.type, GEO.Geometry))

        # Triplify current HG settings attributes
        base_iri = f'd.USGS_HG_Setting_{row.PASHR_ID}-{row.Overlay}'
        kg.add((hgsiri, _PREFIX['us_hg_set']['hasHGSettingId'], Literal(row.PASHR_ID + '-' + row.Overlay, datatype=XSD.string)))
        kg.add((hgsiri, _PREFIX['us_hg_set']['hasOverlay'], _PREFIX['us_hg_set'][f'Overlay.{row.Overlay}']))
        kg.add((hgsiri, _PREFIX['us_hg_set']['hasHGSettingName'], Literal(row.HG_Setting, datatype=XSD.string)))
        kg.add((hgsiri, _PREFIX['us_hg_set']['hasLithology'], _PREFIX['us_hg_set'][f'Lithology.{get_lithology(row.Lithology)}']))

        medians = { 'DomesticMedianTopDepth': row.DomMedTop,
                    'DomesticMedianBottomDepth': row.DomMedBot,
                    'DomesticMedianOpenIntervalLength': row.DomMedOL,
                    'PublicMedianTopDepth': row.PubMedTop,
                    'PublicMedianBottomDepth': row.PubMedBot,
                    'PublicMedianOpenIntervalLength': row.PubMedOL }
        for k, v in medians.items():
            kg.add((hgsiri, _PREFIX['us_hg_set']['has' + k], _PREFIX['us_hg_set_data'][base_iri + '.' + k]))
            kg.add((_PREFIX['us_hg_set_data'][base_iri + '.' + k], RDF.type, _PREFIX['us_hg_set'][k]))
            kg.add((_PREFIX['us_hg_set_data'][base_iri + '.' + k], _PREFIX['qudt']['hasQuantityValue'], _PREFIX['us_hg_set_data'][base_iri + '.' + k + '.QV']))
            kg.add((_PREFIX['us_hg_set_data'][base_iri + '.' + k + '.QV'], RDF.type, _PREFIX['qudt']['QuantityValue']))
            kg.add((_PREFIX['us_hg_set_data'][base_iri + '.' + k + '.QV'], _PREFIX['qudt']['numericValue'], Literal(v, datatype=XSD.decimal)))
            kg.add((_PREFIX['us_hg_set_data'][base_iri + '.' + k + '.QV'], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))

    logger.info(f'Write hydrogeologic settings triples to {outfile}')
    kg.serialize(outfile, format='turtle')  # Write the completed KG to a .ttl file


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script')
    process_hgsetting_shp2ttl(hgsettings_file, ttl_file, epsg_in, epsg_out)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
