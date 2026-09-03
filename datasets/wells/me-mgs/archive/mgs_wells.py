import os
from rdflib.namespace import OWL, XMLNS, XSD, RDF, RDFS
from rdflib import Namespace
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
import pandas as pd
import shapely
import encodings
import logging
import csv
from datetime import datetime
import sys
import math
import json
import numpy as np
from datetime import date
from pyutil import *
from pathlib import Path



## importing utility/variable file
code_dir = Path(__file__).resolve().parent.parent.parent.parent
# print(code_dir)
sys.path.insert(0, str(code_dir))
# from datasets.wells.me-mgs.variable import NAME_SPACE, _PREFIX
from variable import NAME_SPACE, _PREFIX
# from datasets import utilities


## declare variables
logname = "log"

## data path
root_folder = Path(__file__).resolve().parent.parent.parent
data_dir = root_folder / "data/mgs_wells/"
metadata_dir = root_folder / "data/mgs_wells/metadata/"
output_dir = root_folder / "wells/me-mgs/ttl_files/"

me_mgs = Namespace(f"http://sawgraph.spatialai.org/v1/me-mgs#")
me_mgs_data = Namespace(f"http://sawgraph.spatialai.org/v1/me-mgs-data#")


## data dictionaries -- for controlled vocabularies

# with open(metadata_dir + 'analysis_lab.csv', mode='r') as infile:
#     reader = csv.reader(infile)
#     lab_dict = {rows[1]: rows[0] for rows in reader}


## initiate log file
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info("Running triplification for MGS Wells")

def main():
    #unlocated wells
    mgs_wells_unlocated_df = pd.read_csv(data_dir / 'Maine_Well_Database_-_Unlocated_Wells.csv', header=0, low_memory=False)
    logger.info('MGS unlocated wells data loaded to dataframe.')

    kg, towns = triplify_well_data(mgs_wells_unlocated_df, _PREFIX)
    kg_turtle_file = output_dir / "mgs_wells_unlocated_output.ttl"
    kg.serialize(kg_turtle_file, format='turtle')
    towns.serialize(output_dir / 'towns_unlocated.ttl', format='turtle')
    logger.info('Finished triplifying MGS unlocated well data.')

    #located wells
    mgs_wells_located_df = pd.read_csv(data_dir / 'Maine_Well_Database_-_Well_Depth.csv', header=0,
                                         encoding='ISO-8859-1')
    logger.info('MGS located wells data loaded to dataframe.')

    kg2, towns2 = triplify_well_data(mgs_wells_located_df, _PREFIX)
    kg_turtle_file = output_dir / "mgs_wells_located_output.ttl"
    kg2.serialize(kg_turtle_file, format='turtle')
    towns2.serialize(output_dir / 'towns_located.ttl', format='turtle')
    logger.info('Finished triplifying MGS located well data.')


def Initial_KG(_PREFIX):
    prefixes: Dict[str, str] = _PREFIX
    kg = Graph()
    for prefix in prefixes:
        kg.bind(prefix, prefixes[prefix])
    kg.bind('me_mgs', me_mgs)
    kg.bind('me_mgs_data', me_mgs_data)
    return kg

def get_attributes(row):
    #this attribute schema works for MGS well data
    well_no = row['WELLNO']  # well number
    well_use = str(row['WELL_USE']).lower().title().replace(', ', '')  # well use
    well_type = str(row['WELL_TYPE']).lower().title().replace(' ', '')  # well type
    well_depth = row['WELL_DEPTH_FT']
    well_overburden = row['OVERBURDEN_THICKNESS_FT']
    well_iri = me_mgs_data.term(f"d.MGS-Well.{well_no}")
    #print('well_iri: ', well_iri)
    # town
    town_name_formatted = str(row['WELL_LOCATION_TOWN'])

    #town_iri = _PREFIX["aik-pfas"][f"{'town'}.{town_name_formatted}"]
    try:
        well_point = shapely.Point((row['LONGITUDE'], row['LATITUDE']))
        geom = well_point.wkt
        # print(f'Shapely point: {well_point}; WKT point: {geom}')
    except:
        geom = None

    return well_no, well_use, well_type, well_depth, well_overburden, well_iri, town_name_formatted, geom


## triplify the abox
def triplify_well_data(df, _PREFIX):
    kg = Initial_KG(_PREFIX)
    kg2 = Initial_KG(_PREFIX)
    get_towns = False
    ## materialize each well record
    # df.info()

# <<<<<<< HEAD
#     if get_towns:
# =======
    if get_towns:
# >>>>>>> 6768acf (Add maine and illinois well scripts,  readmes, and schemas)
        #get dcids for each unique town
        towns = df.WELL_LOCATION_TOWN.unique()
        town_dcid = {}
        for town in towns:
            town_name_formatted = str(town)+" town, MAINE"
            resp = utilities.resolvePlaceName(town_name_formatted)
            #print(town_name_formatted, resp.text)
            try:
                dcids = resp.json()['entities'][0]['resolvedIds']
            except:
                dcids = []
            town_dcid[town] = dcids
        with open('towns.txt', 'w') as town_dictionary:
            town_dictionary.write(json.dumps(town_dcid))
    else:
        with open('towns.txt', 'r') as town_file:
            town_dcid = json.load(town_file)
            # print(town_dcid)
    for town in town_dcid.keys():
        # print(town, town_dcid[town])
        if town_dcid[town] != []:
            for place in town_dcid[town]:
                kg2.add((_PREFIX['dc'][place], RDF.type, _PREFIX['kwg-ont']["AdministrativeRegion_3"]))

    for idx, row in df.iterrows():

        well_no, well_use, well_type, well_depth, well_overburden, well_iri, town_name_formatted, geom = get_attributes(row)

        # well instance
        kg.add((well_iri, RDF.type, me_mgs["MGS-Well"]))
        kg.add((well_iri, RDFS['label'], Literal('MGS well ' + str(well_no))))

        # well type
        if well_type != 'Nan':
            kg.add((well_iri, me_mgs["ofWellType"], me_mgs_data['d.wellType.' + well_type]))
        # well use
        if well_use != 'Nan':
            kg.add((well_iri, me_mgs["hasUse"], me_mgs_data['d.wellUse.' + well_use]))
        # well depth
        kg.add((well_iri, me_mgs['wellDepth'],
                me_mgs_data["d.WellDepthInFt." + 'MGS-Well.' + str(well_no)]))
        kg.add((me_mgs_data["d."+"WellDepthInFt." +'MGS-Well.' + str(well_no)], _PREFIX["qudt"]["numericValue"],
               Literal(float(well_depth), datatype=XSD.float)))
        #print(well_overburden, type(well_overburden))
        if pd.isna(well_overburden)==False:
            kg.add((well_iri, me_mgs['wellOverburden'], me_mgs_data["d.WellOverburdenInFt." + 'MGS-Well.' + str(well_no)]))
            kg.add(( me_mgs_data["d.WellOverburdenInFt." + 'MGS-Well.' + str(well_no)], _PREFIX["qudt"]["numericValue"], Literal(float(well_overburden), datatype=XSD.float)))
        # well depth unit will be added through OWL restriction
        # kg.add((_PREFIX["aik-pfas-ont"]["WellDepthInFt."+well_iri], _PREFIX["qudt"]["unit"], _PREFIX["qudt"]["FT"]))

        # well geometry
        if geom is not None:
            # extract the geometry
            well_geometry_iri = me_mgs_data[f"d.MGS-Well-Geometry.{well_no}"]
            kg.add((well_iri, _PREFIX['geo']['hasGeometry'], well_geometry_iri))
            kg.add((well_iri, _PREFIX['geo']['defaultGeometry'], well_geometry_iri))
            kg.add((well_geometry_iri, _PREFIX["geo"]["asWKT"], Literal(geom, datatype=_PREFIX["geo"]["wktLiteral"])))
            kg.add((well_geometry_iri, RDF.type, _PREFIX['geo']['Geometry']))

        
        # todo lookup FIPS code for town
        #kg.add((well_iri, _PREFIX["aik-pfas"]['locatedIn'], town_iri))
        if town_name_formatted in town_dcid.keys():
            for place in town_dcid[town_name_formatted]:
                    kg.add((well_iri, _PREFIX['kwg-ont']['sfWithin'], _PREFIX['dc'][place]))

        #if idx == 5:
            #break


    # T-box lists
    f_type=open("well_types.txt", "w")
    f_use=open("well_uses.txt", "w")

    well_types = df.WELL_TYPE.unique().flatten()
    # print('well types: ', well_types)
    for t in well_types:
        wt = str(t).lower().title().replace(' ', '')
        if wt != 'Nan':
            #kg.add((_PREFIX["aik-pfas"]["d.wellType." + wt], RDF.type, _PREFIX["aik-pfas-ont"]['MGS-WellType']))
            f_type.write(wt)
    f_type.close()

    well_use = df.WELL_USE.unique().flatten()
    # print('well use: ', well_use)
    for t in well_use:
        wu = str(t).lower().title().replace(', ', '')
        if wu != 'Nan':
            #kg.add((_PREFIX["aik-pfas"]["d.wellUse." + wt], RDF.type, _PREFIX["aik-pfas-ont"]['MGS-WellUse']))
            f_use.write(wu)
    f_use.close()

    return kg, kg2


## utility functions

def is_valid(value):
    if math.isnan(float(value)):
        return False
    else:
        return True


def rem_time(d):
    s = date(d.year, d.month, d.day)
    return s


if __name__ == "__main__":
    main()
