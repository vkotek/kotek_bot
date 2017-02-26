#!/usr/local/bin/python3
# coding: utf-8

try:
    import json, requests, urllib
    from geopy.geocoders import Nominatim
    from geopy.distance import vincenty
except:
    print("Error importing modules, exiting.")
    exit()

api_url = "http://opendata.iprpraha.cz/CUR/FSV/FSV_VerejnaWC_b/WGS_84/FSV_VerejnaWC_b.json"


def find(address):

    # convert address to latlong
    me = locate(address+", Prague")

    if me == None:
        return None

    toilets = getToilets(api_url)

    # Get closest toilet
    wcID = getClosestID(me, toilets)
    wc = toilets[wcID-1]

    data = []
    try:
        address = wc['properties']['ADRESA']
    except:
        address = "Address not available."
    try:
        typ = wc['properties']['TYP']
    except:
        typ = ""

    r = "Closest public toilet is {} meters away.\n{}".format(getDist(me, wc), address)
    return [r , getCoords(wc)]

def getClosestID(me, toilets):

    a = {}
    for toilet in toilets:
        ID = toilet['properties']['OBJECTID']
        a[ID] = getDist(me, toilet)
    closest = min(a,key=a.get) # list offset
    print("ID {} is {} meters away.".format(closest,a[closest]))

    return closest


def getDist( coords, toilet):

    loc = toilet['geometry']['coordinates']
    loc = (loc[1],loc[0]) # Switch coords position
    dist = round(vincenty(coords, loc).meters)

    return dist

def getCoords(toilet):
    loc = toilet['geometry']['coordinates']
    return (loc[1],loc[0])


def locate(address):

    geolocator = Nominatim()
    location = geolocator.geocode(address)
    if location:
        coords = (location.latitude, location.longitude)
        return coords
    return None

def getToilets(url):
    # outputs list of dicts
    response = requests.get(url)
    content = response.content.decode('utf-8')
    js = json.loads(content)

    return js['features']

# x = find()
# print(x)
