import json
import geojson
import urllib3
import geopandas
from pathlib import Path

def dump_file(filename, geojson):
    '''Outputs the geojson to a file in data/maine_dep_esri_server directory'''
    # dump the geojson to data folder
    root_dir = Path(__file__).resolve().parent.parent.parent
    output = root_dir / "datasets" / "data" / "il-isgs" / filename
    # print(output)
    try:
        with open(output, 'w') as outfile:
            json.dump(geojson, outfile, indent=1)
    except:
        out_directory = input("Path to save the file?")
        with open(out_directory / filename, 'w') as outfile:
            json.dump(geojson, outfile, indent=1)

def get_wells():
    check= urllib3.request("GET", 'https://maps.isgs.illinois.edu/arcgis/rest/services/ILWATER/Water_and_Related_Wells2/MapServer/2/query?where=OBJECTID+%3E+-1&returnCountOnly=true&f=geojson')
    feature_count = json.loads(check.data.decode())['count']
    print(feature_count, ' Wells')
    #This server also contains aquifers
    #max record count for requests is 3000
    f=0
    layers=[]

    #get the features in batches of 3000 based on server limits
    while f < feature_count+3000:
        resp= urllib3.request("GET", f'https://maps.isgs.illinois.edu/arcgis/rest/services/ILWATER/Water_and_Related_Wells2/MapServer/2/query?where=OBJECTID+%3E+-1&outFields=*&resultOffset={f}&resultRecordCount=3000&f=geojson')
        layer_geojson = geojson.loads(resp.data)
        layers.append(layer_geojson)
        f+=3000

    #merge all the geojsons together
    layer_geojson = layers.pop(0)
    for subset in layers:
        for feature in subset['features']:
            layer_geojson['features'].append(feature)
    print(len(layer_geojson['features']))
    return (layer_geojson)


if __name__ == "__main__":

    wells = get_wells()
    dump_file('il-wells.geojson', wells)
