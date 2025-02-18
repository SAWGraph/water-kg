import os
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
#print(code_dir)
#sys.path.insert(0, str(code_dir))
#from variable import NAME_SPACE, _PREFIX

## declare variables
logname = "log"
state = "IL"
controlledVocab= True

## data path
root_folder = Path(__file__).resolve().parent.parent.parent
data_dir = root_folder / "data/us-sdwis/"
metadata_dir = None
output_dir = root_folder / "federal/us-sdwis/"

##namespaces

prefixes = {}
prefixes['us_sdwis'] = Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis#')
prefixes['us_sdwis_data'] = Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis-data#')
#prefixes['us_frs'] = Namespace(f"http://sawgraph.spatialai.org/v1/us-frs#")
#prefixes['us_frs_data'] = Namespace(f"http://sawgraph.spatialai.org/v1/us-frs-data#")
prefixes['qudt'] = Namespace(f'https://qudt.org/schema/qudt/')
prefixes['coso'] = Namespace(f'http://sawgraph.spatialai.org/v1/contaminoso#')
prefixes['geo'] = Namespace(f'http://www.opengis.net/ont/geosparql#')
prefixes['sosa'] = Namespace(f'http://www.w3.org/ns/sosa/')
prefixes['gcx']= Namespace(f'http://geoconnex.us/')

## initiate log file
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running triplification for facilities")


def main():
    codes = load_data()
    kg2 = triplify(codes)

    kg2_turtle_file = f"us-sdwis-controlledVocab.ttl".format(output_dir)
    kg2.serialize(kg2_turtle_file, format='turtle')
    logger = logging.getLogger('Finished triplifying SDWIS controlled vocabularies.')

def load_data():
    codes = pd.read_csv(data_dir/'SDWA_REF_CODE_VALUES.csv')

    print(codes.info(verbose=True))
    logger = logging.getLogger('Data loaded to dataframe.')
    return codes


def Initial_KG():
    # prefixes: Dict[str, str] = _PREFIX
    kg = Graph()
    for prefix in prefixes:
        kg.bind(prefix, prefixes[prefix])
    return kg


def get_iris(facility):
    iris = {}

    if 'Type' in facility.keys():
        iris['type'] = prefixes['us_sdwis_data']['d.PWS-SubFeatureType.'+facility['Type']]
    if 'Active' in facility.keys():
        iris['activity'] = prefixes['us_sdwis_data']['d.PWS-SubFeatureActivity.'+ facility['Active']]

    if 'SourceType' in facility.keys():
        iris['sourceType'] = prefixes['us_sdwis_data']['d.PWS-WaterSourceType.'+facility['SourceType']]

    if 'serviceAreaType' in facility.keys():
        iris['serviceAreaType'] = prefixes['us_sdwis_data']['d.PWS-ServiceArea-'+ facility['serviceAreaType']]
    #print(iris)
    return iris


def triplify(codes):

    #Controlled Vocabs
    kg2 = Initial_KG()
    facility_type= codes[codes['VALUE_TYPE']=='FACILITY_TYPE_CODE']
    #facility type controlled vocab
    for idx, row in facility_type.iterrows():
        facility = {}
        facility['Type']=row['VALUE_CODE']
        iris = get_iris(facility)
        kg2.add((iris['type'], RDF.type, prefixes['us_sdwis']['PWS-SubFeatureType']))
        kg2.add((iris['type'], RDFS.label, Literal(row['VALUE_DESCRIPTION'])))

    activity_type = codes[codes['VALUE_TYPE']=='ACTIVITY_CODE']
    for idx, row in activity_type.iterrows():
        facility = {}
        facility['Active']=row['VALUE_CODE']
        iris = get_iris(facility)
        kg2.add((iris['activity'], RDF.type, prefixes['us_sdwis']['PWS-SubFeatureActivity']))
        kg2.add((iris['activity'], RDFS.label, Literal(row['VALUE_DESCRIPTION'])))

    serviceAreaType = codes[codes['VALUE_TYPE']=='SERVICE_AREA_TYPE_CODE']
    for idx, row in serviceAreaType.iterrows():
        vocab = {}
        vocab['serviceAreaType'] = row['VALUE_CODE']
        iris = get_iris(vocab)
        kg2.add((iris['serviceAreaType'], RDF.type, prefixes['us_sdwis']['PWS-ServiceAreaType']))
        kg2.add((iris['serviceAreaType'], RDFS.label,  Literal(row['VALUE_DESCRIPTION'] )))

    return kg2
    

if __name__ == "__main__":
    main()
