import requests
import json
import dbConfig


def current_position():
    session = requests.Session()
    a = session.post('https://www.googleapis.com/geolocation/v1/geolocate?key='+dbConfig.googleCloudConfig['GOOGLE_GEOLOCATION'] , headers = {'Content-Type': 'application/json'})
    print(a.text)
    geo_json = json.loads(a.text)
    lat = geo_json['location']['lat']
    lng = geo_json['location']['lng']
    return [lat, lng]