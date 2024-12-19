
import requests
import json
import s2sphere 

def resolvePlaceName(string, dominantType=''):
    key = 'L4Qn6dH7FvYNuLOwJBCwq8GU7jTLGZ5T0EkA5O7SdoMt6EyH'
    property = f'%3C-description{dominantType}-%3Edcid'
    res = requests.get(f"https://api.datacommons.org/v2/resolve?key={key}&nodes={string}&property={property}")
    return res

def getS2point(geom, level=13):
    p1 =s2sphere.LatLng.from_degrees(geom[0], geom[1])
    cell_ids = s2sphere.CellId.from_lat_lng(p1).parent(level).id()
    uri = f's2.level{level}.'+str(cell_ids)
    
    #cell_ids= r.get_covering(p1)
    return uri

def getS2poly(wkt, level=13):
    r = s2sphere.RegionCoverer()
    #get minimum bounding rectangle from WKT
    #get cell ids for bounding rectangle
    p1 = s2sphere.LatLng.from_degrees(33, -122)
    p2 = s2sphere.LatLng.from_degrees(33.1, -122.1)
    cell_ids = r.get_covering(s2sphere.LatLngRect.from_point_pair(p1, p2))


if __name__ == '__main__':
    #result = resolvePlaceName('POLAND town, MAINE')   #{typeOf:CensusCountyDivision}
    #print(result.text)
    #print(result.json())
    #print(result.json()['entities'][0]['resolvedIds'])

    s2 = getS2point((45, -70))
    print(s2)