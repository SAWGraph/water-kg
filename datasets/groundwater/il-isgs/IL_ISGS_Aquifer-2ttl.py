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
    * namestr - takes an object and returns a string version of its variable name
    * log_gdf_info - takes a GeoDataFrame (gdf) and prints its variable name, column names, EPSG value,
                     and size to the console
    * read_shp_2_gdf - takes a .shp file and returns a gdf
    * convert_crs - takes a gdf and an EPSG value and returns a gdf
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for an aquifer and its geometry
    * process_aquifers_shp2ttl - takes two .shp files (aquifers and S2 cells), an output file name, and a dictionary
                                 of dissolved ids to lists of original ids, and creates and saves a .ttl file
"""

import geopandas as gpd
from pathlib import Path
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import GEO, RDF, RDFS, XSD

import logging
import time
import datetime

import sys
import os

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

### OUTPUT Filenames ###
# aq_ttl_file: the resulting (output) .ttl file for aquifers
aq_ttl_file = ttl_dir / 'il_17_isgs_aquifers2.ttl'

### VARIABLES ###
epsg_working = 4269  # Default for the input shape files
epsg_final = 4326  # WGS 84, the default CRS for GeoSPARQL
# aquifer id values are padded with leading zeros so they are all a fixed length
# max_id_length should be set to the maximum expected length of an id value (or longer)
max_id_length = 4

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


def namestr(obj, namespace):
    """Return the name of an object

    :param obj: A python object
    :param namespace: The object's namespace [globals() is the typical choice here]
    :return: The object's name; i.e., for some variable storing some object this returns the variable name
    """
    return [name for name in namespace if namespace[name] is obj][0]


def log_gdf_info(gdf, step):
    """Log diagnostic information for a GeoDataFrame

    :param gdf: a GeoDataFrame
    :param step: a text string describing the current processing step
    """
    # print(f'Dataframe: {namestr(gdf, globals())}')
    logger.info(f'Step: {step}')
    logger.info(f'Columns: {gdf.columns}')
    logger.info(f'EPSG: {gdf.crs.to_epsg()}')
    logger.info(f'Rows: {gdf.shape[0]}; Columns: {gdf.shape[1]}\n')


def read_shp_2_gdf(path):
    """Reads a .shp file and converts it to a GeoDataFrame

    :param path: a path to a .shp file
    :param diag: if True the function logs more detailed info than when it is False
    :return: a GeoDataFrame
    """
    logger.info(f'Importing shapefile from {path}')
    gdfout = gpd.read_file(path)
    return gdfout


def convert_crs(gdfin, epsg):
    """Convert a GeoDataFrame to a desired EPSG

    :param gdfin: a GeoDataFrame
    :param epsg: the new EPSG value
    :param diag: if True the function logs more detailed info than when it is False
    :return: a GeoDataFrame
    """
    gdfout = gdfin.to_crs(epsg=epsg)
    logger.info(f'CRS changed to EPSG {epsg}')
    return gdfout


def initial_kg(_PREFIX):
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


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