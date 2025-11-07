"""Create a .ttl file of state well data.

Setup instructions

Required packages:
* geopandas
* zip
* rdflib (Graph and Literal)
* rdflib.namespace (GEO, RDF, SDO, and XSD)
* pathlib (Path)
* namespaces (a local .py file with a dictionary of project namespaces)

Functions:
*
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from rdflib import Graph, Literal
from rdflib.namespace import GEO, RDF, SDO, XSD

import logging
import time
import datetime

import sys
import os

# Set working path variables and output for verification
cwd = Path(__file__).resolve().parent
ns_dir = cwd.parent.parent.parent.parent
data_dir = cwd.parent.parent / "data"
ttl_dir = cwd / "ttl_files"
log_dir = cwd / "logs"
# print(f"Current working directory:      {cwd}")
# print(f"Github repos and namespaces.py: {ns_dir}")
# print(f"Data (input) directory:         {data_dir}")
# print(f"Turtle (output) directory:      {ttl_dir}")
# print(f"Logging directory:              {log_dir}")

# Modify the system path to find namespaces.py
# sys.path.insert(1, 'G:/My Drive/Laptop/SAWGraph/Data Sources')
sys.path.insert(0, str(ns_dir))
from namespaces import _PREFIX

# Set the current directory to this file's directory
os.chdir(cwd)

### State Abbrreviation ###
state = 'me'
# Valid codes: 2-digit state abbreviations (case insensitive)

### Retrieve State Name ###
fips_dir = ns_dir / 'geospatial' / 'datasets'
fips_file = fips_dir / 'fips2county.tsv'
df_fips = pd.read_csv(fips_file, sep='\t', header='infer', dtype=str, encoding='latin-1')
state_name_df = df_fips[["StateAbbr", "StateName"]].drop_duplicates()
state_name = state_name_df.loc[state_name_df["StateAbbr"] == state.upper(), "StateName"].values[0]

### ZIP File and SHP File names ###
zip_file = data_dir / f'USGWD/USGWD_{state_name}.zip'
shape_file = f'zip://{zip_file}!USGWD_{state_name}.shp'

### OUTPUT Filename ###
main_ttl_file = ttl_dir / f'us_gwd_{state.upper()}.ttl'

logname = log_dir / f"log_US_GWD_State-2ttl.txt"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('')
logger.info('LOGGER INITIALIZED')


def load_shapefile(shp_path: str):
    try:
        gdf = gpd.read_file(shp_path)
        gdf.rename(columns={'Well ID': 'WellID',
                            'ID-State': 'IDState',
                            'Aquifer-Sp': 'AquiferSp',
                            'Aquifer-Br': 'AquiferBr',
                            'HUC12-Name': 'HUC12Name',
                            'Well Depth': 'WellDepth',
                            'Scr Depth': 'ScrDepth',
                            'Len of Scr': 'LenOfScr',
                            'Litho Data': 'LithoData',
                            'Sur Ele': 'SurEle',
                            'Yr Constr': 'YrConstr',
                            'Yr Report': 'YrReport',
                            'USGS Categ': 'USGSCateg',
                            'Irr-State': 'IrrState',
                            'Irr-USGWD': 'IrrUSGWD'}, inplace=True)
        return gdf
    except Exception as e:
        print(f'Error loading layer: {e}')


def initial_kg(_PREFIX):
    """Create an empty knowledge graph with project namespaces

    :param _PREFIX: a dictionary of project namespaces
    :return: an RDFLib graph
    """
    graph = Graph()
    for prefix in _PREFIX:
        graph.bind(prefix, _PREFIX[prefix])
    return graph


def build_iris(base, _PREFIX):
    return _PREFIX['usgwd'][base], _PREFIX['usgwd'][f'{base}.geometry']


def add_county_flag(graph, flag, welliri, _PREFIX):
    if flag == 0:
        graph.add((welliri, _PREFIX['usgwd']['flagCounty'], _PREFIX['usgwd']['FlagCounty.CompleteConsistent']))
    elif flag == 1:
        graph.add((welliri, _PREFIX['usgwd']['flagCounty'], _PREFIX['usgwd']['FlagCounty.Inconsistent']))
    elif flag == 2:
        graph.add((welliri, _PREFIX['usgwd']['flagCounty'], _PREFIX['usgwd']['FlagCounty.IncomparableMissingInfo']))
    else:
        raise ValueError('Unexpected county flag value')
    return graph


def add_state_flag(graph, flag, welliri, _PREFIX):
    if flag == 0:
        graph.add((welliri, _PREFIX['usgwd']['flagState'], _PREFIX['usgwd']['FlagState.CompleteConsistent']))
    elif flag == 1:
        graph.add((welliri, _PREFIX['usgwd']['flagState'], _PREFIX['usgwd']['FlagState.Inconsistent']))
    elif flag == 2:
        graph.add((welliri, _PREFIX['usgwd']['flagState'], _PREFIX['usgwd']['FlagState.IncomparableMissingInfo']))
    else:
        raise ValueError('Unexpected state flag value')
    return graph


def add_us_flag(graph, flag, welliri, _PREFIX):
    if flag == 0:
        graph.add((welliri, _PREFIX['usgwd']['flagUS'], _PREFIX['usgwd']['FlagUS.WithinBorder']))
    elif flag == 1:
        graph.add((welliri, _PREFIX['usgwd']['flagUS'], _PREFIX['usgwd']['FlagUS.OutsideBorder']))
    elif flag == 2:
        graph.add((welliri, _PREFIX['usgwd']['flagUS'], _PREFIX['usgwd']['FlagUS.UnknownMissingInfo']))
    else:
        raise ValueError('Unexpected US flag value')
    return graph


def add_dup_flag(graph, flag, welliri, _PREFIX):
    if flag == 0:
        graph.add((welliri, _PREFIX['usgwd']['flagDuplicate'], _PREFIX['usgwd']['FlagDuplicate.Unique']))
    elif flag == 1:
        graph.add((welliri, _PREFIX['usgwd']['flagDuplicate'], _PREFIX['usgwd']['FlagDuplicate.IncomparableMissingInfo']))
    elif flag == 2:
        graph.add((welliri, _PREFIX['usgwd']['flagDuplicate'], _PREFIX['usgwd']['FlagDuplicate.SharesIdenticalValues']))
    elif flag == 3:
        graph.add((welliri, _PREFIX['usgwd']['flagDuplicate'], _PREFIX['usgwd']['FlagDuplicate.SharesIdentifyingValues']))
    else:
        raise ValueError('Unexpected US flag value')
    return graph


def process_state(state, state_name, shp_file, graph, _PREFIX):
    logger.info(f'Load {state_name} well data from {shp_file}.')
    gdf = load_shapefile(shp_file)
    # print(gdf.columns)
    logger.info(f'Triplify {state_name} well data.')
    for row in gdf.itertuples():
        welliri_base = f'd.USGWD_Well.{str(row.WellID)}'
        welliri, geomiri = build_iris(welliri_base, _PREFIX)
        graph.add((welliri, RDF.type, _PREFIX['gwml2']['GW_Well']))
        graph.add((welliri, _PREFIX['usgwd']['hasUSGWDID'], Literal(str(row.WellID), datatype=XSD.string)))
        graph.add((welliri, _PREFIX['usgwd']['hasStateID'], Literal(str(row.IDState), datatype=XSD.string)))
        graph.add((welliri, GEO.hasGeometry, geomiri))
        graph.add((welliri, GEO.defaultGeometry, geomiri))
        graph.add((geomiri, RDF.type, GEO.Geometry))
        graph.add((geomiri, GEO.asWKT, Literal(row.geometry, datatype=GEO.wktLiteral)))
        if 'unk' not in row.AquiferSp.lower():
            graph.add((welliri, _PREFIX['gwml2']['gwWellUnit'], Literal(row.AquiferSp, datatype=XSD.string)))
        graph.add((welliri, _PREFIX['kwg-ont']['sfWithin'], _PREFIX['wbd'][f'd.HUC12.{row.HUC12}']))
        if row.xyVerified != 'Unknown':
            graph.add((welliri, _PREFIX['usgwd']['locationVerified'], Literal(row.xyVerified, datatype=XSD.string)))
        graph = add_county_flag(graph, row.F_County, welliri, _PREFIX)
        graph = add_state_flag(graph, row.F_State, welliri, _PREFIX)
        graph = add_us_flag(graph, row.F_US, welliri, _PREFIX)
        if row.WellDepth is not None and not pd.isna(row.WellDepth):
            lengthiri = f'{welliri_base}.totalLength'
            qviri = f'{lengthiri}.QV'
            graph.add((welliri, _PREFIX['gwml2']['gwWellTotalLength'], _PREFIX['usgwd'][lengthiri]))
            graph.add((_PREFIX['usgwd'][lengthiri], RDF.type, _PREFIX['usgwd']['WellDepth']))
            graph.add((_PREFIX['usgwd'][lengthiri], _PREFIX['qudt']['quantityValue'], _PREFIX['usgwd'][qviri]))
            graph.add((_PREFIX['usgwd'][qviri], RDF.type, _PREFIX['qudt']['QuantityValue']))
            graph.add((_PREFIX['usgwd'][qviri], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
            graph.add((_PREFIX['usgwd'][qviri], _PREFIX['qudt']['numericValue'], Literal(row.WellDepth, datatype=XSD.decimal)))
        if row.ScrDepth is not None and not pd.isna(row.ScrDepth):
            depthiri = f'{welliri_base}.constructedDepth'
            qviri = f'{depthiri}.QV'
            graph.add((welliri, _PREFIX['gwml2']['gwWellConstructedDepth'], _PREFIX['usgwd'][depthiri]))
            graph.add((_PREFIX['usgwd'][depthiri], RDF.type, _PREFIX['usgwd']['ScreenDepth']))
            graph.add((_PREFIX['usgwd'][depthiri], _PREFIX['qudt']['quantityValue'], _PREFIX['usgwd'][qviri]))
            graph.add((_PREFIX['usgwd'][qviri], RDF.type, _PREFIX['qudt']['qudt:QuantityValue']))
            graph.add((_PREFIX['usgwd'][qviri], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['FT']))
            graph.add((_PREFIX['usgwd'][qviri], _PREFIX['qudt']['numericValue'], Literal(row.ScrDepth, datatype=XSD.decimal)))
        if row.Capacity is not None and not pd.isna(row.Capacity):
            capiri = f'{welliri_base}.wellYield'
            qviri = f'{capiri}.QV'
            graph.add((welliri, _PREFIX['gwml2']['gwWellYield'], _PREFIX['usgwd'][capiri]))
            graph.add((_PREFIX['usgwd'][capiri], RDF.type, _PREFIX['usgwd']['Capacity']))
            graph.add((_PREFIX['usgwd'][capiri], _PREFIX['qudt']['quantityValue'], _PREFIX['usgwd'][qviri]))
            graph.add((_PREFIX['usgwd'][qviri], RDF.type, _PREFIX['qudt']['qudt:QuantityValue']))
            graph.add((_PREFIX['usgwd'][qviri], _PREFIX['qudt']['hasUnit'], _PREFIX['unit']['GAL_US-PER-MIN']))
            graph.add((_PREFIX['usgwd'][qviri], _PREFIX['qudt']['numericValue'], Literal(row.Capacity, datatype=XSD.decimal)))
        graph.add((welliri, _PREFIX['gwml2']['gwWellStatus'], Literal(row.Status, datatype=XSD.string)))
        if 'unk' not in row.YrConstr.lower():
            graph.add((welliri, _PREFIX['usgwd']['constructedDuring'], Literal(row.YrConstr, datatype=XSD.string)))
        if 'unk' not in row.YrReport.lower():
            graph.add((welliri, _PREFIX['usgwd']['reportedDuring'], Literal(row.YrReport, datatype=XSD.string)))
        graph.add((welliri, _PREFIX['usgwd']['hasUSGSWaterUse'], Literal(f'{row.USGSCateg}', datatype=XSD.string)))
        if 'irr' in row.USGSCateg.lower():
            graph.add((welliri, _PREFIX['usgwd']['hasStateIrrigSubCat'], Literal(f'{row.IrrState}', datatype=XSD.string)))
            graph.add((welliri, _PREFIX['usgwd']['hasUSGWDIrrigSubCat'], Literal(row.IrrUSGWD, datatype=XSD.string)))
        graph.add((welliri, _PREFIX['usgwd']['potable'], Literal(row.Quality.lower(), datatype=XSD.string)))
        graph = add_dup_flag(graph, row.F_Dup, welliri, _PREFIX)
    return graph


def write_graph_to_ttl(graph, outfile):
    logger.info(f'Serialize the triples to {outfile}')
    graph.serialize(outfile, format='ttl')


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f'Launching script: USGWD for {state_name}')
    kg = initial_kg(_PREFIX)
    kg = process_state(state.upper(), state_name, shape_file, kg, _PREFIX)
    write_graph_to_ttl(kg, main_ttl_file)
    logger.info(f'Runtime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
    # print(f'\nRuntime: {str(datetime.timedelta(seconds=time.time() - start_time))} HMS')
