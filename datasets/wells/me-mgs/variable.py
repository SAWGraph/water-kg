import geopandas as gdp
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
from rdflib import Namespace
from rdflib import Graph
from rdflib import URIRef, BNode, Literal

import math
import os
import json
import pickle
import numpy as np
from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
import random
import re
import requests
from re import sub
import shapely

from datetime import datetime



# NAME_SPACE = "http://stko-roy.geog.ucsb.edu/"
NAME_SPACE = "http://aiknowspfas.skai.maine.edu/"

_PREFIX = {
    "aik-pfas": Namespace(f"{NAME_SPACE}lod/resource/"),
    "aik-pfas-ont": Namespace(f"{NAME_SPACE}lod/ontology/"),
    "kwg-ont": Namespace(f'http://stko-kwg.geog.ucsb.edu/lod/ontology/'),
    "dc": Namespace('https://datacommons.org/browser/'),
    "geo": Namespace("http://www.opengis.net/ont/geosparql#"),
    "sf": Namespace("http://www.opengis.net/ont/sf#"),
    "rdf": RDF,
    "rdfs": RDFS,
    "xsd": XSD,
    "owl": OWL,
    "time": TIME,
    "time": Namespace("http://www.w3.org/2006/time#"),
    "ssn": Namespace("http://www.w3.org/ns/ssn/"),
    "sosa": Namespace("http://www.w3.org/ns/sosa/"),
    "qudt": Namespace("https://qudt.org/schema/qudt/"),
    "prov": Namespace("http://www.w3.org/ns/prov#")
}

def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])

