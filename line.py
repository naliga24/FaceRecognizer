#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
import json
import urllib
import googlemaps
import position
LINE_API_KEY="MsrOOSUVgB38JhrKhni36IEqDftOpZbUgVYwZZmpxQT"

def line_pic(message):
        url="https://notify-api.line.me/api/notify"
        res= {"imageFile":open('frame.jpg','rb')}
        print (res)
        data = ({
        "message":message
        })
        LINE_HEADERS = {"Authorization":"Bearer "+LINE_API_KEY}
        session = requests.Session()
        b = session.post(url , headers = LINE_HEADERS , files = res , data = data)
        print(b.text) 

def line_ipstack():
        url="https://notify-api.line.me/api/notify"
        send_url = "http://api.ipstack.com/check?access_key=5ce47b09f9ee6a9e089068f0a6042b44"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        latitude = geo_json['latitude']
        longitude = geo_json['longitude']
        city = geo_json['city']
        print(geo_json)   
        msg = urllib.urlencode({"message":"https://www.google.com/maps/search/?api=1&query="+repr(latitude)+","+repr(longitude)})
        LINE_HEADERS = {"Content-Type":"application/x-www-form-urlencoded","Authorization":"Bearer "+LINE_API_KEY}
        session = requests.Session()
        a = session.post(url , headers = LINE_HEADERS , data=msg)
        print(a.text)
        
        # LINE_API_KEY = 'Bearer /mnxywYk+P8dLSFrPpEcZinPM5xmqGvzWGDLnOLhcmz3Iv4ymldO/P75wa3yPZCv2y4MNEMa/m9kHbaTHtKyxNJsoXIhWinqT8l94ePO7vflwsGHPiF0VzH8OSSL/4DRNH4zNVYWuvGDHAjyqPBuewdB04t89/1O/w1cDnyilFU='
        # LINE_API = 'https://api.line.me/v2/bot/message/push'  #reply
        # headers = {
        # 'Content-Type': 'application/json; charset=UTF-8',
        # 'Authorization': LINE_API_KEY
        # }
        # data1 ={
        # "to":""
        # "messages":[{
        # "type": "location",
        # "title": "my location",
        # "address": "ฺBangkok, Thailand",
        # "latitude": 35.65910807942215,
        # "longitude": 139.70372892916203
        # }]
        # }
        # requests.post(LINE_API, headers=headers, data=json.dumps(data1))


def line_googlemaps():
    classAttendanceLat , classAttendanceLng = position.current_position()
    url="https://notify-api.line.me/api/notify"
    # gm = googlemaps.Client(key = api_key)
    # geocode_result = gm.geocode('scranton')[0]
    # map={
    # 'position':  { 'lat': latitude, 'lng': longitude },
    # 'icon': {
    # 'url': "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
    # }
    # }
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/@"+repr(latitude)+","+repr(longitude)}) #wrong syntax(return default)
    msg = urllib.urlencode({"message":"https://www.google.com/maps/search/?api=1&query="+repr(classAttendanceLat)+","+repr(classAttendanceLng)})#3G result wrong,cable near(show red)
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/dir/?api=1&query="+repr(latitude)+","+repr(longitude)})#3G result correct,cable near
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/@?api=1&map_action=map&query="+repr(latitude)+","+repr(longitude)})#3G result correct,cable near
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/@?api=1&map_action=pano&query="+repr(latitude)+","+repr(longitude)})#3G result correct,cable near
    LINE_HEADERS = {"Content-Type":"application/x-www-form-urlencoded","Authorization":"Bearer "+LINE_API_KEY}
    session = requests.Session()
    a = session.post(url , headers = LINE_HEADERS , data=msg)
    print(a.text)
        
