from rdflib.namespace import OWL, XMLNS, XSD, RDF, RDFS
from rdflib import Namespace
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
import pandas as pd
import logging
import sys
from pathlib import Path

## declare variables
state = "IL"
controlledVocab = True

## data paths
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent
data_dir = cwd.parent / "data"
ttl_dir = cwd / "ttl_files"
log_dir = cwd / "logs"
# print(f"Current working directory:      {cwd}")
# print(f"Github repos and namespaces.py: {ns_dir}")
# print(f"Data (input) directory:         {data_dir}")
# print(f"Turtle (output) directory:      {ttl_dir}")
# print(f"Logging directory:              {log_dir}")

## namespaces

prefixes = {}
prefixes['us_sdwis'] = Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis#')
prefixes['us_sdwis_data'] = Namespace(f'http://sawgraph.spatialai.org/v1/us-sdwis-data#')
prefixes['qudt'] = Namespace(f'http://qudt.org/schema/qudt/')
prefixes['coso'] = Namespace(f'http://w3id.org/coso/v1/contaminoso#')
prefixes['geo'] = Namespace(f'http://www.opengis.net/ont/geosparql#')
prefixes['sosa'] = Namespace(f'http://www.w3.org/ns/sosa/')
prefixes['gcx'] = Namespace(f'http://geoconnex.us/')
# prefixes['us_frs'] = Namespace(f"http://sawgraph.spatialai.org/v1/us-frs#")
# prefixes['us_frs_data'] = Namespace(f"http://sawgraph.spatialai.org/v1/us-frs-data#")

## initiate log file
logname = log_dir / "log_sdwa_controlledVocab.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info("Running triplification for facilities")


def main():
    codes = load_data()
    kg2 = triplify(codes)
    kg2_turtle_file = ttl_dir / f'us-sdwis-controlledVocab.ttl'
    kg2.serialize(kg2_turtle_file, format='turtle')
    logger.info('Finished triplifying SDWIS controlled vocabularies.')


def load_data():
    codes = pd.read_csv(data_dir / 'SDWIS/SDWA_REF_CODE_VALUES.csv')
    print(codes.info(verbose=True))
    logger.info('Data loaded to dataframe.')
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
        iris['type'] = prefixes['us_sdwis']['PWS-SubFeatureType.' + facility['Type']]
    if 'Active' in facility.keys():
        iris['activity'] = prefixes['us_sdwis']['PWS-SubFeatureActivity.' + facility['Active']]
    if 'SourceType' in facility.keys():
        iris['sourceType'] = prefixes['us_sdwis']['PWS-WaterSourceType.' + facility['SourceType']]
    if 'serviceAreaType' in facility.keys():
        iris['serviceAreaType'] = prefixes['us_sdwis']['PWS-ServiceArea-' + facility['serviceAreaType']]
    # print(iris)
    return iris


def triplify(codes):
    # Controlled Vocabularies
    kg2 = Initial_KG()
    # SubFeature Type controlled vocabulary
    facility_type = codes[codes['VALUE_TYPE'] == 'FACILITY_TYPE_CODE']
    for idx, row in facility_type.iterrows():
        facility = {}
        facility['Type'] = row['VALUE_CODE']
        iris = get_iris(facility)
        kg2.add((iris['type'], RDF.type, prefixes['us_sdwis']['PWS-SubFeatureType']))
        kg2.add((iris['type'], RDF.type, OWL.NamedIndividual))
        kg2.add((iris['type'], RDFS.label, Literal(row['VALUE_DESCRIPTION'])))
    # SubFeature Activity controlled vocabulary
    activity_type = codes[codes['VALUE_TYPE'] == 'ACTIVITY_CODE']
    for idx, row in activity_type.iterrows():
        facility = {}
        facility['Active'] = row['VALUE_CODE']
        iris = get_iris(facility)
        kg2.add((iris['activity'], RDF.type, prefixes['us_sdwis']['PWS-SubFeatureActivity']))
        kg2.add((iris['activity'], RDF.type, OWL.NamedIndividual))
        kg2.add((iris['activity'], RDFS.label, Literal(row['VALUE_DESCRIPTION'])))
    # Service Area Type controlled vocabulary
    serviceAreaType = codes[codes['VALUE_TYPE'] == 'SERVICE_AREA_TYPE_CODE']
    for idx, row in serviceAreaType.iterrows():
        vocab = {}
        vocab['serviceAreaType'] = row['VALUE_CODE']
        iris = get_iris(vocab)
        kg2.add((iris['serviceAreaType'], RDF.type, prefixes['us_sdwis']['PWS-ServiceAreaType']))
        kg2.add((iris['serviceAreaType'], RDF.type, OWL.NamedIndividual))
        kg2.add((iris['serviceAreaType'], RDFS.label, Literal(row['VALUE_DESCRIPTION'])))
    return kg2


if __name__ == "__main__":
    main()
