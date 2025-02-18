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
state = False
#state = "IL"
#fips codes from https://www2.census.gov/geo/docs/reference/codes2020/national_state2020.txt
state_fips = {'AL':'01',
              'AK':'02',
              'AZ':'04',
              'AR':'05',
              'CA':'06',
              'CO':'08',
              'CT':'09',
              'DE':'10',
              'DC':'11',
              'FL':'12',
              'GA':'13',
              'HI':'15',
              'ID':'16',
              'IL':'17',
              'IN':'18',
              'IA':'19',
              'KS':'20',
              'KY':'21',
              'LA':'22',
              'ME':'23',
              'MD':'24',
              'MA':'25',
              'MI':'26',
              'MN':'27',
              'MS':'28',
              'MO':'29',
              'MT':'30',
              'NE':'31',
              'NV':'32',
              'NH':'33',
              'NJ':'34',
              'NM':'35',
              'NY':'36',
              'NC':'37',
              'ND':'38',
              'OH':'39',
              'OK':'40',
              'OR':'41',
              'PA':'42',
              'RI':'44',
              'SC':'45',
              'SD':'46',
              'TN':'47',
              'TX':'48',
              'UT':'49',
              'VT':'50',
              'VA':'51',
              'WA':'53',
              'WV':'54',
              'WI':'55',
              'WY':'56',
              'AS':'60',
              'GU':'66',
              'MP':'69',
              'PR':'72',
              'UM':'74',
              'VI':'78'
              }

## data path
root_folder = Path(__file__).resolve().parent.parent.parent
data_dir = root_folder / "data/us-sdwis/"
metadata_dir = None
output_dir = root_folder / "federal/us-sdwis/"

##namespaces

prefixes = {}
prefixes['us_sdwis'] = Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis#')
prefixes['us_sdwis_data'] = Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis#')
prefixes['kwg-ont']= Namespace(f'http://stko-kwg.geog.ucsb.edu/lod/ontology/')
prefixes['qudt'] = Namespace(f'https://qudt.org/schema/qudt/')
prefixes['coso'] = Namespace(f'http://sawgraph.spatialai.org/v1/contaminoso#')
prefixes['geo'] = Namespace(f'http://www.opengis.net/ont/geosparql#')
prefixes['sosa'] = Namespace(f'http://www.w3.org/ns/sosa/')
prefixes['gcx']= Namespace(f'http://geoconnex.us/')
prefixes['kwg-ont']= Namespace(f'http://stko-kwg.geog.ucsb.edu/lod/ontology/')
prefixes['kwgr']= Namespace(f'http://stko-kwg.geog.ucsb.edu/lod/resource/')

## initiate log file
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running triplification for facilities")


def main():
    df = load_data()
    global state
    if state:
        #filter
        df = df[df['state'] == state]
        print(df.info(verbose=True))
        kg = triplify(df)
        kg_turtle_file = f"us-sdwis-geographicarea-{state.strip()}.ttl".format(output_dir)
        kg.serialize(kg_turtle_file, format='turtle')
        logger = logging.getLogger(f'Finished triplifying sdwis geographic areas {state}.')
    else:
        for state in df['state'].unique():
            df_state = df[df['state'] == state]
            print(df_state.info(verbose=True))
            kg = triplify(df_state)
            kg_turtle_file = f"us-sdwis-geographicarea-{state.strip()}.ttl".format(output_dir)
            kg.serialize(kg_turtle_file, format='turtle')
            logger = logging.getLogger(f'Finished triplifying sdwis geographic areas {state}.')


def load_data():
    df = pd.read_csv(data_dir / 'SDWA_GEOGRAPHIC_AREAS.csv', dtype=str) # , nrows=50
    #filter to just one state
    #get the state from first two characters of pwsid
    df['state'] = df['PWSID'].str[:2]
    logger = logging.getLogger('Data loaded to dataframe.')
    return df


def Initial_KG():
    # prefixes: Dict[str, str] = _PREFIX
    kg = Graph()
    for prefix in prefixes:
        kg.bind(prefix, prefixes[prefix])
    return kg


def get_attributes(row):
    global state
    pws = {
        'PWSID': row['PWSID'],
        'TYPE': row['AREA_TYPE_CODE']
        

    }
    #county service
    if row.AREA_TYPE_CODE == 'CN':
        try:
            int(state) #these are EPA regions not states (for tribal areas)
            print(state, row.ANSI_ENTITY_CODE)

        except:
            pws['county_fips'] = str(state_fips[state]) + row['ANSI_ENTITY_CODE']

    #if pd.notnull(row.PWS_NAME):
    #    pws['Name'] = row['PWS_NAME']
    

    return pws


def get_iris(pws):
    iris = {}
    iris['PWS'] = prefixes['gcx']['ref/pws/'+ pws['PWSID']]
    #county iri
    if pws['TYPE'] == 'CN':
        if 'county_fips' in pws.keys():
            iris['admin2'] = prefixes['kwgr']['administrativeRegion.USA.'+str(pws['county_fips'])]
        else:
            print('unknown state')
    #zip
    #tribal
    #city

    #print(iris)
    return iris


def triplify(df):
    kg = Initial_KG()
    for idx, row in df.iterrows():
        # get attributes
        pws = get_attributes(row)
        # get iris
        iris = get_iris(pws)
        #print(iris)

        #pws
        kg.add((iris['PWS'], RDF.type, prefixes['us_sdwis']['PublicWaterSystem']))
        if 'admin2' in iris.keys():
            kg.add((iris['PWS'], prefixes['kwg-ont']['sfOverlaps'], iris['admin2']))
    return kg


if __name__ == "__main__":
    main()
