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
import urllib3

code_dir = Path(__file__).resolve().parent.parent
#print(code_dir)
#sys.path.insert(0, str(code_dir))
#from variable import NAME_SPACE, _PREFIX

## declare variables
logname = "log"
state = None
#state = "ME"

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
prefixes['qudt'] = Namespace(f'http://qudt.org/schema/qudt/')
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

logging.info("Running triplification for Public Water Systems")


def main():
    df = load_data()
    global state
    if state:
        #filter to just one state
        df = df[df['PRIMACY_AGENCY_CODE'] == state]
        print(df.info(verbose=True))
        kg = triplify(df)
        kg_turtle_file = f"us-sdwis-{state.strip()}.ttl".format(output_dir)
        kg.serialize(kg_turtle_file, format='turtle')
        logger = logging.getLogger('Finished triplifying sdwis.')
    else:
        #otherwise run all states
        for state in df['PRIMACY_AGENCY_CODE'].unique():
            #filter to just one state
            state_df= df[df['PRIMACY_AGENCY_CODE'] == state]
            print(state, len(state_df))
            kg = triplify(state_df)

            kg_turtle_file = f"us-sdwis-{state.strip()}.ttl".format(output_dir)
            kg.serialize(kg_turtle_file, format='turtle')
            logger = logging.getLogger(f'Finished triplifying sdwis for {state} .')


def load_data():
    df = pd.read_csv(data_dir / 'SDWA_PUB_WATER_SYSTEMS.csv', dtype=str) # , nrows=50

   
    logger = logging.getLogger('Data loaded to dataframe.')
    return df


def Initial_KG():
    # prefixes: Dict[str, str] = _PREFIX
    kg = Graph()
    for prefix in prefixes:
        kg.bind(prefix, prefixes[prefix])
    return kg


def get_attributes(row):
    pws = {
        'PWSID': row['PWSID'],
        'ActivityCode': row['PWS_ACTIVITY_CODE'], # A - Active, I- inactive, N- changed from public to non-public, M - merged with another system, P- potential future system to be regulated
        #TODO should this be a controlled vocab? and how is that implemented?
        'PopulationServed': row['POPULATION_SERVED_COUNT'],
        'Connections': row['SERVICE_CONNECTIONS_COUNT'],
        # TODO IS_WHOLESALER_IND, IS_SCHOOL_OR_DAYCARE_IND
        'FirstReport': datetime.strptime(row['FIRST_REPORTED_DATE'], '%m/%d/%Y')

    }

    if pd.notnull(row.PWS_NAME):
        pws['Name'] = row['PWS_NAME']
    if pd.notnull(row.SEASON_BEGIN_DATE):
        pws['SeasonBegin'] = row['SEASON_BEGIN_DATE']
        pws['SeasonEnd'] = row['SEASON_END_DATE']
    if pd.notnull(row.PWS_DEACTIVATION_DATE): #only inactive pws have deactivation date?
        pws['Deactivation'] = datetime.strptime(row['PWS_DEACTIVATION_DATE'], '%m/%d/%Y')
        #print(pws['Deactivation'])
    if pd.notnull(row.LAST_REPORTED_DATE):
        pws['LastReport'] = datetime.strptime(row['LAST_REPORTED_DATE'], '%m/%d/%Y')

    # controlled vocabularies  TODO fix to controlled vocabulary
    pwsPrimarySourceLookup={
        'GW': 'Ground water',
        'GWP': 'Ground water Purchased',
        'SW': 'Surface water',
        'SWP': 'Surface water Purchased',
        'GU': 'Ground water under influence of surface water',
        'GUP': 'Purchased ground water under influence of surface water source'
    }
    if pd.notnull(row.PRIMARY_SOURCE_CODE):
        pws['Source'] = pwsPrimarySourceLookup[row['PRIMARY_SOURCE_CODE']]
        pws['SourceType'] = row.PRIMARY_SOURCE_CODE

    pwsTypeLookup = {
        'CWS':'Community Water System',
        'TNCWS': 'Transient Community Water System',
        'NTNCWS': 'Nontransient Non-Community Water System',
        'NP': ''
    }
    if row['PWS_TYPE_CODE'] in ['TNCWS', 'NTNCWS']:
        pws['Type'] = 'NCWS'
        pws['Transient'] = row['PWS_TYPE_CODE']
    else:
        pws['Type'] = row['PWS_TYPE_CODE']
    pws['PWSTypeName'] = pwsTypeLookup[row['PWS_TYPE_CODE']]

    if pd.notnull(row.GW_SW_CODE):
        pws['GWSW'] = row['GW_SW_CODE']
    if pd.notnull(row.CDS_ID):
        pws['CDSID'] = str(row['CDS_ID']).replace(" ","")

    pwsActivityCodeLookup={   # A - Active, I- inactive, N- changed from public to non-public, M - merged with another system, P- potential future system to be regulated
        'A': 'Active',
        'I': 'Inactive',
        'N': 'Non-Public',
        'M': 'Merged',
        'P': 'Potential Future System'

    }
    pws['ActivityCodeLong'] = pwsActivityCodeLookup[pws['ActivityCode']]

    pwsOwnerTypeLookup={
        'F': 'Federal Government',
        'L': 'Local Government',
        'M': 'Public / Private',
        'N': 'Native American',
        'P': 'Private',
        'S': 'State Government'
    }
    if pd.notnull(row.OWNER_TYPE_CODE):
        pws['Owner'] = pwsOwnerTypeLookup[row['OWNER_TYPE_CODE']]
    

    return pws


def get_iris(pws):
    iris = {}
    iris['PWS'] = prefixes['gcx']['ref/pws/'+ pws['PWSID']]
    if 'CDSID' in pws.keys():
        iris['CDS'] = prefixes['us_sdwis_data']['d.CombinedDistributionSystem.'+ pws['CDSID']]
    if 'SourceType' in pws.keys():
        iris['SourceType'] = prefixes['us_sdwis_data']['d.PWS-WaterSourceType.'+ pws['SourceType']]
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
        if pws['Type'] != "NP":
            kg.add((iris['PWS'], RDF.type, prefixes['us_sdwis'][str('PublicWaterSystem' + '-' + pws['Type'])])) 
        if 'Transient' in pws.keys():
            kg.add((iris['PWS'], RDF.type, prefixes['us_sdwis'][str('PublicWaterSystem' + '-' + pws['Transient'])]))
        if 'GWSW' in pws.keys():
            kg.add((iris['PWS'], RDF.type, prefixes['us_sdwis'][str('PublicWaterSystem' + '-' + pws['GWSW'])])) #See also primarySourceType
        if 'Name' in pws.keys():
            kg.add((iris['PWS'], prefixes['us_sdwis']['pwsName'], Literal(pws['Name'], datatype=XSD.string)))
            kg.add((iris['PWS'], RDFS.label, Literal(pws['Name'], datatype=XSD.string)))

        #key data properties
        kg.add((iris['PWS'], prefixes['us_sdwis']['populationServed'], Literal(pws['PopulationServed'], datatype=XSD.int)))
        kg.add((iris['PWS'], prefixes['us_sdwis']['serviceConnections'], Literal(pws['Connections'], datatype=XSD.int)))
        # TODO Activity code - class?
        kg.add((iris['PWS'], prefixes['us_sdwis']['hasActivity'], Literal(pws['ActivityCodeLong'], datatype=XSD.string)))
        #TODO season begin/end What datatype for recurring day-month date?

        #extra properties
        if 'Deactivation' in pws.keys():
            kg.add((iris['PWS'], prefixes['us_sdwis']['deactivationDate'], Literal(pws['Deactivation'], datatype=XSD.date)))
        if 'Owner' in pws.keys():
            kg.add((iris['PWS'],prefixes['us_sdwis']['hasOwnership'], Literal(pws['Owner'], datatype=XSD.string)))
        if 'SourceType' in pws.keys():
            #kg.add((iris['PWS'], prefixes['us_sdwis']['primarySource'], Literal(pws['Source'], datatype=XSD.string))) #old literal version
            kg.add((iris['PWS'], prefixes['us_sdwis']['primarySourceType'], iris['SourceType'])) #controlled vocab
        kg.add((iris['PWS'], prefixes['us_sdwis']['firstReport'], Literal(pws['FirstReport'], datatype=XSD.date )))
        if 'LastReport' in pws.keys():
            kg.add((iris['PWS'], prefixes['us_sdwis']['lastReport'], Literal(pws['LastReport'], datatype=XSD.date)))


        #object properties
        ##combined distribution system
        if 'CDSID' in pws.keys():
            kg.add((iris['CDS'], RDF.type, prefixes['us_sdwis']['CombinedDistributionSystem']))
            kg.add((iris['PWS'], prefixes['us_sdwis']['inCombinedSystem'], iris['CDS']))

    return kg


if __name__ == "__main__":
    main()
