"""Create a .ttl file for Illinois aquifers from a .shp files containing fixed aquifer geometries

Under ### INPUT Filenames ###, define
    the name (and path) of the input .shp files
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
"""

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
data_issued_date = '2004-04-01'
# aquifer id values are padded with leading zeros so they are all a fixed length
# max_id_length should be set to the maximum expected length of an id value (or longer)
max_id_length = 4

# Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent.parent
data_dir = cwd.parent.parent / "data"
ttl_dir = cwd / "ttl_files"
log_dir = cwd / "logs"
# print(f"Current working directory:      {cwd}")
# print(f"Github repos and namespaces.py: {ns_dir}")
# print(f"Data (input) directory:         {data_dir}")
# print(f"Turtle (output) directory:      {ttl_dir}")
# print(f"Logging directory:              {log_dir}")

# Modify the system path to find namespaces.py
sys.path.insert(0, str(ns_dir))
from namespaces2 import _PREFIX
ontologyIRI = URIRef('http://w3id.org/hyfo/il-isgs/v1/il-isgs-data')

# Set the current directory to this file's directory
os.chdir(cwd)

### INPUT Filename ###
# isgs_bedrocklt500_aq_shp_path: Illinois major bedrock aquifers (at least 70 gpm)
# isgs_sandgravel_aq_shp_path: Illinois major sand and gravel aquifers (at least 70 gpm)
# isgs_coarsemtls_aq_shp_path: Illinois coarse-grained materials potential aquifers (5 to 70 gpm)
isgs_bedrocklt500_aq_shp_path = data_dir / 'IL_Major_Aquifers/il_bedrock_lt500ft_aqs.shp'
isgs_sandgravel_aq_shp_path = data_dir / 'IL_Major_Aquifers/il_maj_sand_gravel_aqs.shp'
isgs_coarsemtls_aq_shp_path = data_dir / 'IL_Major_Aquifers/il_shallow_coarse_mtls_fixed_aqs.shp'
epsg_working = 4269  # Default for the input shape files
epsg_final = 4326  # WGS 84, the default CRS for GeoSPARQL

### OUTPUT Filenames ###
# aq_ttl_file: the resulting (output) .ttl file for aquifers
aq_ttl_file = ttl_dir / 'il_17_isgs_aquifers2.ttl'

logname = log_dir / 'log_IL_ISGS_Aquifers-2-ttl.txt'
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
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def add_provenance(kg: Graph) -> Graph:
    prefix = 'il_isgs_data'
    dataset = 'sourceDataset.Aquifers'
    kg.add((ontologyIRI, RDF.type, OWL.Ontology))
    kg.add((ontologyIRI, _PREFIX['dcterms']['issued'], Literal(ttl_issued_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['dcterms']['modified'], Literal(ttl_modified_date, datatype=XSD.date)))
    kg.add((ontologyIRI, _PREFIX['prov']['wasDerivedFrom'], _PREFIX[prefix][dataset]))
    kg.add((ontologyIRI, OWL.versionInfo, Literal(ttl_version, datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], RDF.type, _PREFIX['stad']['Dataset']))
    kg.add((_PREFIX[prefix][dataset], RDFS.label, Literal('Illinois Major Aquifers', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['issued'], Literal(data_issued_date, datatype=XSD.date)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['dcterms']['source'], URIRef('https://clearinghouse.isgs.illinois.edu/data/hydrology/major-aquifers')))
    kg.add((_PREFIX[prefix][dataset], RDFS.comment, Literal('Generalized Statewide Location of Major Bedrock, Sand and Gravel, and Potential Shallow Aquifers in Illinois', datatype=XSD.string)))
    kg.add((_PREFIX[prefix][dataset], _PREFIX['stad']['hasSpatialCoverage'], _PREFIX['kwgr']['admininstrativeRegion.USA.17']))
    return kg


def build_aq_iris(aqid, _PREFIX):
    """Create IRIs for an aquifer and its geometry

    :param aqid: The id value for an aquifer
    :param aqtype: The type of aquifer (expects 'bedrock' or 'sand_gravel' and dfaults to 'coarse-grain_materials'
    :param _PREFIX: a dictionary of prefixes
    :return: a tuple with the two IRIs
    """
    return (_PREFIX["il_isgs_data"]['d.ISGS-Aquifer.' + aqid],
            _PREFIX["il_isgs_data"]['d.ISGS-Aquifer.Geometry.' + aqid])


def process_aquifers_shp2ttl(br_infile, sg_infile, cg_infile, outfile):
    """Triplifies the aquifer data in from a set of .shp files and saves the result as a .ttl file

    :param br_infile: bedrock aquifer .shp file
    :param sg_infile: sand and gravel aquifer .shp file
    :param cg_infile: coarse-grained materials potential aquifer .shp file
    :param outfile: the path and name for the aquifers .ttl file
    :return:
    """
    logger.info('BEGIN TRIPLIFYING THE AQUIFERS')
    logger.info('Loading the shapefiles')
    gdf_bedrock_aqs = gpd.read_file(br_infile)
    gdf_sandgravel_aqs = gpd.read_file(sg_infile)
    gdf_coarsemtls_aqs = gpd.read_file(cg_infile)
    dict_aqs = { 'bedrock': gdf_bedrock_aqs,
                 'sand_gravel':gdf_sandgravel_aqs,
                 'coarse-grain_materials': gdf_coarsemtls_aqs }
    logger.info('Initializing the knowledge graph')
    kg = initial_kg(_PREFIX)
    kg = add_provenance(kg)
    logger.info('Creating the triples')
    for type, gdf in dict_aqs.items():
        logger.info(f'   Processing {type} aquifers')
        for row in gdf.itertuples():
            if row.aqtype.lower() == 'bedrock':
                init = 'BR'
            elif row.aqtype.lower() == 'sand_gravel':
                init = 'SG'
            elif row.aqtype.lower() == 'coarse-grain_materials':
                init = 'CM'
            fid = int(round(row.fid, 0))
            aqid = init + str(fid).zfill(max_id_length)
            aqiri, geoiri = build_aq_iris(aqid, _PREFIX)
            kg.add((aqiri, RDF.type, _PREFIX['gwml2']['GW_Aquifer']))
            kg.add((aqiri, _PREFIX['il_isgs']['ilSawAqId'], Literal(aqid, datatype=XSD.string)))
            kg.add((aqiri, _PREFIX['hyfoplus']['aquiferType'], Literal(row.aqtype, datatype=XSD.string)))
            kg.add((aqiri, RDFS.label, Literal(f'A {row.aqtype} aquifer in Illinois', datatype=XSD.string)))
            kg.add((aqiri, GEO.hasGeometry, geoiri))
            kg.add((aqiri, GEO.defaultGeometry, geoiri))
            kg.add((geoiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
            kg.add((geoiri, RDF.type, GEO.Geometry))
            # if 'multipolygon' in str(row.geometry).lower():
            #     kg.add((geoiri, RDF.type, _PREFIX['sf']['MultiPolygon']))
            # else:
            #     kg.add((geoiri, RDF.type, _PREFIX['sf']['Polygon']))
    kg.serialize(outfile, format='ttl')
    logger.info('TRIPLIFYING COMPLETE AND .ttl FILE CREATED')


if __name__ == '__main__':
    start_time = time.time()
    process_aquifers_shp2ttl(isgs_bedrocklt500_aq_shp_path,
                             isgs_sandgravel_aq_shp_path,
                             isgs_coarsemtls_aq_shp_path,
                             aq_ttl_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS\n')