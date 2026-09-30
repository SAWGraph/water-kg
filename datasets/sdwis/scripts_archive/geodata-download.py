import json
import geojson
import urllib3
import re
import geopandas
from pathlib import Path

def dump_file(filename, geojson):
    '''Outputs the geojson to a file '''
    # dump the geojson to data folder
    output = root_dir / "data" / "us-sdwis" / filename
    # print(output)
    with open(output, 'w') as outfile:
        json.dump(geojson, outfile)

def get_source_layer(layer):
    """
    Request geojson from server by layer id
    Layers:

    """
    getCount = urllib3.request("GET", f'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/Water_System_Boundaries/FeatureServer/{layer}/query?where=OBJECTID+>+-1&text=&returnIdsOnly=false&returnCountOnly=true&returnDistinctValues=false&resultOffset=&f=pjson')
    #print(getCount.data)
    count = re.findall(r'\d+', str(getCount.data))
    print('record count: ', count)
    n = 0
    i = 0
    json_dump = []
    while n < int(count[0]):
        resp = urllib3.request("GET", f'https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/Water_System_Boundaries/FeatureServer/{layer}/query?where=OBJECTID+%3E+-1&outFields=*&returnGeometry=true&featureEncoding=esriDefault&resultOffset={n}&f=geojson')
        #type(resp.data)
        n += 2000 #max record count 
        print( f'get {n} dateset')
        json_dump.append(resp.data)
    while i < len(json_dump):
        layer_geojson = geojson.loads(json_dump[i])
        dump_file(f"CWS_{i}.geojson", layer_geojson)
        i += 1
    # print(json.dumps(layer_geojson[0], indent=4))
    return (json_dump)

if __name__ == "__main__":
    # set the project root for relative paths
    root_dir = Path(__file__).resolve().parent.parent.parent
    print(root_dir)

    cws_boundaries = get_source_layer(0)
    #dump file is called automatically
