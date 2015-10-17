from os import environ
from requests import get
from sys import exit


def get_travel_time(orig_coord, dest_coord, travel_type):
    
    try: 
        maps_api_key = environ['GM_APIKEY']
    except KeyError:
        print "ERROR: set $GM_APIKEY to your google maps api key"
        exit()
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode={2}&language=en-EN&key={3}".format(
        str(orig_coord), travel_type, str(dest_coord), maps_api_key)
    result = get(url, timeout=30).json()
    transit_time = result['rows'][0]['elements'][0]['duration']['value']
    return transit_time  # in seconds
