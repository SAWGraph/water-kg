"""Create a .ttl file for Illinois aquifers from a .shp files containing fixed aquifer geometries

Under ### INPUT Filenames ###, define
    the name (and path) of the input .shp files
Under ### OUTPUT Filenames ###, define
    the name (and path) of the output .shp files (for the processed aquifer layers)
    the name (and path) of the output .ttl file for aquifers
    the name (and path) of the output .ttl file for aquifer systems

Required:
    * geopandas
    * pandas
    * shapely (LineString, Point, and Polygon)
    * rdflib (Graph and Literal)
    * rdflib.namespace (GEO, PROV, RDF, RDFS, and XSD)
    * namespaces (a local .py file with a dictionary of project namespaces)

Functions:
    * namestr - takes an object and returns a string version of its variable name
    * print_gdf_info - takes a GeoDataFrame (gdf) and prints its variable name, column names, EPSG value,
                       and size to the console
    * read_shp_2_gdf - takes a .shp file and returns a gdf
    * dissolve_on_attribute - takes a gdf and an attribute name, dissolves on the attribute, and returns a gdf
    * convert_crs - takes a gdf and an EPSG value and returns a gdf
    * dissolve_spatially - takes a gdf and an EPSG value, dissolves all features spatially, explodes the dissolve,
                           assigns the EPSG (this must be the same as the input gdf), and returns a gdf
    * spatial_join_ids - takes two gdfs and a common attribute name, does a left spatial join on the two gdfs,
                         renames the index from the right gdf, and returns a gdf
    * create_id_dict - takes a gdf and creates a dictionary of dissolved ids to lists of original ids
    * process_aquifers_shp2shp - takes a .shp file, processes it, saves the result as a .shp file, and returns a
                                 dictionary of dissolved ids to lists of original ids
    * initial_kg - takes a dictionary of prefixes and returns an empty RDFLib knowledge graph
    * build_iris - takes an id value and a dictionary of prefixes and returns IRIs for an aquifer and its geometry
    * process_aquifers_shp2ttl - takes two .shp files (aquifers and S2 cells), an output file name, and a dictionary
                                 of dissolved ids to lists of original ids, and creates and saves a .ttl file
"""

import geopandas as gpd
import pandas as pd
from shapely import LineString, Point, Polygon
from rdflib import Graph, Literal
from rdflib.namespace import GEO, DCTERMS, OWL, PROV, RDF, RDFS, SDO, XSD

import logging
import time
import datetime

import sys
import os

# Modify the system path to find namespaces.py
sys.path.insert(1, 'G:/My Drive/Laptop/SAWGraph/Data Sources')
from namespaces import _PREFIX, find_s2_intersects_poly

# Set the current directory to this file's directory
os.chdir('G:/My Drive/Laptop/SAWGraph/Data Sources/Hydrology/Groundwater')

### INPUT Filename ###
# isgs_bedrocklt500_aq_shp_path: Illinois major bedrock aquifers (at least 70 gpm)
# isgs_sandgravel_aq_shp_path: Illinois major sand and gravel aquifers (at least 70 gpm)
# isgs_coarsemtls_aq_shp_path: Illinois coarse-grained materials potential aquifers (5 to 70 gpm)
isgs_bedrocklt500_aq_shp_path = '../../Geospatial/Illinois/IL_Major_Aquifers/il_bedrock_lt500ft_aqs.shp'
isgs_sandgravel_aq_shp_path = '../../Geospatial/Illinois/IL_Major_Aquifers/il_maj_sand_gravel_aqs.shp'
isgs_coarsemtls_aq_shp_path = '../../Geospatial/Illinois/IL_Major_Aquifers/il_shallow_coarse_mtls_fixed_aqs.shp'

### OUTPUT Filenames ###
# isgs_coarsemtls_aqsys_shp_path: the final saved output from the .shp processing steps; also an input to triplification
#                                 it consists of dissolved coarse-grained materials aquifers to create aquifer systems
# aq_ttl_file: the resulting (output) .ttl file for aquifers
# aqsys_ttl_file: the resulting (output) .ttl file for aquifer systems
isgs_coarsemtls_aqsys_shp_path = '../../Geospatial/Illinois/IL_Major_Aquifers/il_shallow_coarse_mtls_fixed_aq_sys.shp'
aq_ttl_file = 'ttl_files/il_17_isgs_aquifers.ttl'
aqsys_ttl_file = 'ttl_files/il_17_saw_aqsystems.ttl'

### VARIABLES ###
# When True, prints column names, epsg value, and size (rows & columns) for each processing step GeoDataFrame
# When False, a brief statement is logged acknowledging a step is complete
diagnostics = False
# flow_rates is a list of 'SYMBOLOGY' values to keep in the processed aquifer file
# dissolve_attr_1 is the id column for aquifers
# dissolve_attr_2 is the id column for the connected aquifers
dissolve_attr_1 = 'fid'
dissolve_attr_2 = 'saw_id'
epsg_working = 4269  # Default for the input shape files
epsg_final = 4326  # WGS 84, the default CRS for GeoSPARQL
# aquifer id values are padded with leading zeros so they are all a fixed length
# max_id_length should be set to the maximum expected length of an id value (or longer)
max_id_length = 4

logname = 'logs/log_IL_ISGS_Aquifers-2-ttl_aqsystems.txt'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


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


def read_shp_2_gdf(path, diag):
    """Reads a .shp file and converts it to a GeoDataFrame

    :param path: a path to a .shp file
    :param diag: if True the function logs more detailed info than when it is False
    :return: a GeoDataFrame
    """
    gdfout = gpd.read_file(path)
    log_gdf_info(gdfout, 'Shapefile imported') if diag else logger.info('Shapefile imported')
    return gdfout


def dissolve_on_attribute(gdfin, attr, diag):
    """Dissolves a GeoDataFrame based on a given attribute

    :param gdfin: a GeoDataFrame
    :param attr: the attribute with values for dissolving on
    :param diag: if True the function logs more detailed info than when it is False
    :return: a GeoDataFrame
    """
    gdfout = gdfin.dissolve(by=attr)
    log_gdf_info(gdfout, f'Dissolve on {attr}') if diag else logger.info(f'Polygons dissolved on {attr}')
    return gdfout


def convert_crs(gdfin, epsg, diag):
    """Convert a GeoDataFrame to a desired EPSG

    :param gdfin: a GeoDataFrame
    :param epsg: the new EPSG value
    :param diag: if True the function logs more detailed info than when it is False
    :return: a GeoDataFrame
    """
    gdfout = gdfin.to_crs(epsg=epsg)
    log_gdf_info(gdfout, f'Convert to EPSG {epsg}') if diag else logger.info(f'CRS changed to EPSG {epsg}')
    return gdfout


def dissolve_spatially(gdfin, epsg, diag):
    """Performs a spatial dissolve on a GeoDataFrame of polygons

    :param gdfin: a GeoDataFrame
    :param epsg: the EPSG of the input GeoDataFrame (it is lost during the spatial dissolve and must be reset)
    :param diag: if True the function logs more detailed info than when it is False
    :return: a GeoDataFrame
    """
    gdfout = gpd.GeoDataFrame(geometry=[gdfin.unary_union]).explode(index_parts=False).reset_index()
    gdfout.set_crs(epsg=epsg, inplace=True)
    gdfout.index += 1
    log_gdf_info(gdfout, 'Spatial dissolve') if diag else logger.info(
        f'Polygon layer dissolved spatially, CRS set to EPSG {epsg}')
    return gdfout


def spatial_join_ids(gdf_left, gdf_right, idname1, idname2, diag):
    """Takes two GeoDataFrames and does a left spatial join based on their intersections

    :param gdf_left: a GeoDataFrame
    :param gdf_right: a GeoDataFrame
    :param idname1: name for a column of ids from the left GeoDataFrame
    :param idname2: name for the index column from the right GeoDataFrame
    :param diag: if True the function logs more detailed info than when it is False
    :return: a GeoDataFrame
    """
    gdfout = gdf_left.sjoin(gdf_right, how='left', predicate='intersects')
    gdfout.drop(columns=['index'], inplace=True)
    gdfout.rename(columns={'index_right': idname2}, inplace=True)
    gdfout[idname1] = pd.to_numeric(gdfout[idname1]).astype('Int64')
    gdfout[idname2] = pd.to_numeric(gdfout[idname2]).astype('Int64')
    log_gdf_info(gdfout, f'Spatially join {idname2}') if diag else logger.info(
        f'Spatial join of new {idname2} attribute complete')
    return gdfout


def create_id_dict(gdf):
    """Essentially connects original aquifer ids to dissolved aquifer ids

    :param gdf: a GeoDataFrame
    :return: a dictionary
    """
    dic = {}
    for row in gdf.itertuples():
        dic[int(round(row.fid, 0))] = row.saw_id
    logger.info('Dictionary of old versus new IDs created')
    return dic


def process_aquifers_shp2shp(infile, outfile, diag):
    """A function that carries out a complete sequence of geospatial processing on a .shp file
       The result is saved as a .shp file

    :param infile: a path to a .shp file
    :param outfile: a path and name for the resulting .shp file
    :param diag: if True the called functions log more detailed info than when it is False
    :return: a dictionary
    """
    logger.info('BEGIN PROCESSING THE COARSE MATERIALS AQUIFERS SHAPEFILE')
    gdf_initial = read_shp_2_gdf(infile, diag)
    gdf_dissolved = dissolve_spatially(gdf_initial, epsg_working, diag)
    gdf_joined = spatial_join_ids(gdf_initial, gdf_dissolved, dissolve_attr_1, dissolve_attr_2, diag)
    gdf_dissolved_2 = dissolve_on_attribute(gdf_joined, dissolve_attr_2, diag)
    gdf_final = convert_crs(gdf_dissolved_2, epsg_final, diag)
    gdf_final.drop(columns=['fid'], inplace=True)
    gdf_final.to_file(outfile)
    logger.info('COARSE MATERIALS AQUIFER SHAPEFILE PROCESSING COMPLETE')
    return create_id_dict(gdf_joined)


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


def build_aqsys_iris(aqsysid, _PREFIX):
    """Create IRIs for an aquifer and its geometry

    :param aqsysid: The id value for an aquifer system
    :param _PREFIX: a dictionary of prefixes
    :return: a tuple with the two IRIs
    """
    return (_PREFIX["il_isgs_data"]['d.SAW-Aquifer-System.CM' + str(aqsysid).zfill(max_id_length)],
            _PREFIX["il_isgs_data"]['d.SAW-Aquifer-System.Geometry.CM' + str(aqsysid).zfill(max_id_length)])


def process_aquifers_shp2ttl(br_infile, sg_infile, cg_infile, cgsys_infile, outfile1, outfile2, ids_dict):
    """Triplifies the aquifer data in from a set of .shp files and saves the result as a .ttl file

    :param br_infile: bedrock aquifer .shp file
    :param sg_infile: sand and gravel aquifer .shp file
    :param cg_infile: coarse-grained materials potential aquifer .shp file
    :param cgsys_infile: coarse-grained materials potential aquifer systems .shp file
    :param outfile1: the path and name for the aquifers .ttl file
    :param outfile2: the path and name for the aquifer systems .ttl file
    :param ids_dict: a dictionary of dissolved ids to lists of original ids
    :return:
    """
    logger.info('BEGIN TRIPLIFYING THE AQUIFERS')
    logger.info('Loading the shapefiles')
    gdf_bedrock_aqs = gpd.read_file(br_infile)
    gdf_sandgravel_aqs = gpd.read_file(sg_infile)
    gdf_coarsemtls_aqs = gpd.read_file(cg_infile)
    gdf_coarsemtls_aqsys = gpd.read_file(cgsys_infile)
    list_aqs = [gdf_bedrock_aqs, gdf_sandgravel_aqs, gdf_coarsemtls_aqs]
    logger.info('Intializing the knowledge graph')
    kg_aq = initial_kg(_PREFIX)
    kg_aqsys = initial_kg(_PREFIX)
    logger.info('Creating the triples')
    ordinals = ['first', 'second', 'third', 'fourth']
    count = 0
    for gdf in list_aqs:
        logger.info(f'   Processing {ordinals[count]} set of aquifers (of four)')
        count += 1
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
            kg_aq.add((aqiri, RDF.type, _PREFIX['gwml2']['GW_Aquifer']))
            kg_aq.add((aqiri, _PREFIX['il_isgs']['ilSawAqId'], Literal(aqid, datatype=XSD.string)))
            kg_aq.add((aqiri, _PREFIX['saw_water']['aquiferType'], Literal(row.aqtype, datatype=XSD.string)))
            kg_aq.add((aqiri, RDFS.label, Literal(f'A {row.aqtype} aquifer in Illinois', datatype=XSD.string)))
            if row.aqtype.lower() == 'coarse-grain_materials':
                sysid = str(ids_dict[fid])
                aqsysiri = build_aqsys_iris(sysid, _PREFIX)[0]
                kg_aq.add((aqiri, _PREFIX['gwml2']['gwAquiferSystem'], aqsysiri))
                kg_aqsys.add((aqsysiri, _PREFIX['gwml2']['gwAquiferSystemPart'], aqiri))
            kg_aq.add((aqiri, GEO.hasGeometry, geoiri))
            kg_aq.add((aqiri, GEO.defaultGeometry, geoiri))
            kg_aq.add((geoiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
            kg_aq.add((geoiri, RDF.type, GEO.Geometry))
            if 'multipolygon' in str(row.geometry).lower():
                kg_aq.add((geoiri, RDF.type, _PREFIX['sf']['MultiPolygon']))
            else:
                kg_aq.add((geoiri, RDF.type, _PREFIX['sf']['Polygon']))
    logger.info(f'   Processing {ordinals[count]} set of aquifers (of four)')
    for row in gdf_coarsemtls_aqsys.itertuples():
        aqsysiri, geoiri = build_aqsys_iris(row.saw_id, _PREFIX)
        kg_aqsys.add((aqsysiri, RDF.type, _PREFIX['gwml2']['GW_AquiferSystem']))
        kg_aqsys.add((aqsysiri, _PREFIX['il_isgs']['ilSawAqSysId'],
                   Literal('CM' + str(row.saw_id).zfill(max_id_length), datatype=XSD.string)))
        kg_aqsys.add((aqsysiri, RDFS.label, Literal('A system of aquifers in Illinois', datatype=XSD.string)))
        kg_aqsys.add((aqsysiri, RDFS.comment, Literal(
            f'Illinois aquifer systems consist of adjacent potential aquifers in coarse-grained materials within 50ft of the ground surface',
            datatype=XSD.string)))
        kg_aqsys.add((aqsysiri, GEO.hasGeometry, geoiri))
        kg_aqsys.add((aqsysiri, GEO.defaultGeometry, geoiri))
        kg_aqsys.add((geoiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        kg_aqsys.add((geoiri, RDF.type, GEO.Geometry))
        if 'multipolygon' in str(row.geometry).lower():
            kg_aqsys.add((geoiri, RDF.type, _PREFIX['sf']['MultiPolygon']))
        else:
            kg_aqsys.add((geoiri, RDF.type, _PREFIX['sf']['Polygon']))
    kg_aq.serialize(outfile1, format='ttl')
    kg_aqsys.serialize(outfile2, format='ttl')
    logger.info('TRIPLIFYING COMPLETE AND .ttl FILE CREATED')


if __name__ == '__main__':
    start_time = time.time()
    ids = process_aquifers_shp2shp(isgs_coarsemtls_aq_shp_path, isgs_coarsemtls_aqsys_shp_path, diagnostics)
    process_aquifers_shp2ttl(isgs_bedrocklt500_aq_shp_path, isgs_sandgravel_aq_shp_path, isgs_coarsemtls_aq_shp_path,
                             isgs_coarsemtls_aqsys_shp_path, aq_ttl_file, aqsys_ttl_file, ids)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS\n')
    print(f'\nRuntime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
