#import os
from rdflib.namespace import OWL, XMLNS, XSD, RDF, RDFS
from rdflib import Namespace
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
import pandas as pd
import geopandas as gpd
import json
import encodings
import logging
import csv
from datetime import datetime
import sys
import math
import numpy as np
from datetime import date
from pyutil import *
from pathlib import Path
from shapely.geometry import Point

code_dir = Path(__file__).resolve().parent.parent
# print(code_dir)
# sys.path.insert(0, str(code_dir))
# from variable import NAME_SPACE, _PREFIX

## declare variables
logname = "log"

## data path
root_folder = Path(__file__).resolve().parent.parent.parent  # datasets folder
data_dir = root_folder / "data/il-epa/"
metadata_dir = None
output_dir = Path(__file__).resolve().parent

##namespaces
pfas = Namespace(f'http://sawgraph.spatialai.org/v1/pfas#')
coso = Namespace(f'http://sawgraph.spatialai.org/v1/contaminoso#')
geo = Namespace(f'http://www.opengis.net/ont/geosparql#')
qudt = Namespace(f'http://qudt.org/schema/qudt/')
unit = Namespace(f'http://qudt.org/vocab/unit/')
il_isgs = Namespace(f'http://sawgraph.spatialai.org/v1/il-isgs#')
il_isgs_data = Namespace(f'http://sawgraph.spatialai.org/v1/il-isgs-data#')

## initiate log file
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running triplification for tests")


def main():
    '''main function initializes all other functions'''
    df = load_data()
    kg, kg2 = triplify(df)

    kg_turtle_file = "il-isgs-wells.ttl".format(output_dir)
    kg.serialize(kg_turtle_file, format='turtle')
    kg2_turtle_file = 'il-isgs-wellsGeo.ttl'.format(output_dir)
    kg2.serialize(kg2_turtle_file, format='turtle')
    logger = logging.getLogger('Finished triplifying Il wells.')


def load_data():
    json_path = data_dir / 'il-wells.geojson'
    df = gpd.read_file(json_path)
    print(df.info(verbose=True))

    print('Formation:', df.WFORMATION.unique())
    logger = logging.getLogger('Data loaded to dataframe.')
    # print(df)
    return df


def Initial_KG():
    # prefixes: Dict[str, str] = _PREFIX
    kg = Graph()
    # for prefix in prefixes:
    #    kg.bind(prefix, prefixes[prefix])
    kg.bind('il_isgs', il_isgs)
    kg.bind('il_isgs_data', il_isgs_data)
    kg.bind('qudt', qudt)
    kg.bind('unit', unit)
    kg.bind('pfas', pfas)
    kg.bind('coso', coso)
    kg.bind('geo', geo)
    return kg


def get_attributes(row):
    # this is specific to the imported file
    well = {
        'id': row.API_NUMBER,
        'wellType': row.STATUS,
        'purposeDesc': row.STATUSLONG,
        'wkt': f'POINT({row.LONGITUDE} {row.LATITUDE})'  # replace this with geodataframe version?

    }

    if pd.notnull(row.ISWSPNUM):
        well['ISWS'] = int(row.ISWSPNUM)

    if pd.notnull(row.OWNER):
        well['owner'] = row.OWNER

    if pd.notnull(row.FARM_NAME):
        well['name'] = row.FARM_NAME

    if pd.notnull(row.TOTAL_DEPTH):
        well['depth'] = row.TOTAL_DEPTH

    if pd.notnull(row.PUMPGPM):
        well['rate'] = row.PUMPGPM

    return well


def get_iris(well):
    # build iris for any entities

    extra_iris = {
        'well': il_isgs_data['d.ISGS-Well.'+str(well['id'])],
        'purpose': il_isgs_data['d.ISGS-WellPurpose.'+str(well['wellType'])],
        'wellgeo': il_isgs_data['d.ISGS-Well.geometry.'+str(well['id'])]
    }
    if 'depth' in well.keys():
        extra_iris['wellDepth'] = il_isgs_data['d.ISGS-Well.Depth.'+str(well['id'])]

    if 'rate' in well.keys():
        extra_iris['wellYield'] = il_isgs_data['d.ISGS-Well.Yield.' + str(well['id'])]

    return extra_iris


def triplify(df):
    kg = Initial_KG()
    kg2 = Initial_KG()
    for idx, row in df.iterrows():
        pass
        # get attributes
        well = get_attributes(row)
        # get iris
        iris = get_iris(well)

        # create well
        kg.add((iris['well'], RDF.type, il_isgs["ISGS-Well"]))
        if 'ISWS' in well.keys():
                kg.add((iris['well'], il_isgs['hasISWSId'], Literal(well['ISWS'], datatype=XSD.string)))
                #TODO this should map as object property to PWS for illinois
        if 'wellType' in well.keys():
            kg.add((iris['well'], il_isgs['wellPurpose'], iris['purpose']))
            #controlled vocabulary instances
            kg.add((iris['purpose'], RDF.type, il_isgs['WellPurpose']))
            if 'purposeDesc' in well.keys():
                kg.add((iris['purpose'], RDFS.label, Literal(well['purposeDesc'], datatype=XSD.string)))
        if 'owner' in well.keys():
            kg.add((iris['well'], il_isgs['hasOwner'], Literal(well['owner'], datatype=XSD.string)))
            #TODO this should be an object property with instances mapped to agencies etc. 
        if 'name' in well.keys():
            kg.add((iris['well'], RDFS.label, Literal(well['name'], datatype=XSD.string)))
            #this is a poor label on its own as its mostly just a number
        if 'depth' in well.keys():
            kg.add((iris['well'], il_isgs['wellDepth'], iris['wellDepth']))
            kg.add((iris['wellDepth'], RDF.type, il_isgs['WellDepthInFt']))
            kg.add((iris['wellDepth'], qudt['numericValue'], Literal(well['depth'], datatype=XSD.float)))
            #TODO unit?? us foot?
        if 'rate' in well.keys():
            kg.add((iris['well'], il_isgs['wellYield'], iris['wellYield']))
            kg.add((iris['wellYield'], RDF.type, il_isgs['WellYield']))
            kg.add((iris['wellYield'], qudt['numericValue'], Literal(well['rate'], datatype=XSD.float)))
            kg.add((iris['wellYield'], qudt['unit'], unit['GAL_US-PER-MIN']))


        # geometry
        kg2.add((iris['well'], geo['hasGeometry'], iris['wellgeo']))
        kg2.add((iris['wellgeo'], RDF.type, geo['Geometry']))
        kg2.add((iris['wellgeo'], geo["asWKT"], Literal(well['wkt'], datatype=geo["wktLiteral"])))


    return kg, kg2


## utility functions

def is_valid(value):
    if math.isnan(float(value)):
        return False
    else:
        return True


if __name__ == "__main__":
    main()
