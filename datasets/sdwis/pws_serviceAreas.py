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
prefixes['qudt'] = Namespace(f'http://qudt.org/schema/qudt/')
prefixes['coso'] = Namespace(f'http://sawgraph.spatialai.org/v1/contaminoso#')
prefixes['geo'] = Namespace(f'http://www.opengis.net/ont/geosparql#')
prefixes['sosa'] = Namespace(f'http://www.w3.org/ns/sosa/')
prefixes['sf'] = Namespace("http://www.opengis.net/ont/sf#")
prefixes['gcx']= Namespace(f'http://geoconnex.us/')

## initiate log file
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running triplification for facilities")


def main():
    df, df_SA = load_data()
    kg = triplify(df, df_SA)

    kg_turtle_file = f"us-sdwis-serviceareas-{state.strip()}.ttl".format(output_dir)
    kg.serialize(kg_turtle_file, format='turtle')
    logger = logging.getLogger('Finished triplifying ghg releases.')


def load_data():
    df = gpd.read_file(data_dir / 'EPA_CWS_V1'/ 'EPA_CWS_V1.shp', dtype=str) # , nrows=50
    df_SA = pd.read_csv(data_dir / 'SDWA_SERVICE_AREAS.csv', dtype=str)
    df_SA['state'] = df_SA['PWSID'].astype(str).str[0:2] #extract state/region from pwsid
    #filter to just one state
    df = df[df['State'] == state]
    df_SA = df_SA[df_SA['state']== state]
    
    #convert to wgs84
    df = df.to_crs(crs="EPSG:4326")
    df['geometry'] = df['geometry'].make_valid()
    #convert to wkt
    df = df.to_wkt()


    print(df.info(verbose=True))
    logger = logging.getLogger('Data loaded to dataframe.')
    return df, df_SA


def Initial_KG():
    # prefixes: Dict[str, str] = _PREFIX
    kg = Graph()
    for prefix in prefixes:
        kg.bind(prefix, prefixes[prefix])
    return kg


def get_attributes(row):
    sa = {
        'PWSID': row['PWSID'],
        'state': row['State'],
        'geometry': row['geometry']

    }

    if pd.notnull(row.PWS_Name):
        sa['name'] = row['PWS_Name']
    if pd.notnull(row.Primacy_Ag):
        sa['agency'] = row['Primacy_Ag']
    if pd.notnull(row.Service_Ar):
        sa['type'] = row['Service_Ar']
    if pd.notnull(row.Method):
        sa['method'] = row['Method']


    return sa

def get_types(row):
    sa = {
        'PWSID': row['PWSID'],
        'state': row['state'],
        'type': row['SERVICE_AREA_TYPE_CODE'],
        'primary': bool(row['IS_PRIMARY_SERVICE_AREA_CODE']),
        'first': row['FIRST_REPORTED_DATE'],
        'last':row['LAST_REPORTED_DATE']
    }

    return sa

def get_iris(pws):
    iris = {}
    iris['PWS'] = prefixes['gcx']['ref/pws/'+ pws['PWSID']]
    iris['SA'] = prefixes['us_sdwis_data']['d.PWS-ServiceArea.'+ pws['PWSID']] #unsure what to use for this IRI
    iris['geom'] = prefixes['us_sdwis_data']['d.PWS-ServiceArea.geometry.'+ pws['PWSID']]
    if 'type' in pws.keys():
        iris['SAType'] = prefixes['us_sdwis_data']['d.PWS-ServiceArea-'+ pws['type']]
    #print(iris)
    return iris


def triplify(df, df_SA):
    kg = Initial_KG()
    for idx, row in df.iterrows():
        # get attributes
        sa = get_attributes(row)

        # get iris
        iris = get_iris(sa)
        #print(iris)

        #cws service areas
        kg.add((iris['PWS'], RDF.type, prefixes['us_sdwis']['PublicWaterSystem']))
        kg.add((iris['PWS'], prefixes['us_sdwis']['serviceArea'], iris['SA']))
        kg.add((iris['SA'], RDF.type, prefixes['us_sdwis']['PWS-ServiceArea']))
        kg.add((iris['SA'], prefixes['us_sdwis']['hasMethod'], Literal(sa['method'], datatype=XSD.string)))
        kg.add((iris['SA'], prefixes['geo']['hasGeometry'], iris['geom']))
        kg.add((iris['SA'], prefixes['geo']['hasDefaultGeometry'], iris['geom']))
        kg.add((iris['geom'], RDF.type, prefixes['geo']['Geometry']))
        kg.add((iris['geom'], RDF.type, prefixes['sf']['Polygon']))
        kg.add((iris['geom'], prefixes['geo']['asWKT'], Literal(sa['geometry'], datatype=prefixes["geo"]["wktLiteral"])))

    for idx, sa_row in df_SA.iterrows():
        service = get_types(sa_row)
        iris = get_iris(service)
        #all service areas with types
        kg.add((iris['PWS'], RDF.type, prefixes['us_sdwis']['PublicWaterSystem']))
        kg.add((iris['PWS'], prefixes['us_sdwis']['serviceArea'], iris['SA']))
        kg.add((iris['SA'], RDF.type, prefixes['us_sdwis']['PWS-ServiceArea']))
        kg.add((iris['SA'], prefixes['us_sdwis']['serviceAreaType'], iris['SAType'] ))


    return kg


if __name__ == "__main__":
    main()
