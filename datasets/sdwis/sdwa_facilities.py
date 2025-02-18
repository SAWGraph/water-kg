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
state = "ME"

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
    df = load_data()
    kg = triplify(df)

    kg_turtle_file = f"us-sdwis-{state.strip()}-facilities.ttl".format(output_dir)
    kg.serialize(kg_turtle_file, format='turtle')
    logger = logging.getLogger('Finished triplifying SDWA Facilities.')


def load_data():
    df = pd.read_csv(data_dir / 'SDWA_FACILITIES.csv', dtype=str) # , nrows=50
    df['State']= df['PWSID'].astype(str).str[0:2]
    print(df['State'].unique())
    #filter to just one state
    df = df[df['State'] == state]

    #codes = pd.read_csv(data_dir/'SDWA_REF_CODE_VALUES.csv')

    print(df.info(verbose=True))
    logger = logging.getLogger('Data loaded to dataframe.')
    return df


def Initial_KG():
    # prefixes: Dict[str, str] = _PREFIX
    kg = Graph()
    for prefix in prefixes:
        kg.bind(prefix, prefixes[prefix])
    return kg


def get_attributes(row):

    facility = {
        'PWSID': row['PWSID'],
        'Facility_Id': row['FACILITY_ID'],
        'Facility_Name': row['FACILITY_NAME'],
        'Active': row['FACILITY_ACTIVITY_CODE'], #A/I/N/M/P
        'Type':row['FACILITY_TYPE_CODE'],
        'Availability':row['AVAILABILITY_CODE'] #P permanent, 


    }


    if pd.notnull(row.STATE_FACILITY_ID):
        facility['State_Id']= row['STATE_FACILITY_ID']
    if pd.notnull(row.FACILITY_DEACTIVATION_DATE):
        facility['Deactivation_Date'] = row['FACILITY_DEACTIVATION_DATE']
    if pd.notnull(row.SELLER_PWSID):
        facility['Seller_PWSID'] = row['SELLER_PWSID']
    if row.IS_SOURCE_IND == 'Y':
        facility['Source'] = True
    else:
        facility['Source']= False

    if pd.notnull(row['WATER_TYPE_CODE']):
        facility['SourceType'] = row['WATER_TYPE_CODE']

    return facility


def get_iris(facility):
    iris = {}
    if 'PWSID' in facility.keys():
        iris['PWS'] = prefixes['gcx']['ref/pws/'+ facility['PWSID']]
        if 'Seller_PWSID' in facility.keys():
            iris['seller_PWS'] = prefixes['gcx']['ref/pws/'+ facility['Seller_PWSID']]
        iris['facility'] = prefixes['us_sdwis_data']['d.PWS-SubFeature.'+ facility['PWSID'] +'.'+facility['Facility_Id']]
    if 'Type' in facility.keys():
        iris['type'] = prefixes['us_sdwis_data']['d.PWS-SubFeatureType.'+facility['Type']]
    if 'Active' in facility.keys():
        iris['activity'] = prefixes['us_sdwis_data']['d.PWS-SubFeatureActivity.'+ facility['Active']]

    if 'SourceType' in facility.keys():
        iris['sourceType'] = prefixes['us_sdwis_data']['d.PWS-WaterSourceType.'+facility['SourceType']]
    #print(iris)
    return iris


def triplify(df):
    kg = Initial_KG()
    for idx, row in df.iterrows():
        # get attributes
        facility = get_attributes(row)
        # get iris
        iris = get_iris(facility)
        #print(iris)
    
        #facility
        kg.add((iris['facility'], prefixes['us_sdwis']['partOf'], iris['PWS']))
        kg.add((iris['facility'], RDF.type, prefixes['us_sdwis']['PWS-SubFeature']))

        kg.add((iris['facility'], RDFS.label, Literal(facility['PWSID']+": "+facility['Facility_Id'], datatype=XSD.string)))
        kg.add((iris['facility'], prefixes['us_sdwis']['hasFacilityId'], Literal(facility['Facility_Id'], datatype=XSD.string)))
        if 'State_Id' in facility.keys():
                kg.add((iris['facility'], prefixes['us_sdwis']['hasStateFacilityId'], Literal(facility['State_Id'], datatype=XSD.string)))
        kg.add((iris['facility'], prefixes['us_sdwis']['hasType'], iris['type']))
        if 'SourceType' in facility.keys():
            kg.add((iris['facility'], prefixes['us_sdwis']['sourceType'], iris['sourceType']))

        #pws
        kg.add((iris['PWS'], RDF.type, prefixes['us_sdwis']['PublicWaterSystem'])) 
        kg.add((iris['PWS'], prefixes['us_sdwis']['hasPart'], iris['facility']))
        if 'Source' in facility.keys():
            if 'Seller_PWSID' in facility.keys():
                #if source is just a connection to another system, make the connection directly 
                kg.add((iris['PWS'], prefixes['us_sdwis']['buysFrom'], iris['seller_PWS']))
                kg.add((iris['seller_PWS'], prefixes['us_sdwis']['sellsTo'], iris['PWS']))
                kg.add((iris['facility'], prefixes['us_sdwis']['connectsTo'], iris['seller_PWS']))

            elif facility['Type'] in ['IG', 'IN', 'RC', 'RS', 'SP', 'WL']: #only count sources that are SW/GW types
                #find permanent (active) sources
                if facility['Availability']=='P': #note some of these may be inactive
                    kg.add((iris['PWS'], prefixes['us_sdwis']['hasPermanentSource'], iris['facility']))
                    kg.add((iris['facility'], prefixes['us_sdwis']['permanentSourceFor'], iris['PWS']))
                else:
                    #TODO this could be expanded to specify other types (Emergency, interim, seasonal, other, unknown)
                    kg.add((iris['PWS'], prefixes['us_sdwis']['hasSource'], iris['facility']))
                    kg.add((iris['facility'], prefixes['us_sdwis']['sourceFor'], iris['PWS']))
    


    return kg
    

if __name__ == "__main__":
    main()
