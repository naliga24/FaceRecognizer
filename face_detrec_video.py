#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Surya Teja Cheedella
shine123surya[at]gmail[dot]com
BITS Pilani, Hyderabad Campus
    Real-Time detection & prediction of subjects/persons in
        video recording by in-built camera.
    If there is any intruder (trained/ unknown subjects) attack, it posts on your
        facebook timeline to notify you and your friends/ neighbours.
Working:
    Takes images stored in first path and traines faceRecognizer models.
    Then starts recording video from camera and shows detected subjects.
Usage:
    face_detrec_video.py <full/path/to/root/images/folder>
Takes one argument:
    1. Input folder which contains sub-folders of subjects/ persons.
        There should be images saved in subfolders which are used to train.
'''
from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
import os
import sys, time
import requests
import request
import json
import urllib
import googlemaps
from flask import Flask, request
from gtts import gTTS
import mysql.connector
import database
import time
#api_key = os.environ['AIzaSyBu87xwiRb4bzfjLyFsGNFzGI1dLCVQhcM'] #error

LINE_ACCESS_TOKEN="MsrOOSUVgB38JhrKhni36IEqDftOpZbUgVYwZZmpxQT"
url="https://notify-api.line.me/api/notify"

def get_images(path, size):
    '''
    path: path to a folder which contains subfolders of for each subject/person
        which in turn cotains pictures of subjects/persons.
    size: a tuple to resize images.
        Ex- (256, 256)
    '''
    sub= 0
    images, labels= [], []
    people= []

    for subdir in os.listdir(path):
        for image in os.listdir(path+ "/"+ subdir):
            #print(subdir, images)
            img= cv2.imread(path+os.path.sep+subdir+os.path.sep+image, cv2.IMREAD_GRAYSCALE)
            img= cv2.resize(img, size)

            images.append(np.asarray(img, dtype= np.uint8))
            labels.append(sub)

            #cv2.imshow("win", img)
            #cv2.waitKey(10)

        people.append(subdir)
        sub+= 1

    return [images, labels, people]

def detect_faces(image):
    '''
    Takes an image as input and returns an array of bounding box(es).
    '''
    frontal_face= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #frontal_face= cv2.CascadeClassifier("haarcascade_eye.xml")
    bBoxes= frontal_face.detectMultiScale(image, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)

    return bBoxes

def train_model(path):
    '''
    Takes path to images and train a face recognition model
    Returns trained model and people
    '''
    [images, labels, people]= get_images(sys.argv[1], (256, 256))
    #print([images, labels])

    labels= np.asarray(labels, dtype= np.int32)

    # initializing eigen_model and training
    print("Initializing eigen FaceRecognizer and training...")
    sttime= time.clock()
    eigen_model= cv2.createEigenFaceRecognizer()
    eigen_model.train(images, labels)
    print("\tSuccessfully completed training in "+ str(time.clock()- sttime)+ " Secs!")

    return [eigen_model, people]

def majority(mylist):
    '''
    Takes a list and returns an element which has highest frequency in the given list.
    '''
    myset= set(mylist)
    ans= mylist[0]
    ans_f= mylist.count(ans)

    for i in myset:
        if mylist.count(i)> ans_f:
            ans= i
            ans_f= mylist.count(i)

    return ans

def line_text(message):
        msg = urllib.urlencode({"message":message})
        LINE_HEADERS = {"Content-Type":"application/x-www-form-urlencoded","Authorization":"Bearer "+LINE_ACCESS_TOKEN}
        session = requests.Session()
        a = session.post(url , headers = LINE_HEADERS , data = msg)
        print(a.text)

def line_pic(message):
        res= {"imageFile":open('frame.jpg','rb')}
        print (res)
        data = ({
        "message":message
        })
        LINE_HEADERS = {"Authorization":"Bearer "+LINE_ACCESS_TOKEN}
        session = requests.Session()
        b = session.post(url , headers = LINE_HEADERS , files = res , data = data)
        print(b.text) 
        #sys.exit()

def line_location():
        send_url = "http://api.ipstack.com/check?access_key=5ce47b09f9ee6a9e089068f0a6042b44"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        latitude = geo_json['latitude']
        longitude = geo_json['longitude']
        city = geo_json['city']
        print(geo_json)   
        msg = urllib.urlencode({"message":"https://www.google.com/maps/search/?api=1&query="+repr(latitude)+","+repr(longitude)})
        LINE_HEADERS = {"Content-Type":"application/x-www-form-urlencoded","Authorization":"Bearer "+LINE_ACCESS_TOKEN}
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
        #sys.exit()
def line_googlemaps():
    # gm = googlemaps.Client(key = api_key)
    # geocode_result = gm.geocode('scranton')[0]
    session = requests.Session()
    a = session.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBu87xwiRb4bzfjLyFsGNFzGI1dLCVQhcM' , headers = {'Content-Type': 'application/json'})
    print(a.text)
    geo_json = json.loads(a.text)
    latitude = geo_json['location']['lat']
    longitude = geo_json['location']['lng']
    # map={
    # 'position':  { 'lat': latitude, 'lng': longitude },
    # 'icon': {
    # 'url': "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
    # }
    # }
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/@"+repr(latitude)+","+repr(longitude)}) #wrong syntax(return default)
    msg = urllib.urlencode({"message":"https://www.google.com/maps/search/?api=1&query="+repr(latitude)+","+repr(longitude)})#3G result wrong,cable near(show red)
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/dir/?api=1&query="+repr(latitude)+","+repr(longitude)})#3G result correct,cable near
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/@?api=1&map_action=map&query="+repr(latitude)+","+repr(longitude)})#3G result correct,cable near
    #msg = urllib.urlencode({"message":"https://www.google.com/maps/@?api=1&map_action=pano&query="+repr(latitude)+","+repr(longitude)})#3G result correct,cable near
    LINE_HEADERS = {"Content-Type":"application/x-www-form-urlencoded","Authorization":"Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    a = session.post(url , headers = LINE_HEADERS , data=msg)
    print(a.text)
    #sys.exit()
def post_on_facebook(intruder, counter, picture_name):
    '''
    Takes name of intruder and posts on your facebok timeline.
    You need to get access_token from facebook GraphAPI and paste it below.
    '''
    # has a life time of 1 hr. So, no use even if you steal this 😜
    token= "EAAiFv4JrXxYBAHdaMwWLpJyHBPyTnVkoDkTjirypPxYgEBHwunCxyorbilnHvoj8BPcf3LoZC8yFkZBDcnaqZAByrD2cDc6KXaWts5yxLzXFCdRsRhKp1xpUqeOiA0DIkE3FqZBaa8QKgMhZB9U9HBYX31TLdCD7lXrthMRcapi0ZCvxp5YJZAVEl5dbGawXfFZBs5ThBvMJu5AFGOv1IAYH"
    url= "https://graph.facebook.com/me/feed"

    graph= facebook.GraphAPI(access_token= token)

    my_message1= "Andrew is not in his room at present and '"+ intruder+ "' entered into his room without permission."
    my_message2= "PS: This is automatically posted by 'intruder alert system' built by Andrew!\n"
    final_message= my_message1+"\n\n"+my_message2+ "\n"+ str(counter)

    #post on facebook using requests.
    # params= {"access_token": token, "message": final_message}
    # posted= requests.post(url, params)

    # if str(posted)== "<Response [200]>":
    #     print("\tSuccessfully posted on your timeline.")
    # else:
    #     print("\tPlease check your token and its permissions.")
    #     print("\tYou cannot post same message more than once in a single POST request.")

    #post on facebook using python GraphAPI
    graph.put_photo(image= open(picture_name), message= final_message)
def get_student_name(str):
    id = get_student_id(str)
    name = str.replace(id,'')
    return name
def google_tts(text):
    tts = gTTS(text=get_student_name(text),lang='th')
    tts.save('student-name.mp3')
    os.system('student-name.mp3')
    time.sleep( 3 )
    os.system('student-next.mp3')
    time.sleep( 6 )
def get_student_id(str):
    id = str[::-1]
    id = id[0:10]
    id = id[::-1]
    return id
if __name__== "__main__":
    if len(sys.argv)!= 3:
        print("Wrong number of arguments! See the usage.\n")
        print("Usage: face_detrec_video.py <full/path/to/root/images/folder> <subject_name>")
        sys.exit()
    arg_two= sys.argv[2] #subject_name
    arg_one= sys.argv[1]
    eigen_model, people= train_model(arg_one)

    #starts recording video from camera and detects & predict subjects
    cap= cv2.VideoCapture(0)

    counter= 0
    last_20= [0 for i in range(20)]
    final_5= []
    box_text= "นักศึกษา: "
    while(True):
        ret, frame= cap.read()
        if ret is True:
         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         gray_frame = cv2.equalizeHist(gray_frame)

         bBoxes= detect_faces(gray_frame)

         for bBox in bBoxes:
            (p,q,r,s)= bBox
            cv2.rectangle(frame, (p,q), (p+r,q+s), (225,0,25), 2)

            crop_gray_frame= gray_frame[q:q+s, p:p+r]
            crop_gray_frame= cv2.resize(crop_gray_frame, (256, 256))

            [predicted_label, predicted_conf]= eigen_model.predict(np.asarray(crop_gray_frame)) #finding result
            last_20.append(predicted_label)
            last_20= last_20[1:]
            print(last_20)
            print(bBoxes)
            print(bBox)
            print(counter)
            '''
            counter modulo x: changes value of final label for every x frames
            Use max_label or predicted_label as you wish to see in the output video.
                But, posting on facebook always use max_label as a parameter.
            '''
            ## Use Garuda-Bold.ttf to write thai.
            fontpath = "./Garuda-Bold.ttf" 
            font = ImageFont.truetype(fontpath, 24)
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text((0, 0),  unicode(box_text,"utf-8"), font = font, fill = (0,255,0,0))
            frame = np.array(img_pil)
            #cv2.putText(frame,  unicode(box_text,"utf-8"), (p-20, q-5), cv2.FONT_HERSHEY_PLAIN, 1.3, (25,0,225), 2)

            if counter%10== 0: #if counter%10== 0:
                max_label= majority(last_20)
                box_text= format("Subject: "+ people[max_label])
                #box_text= format("นักศึกษา: "+ people[predicted_label])

                if counter > 20:   #counter> 20
                    print("Will post on LINE notify if this counter reaches to 1: "+ str(len(final_5)+ 1))
                    final_5.append(max_label)       #it always takes max_label into consideration
                    if len(final_5)== 5:
                        final_label= majority(final_5)
                        print("Student is "+ people[final_label])
                        picture_name= "frame.jpg"
                        cv2.imwrite(picture_name, frame)
                        database.insert_class_attendace_info(get_student_id(people[final_label]),arg_two)
                        #post_on_facebook(people[final_label], counter, picture_name)
                        line_pic(people[final_label])
                        #line_location()
                        #line_googlemaps()
                        google_tts(unicode(people[final_label],"utf-8"))
                        final_5= []



         cv2.imshow("Video Window", frame)
         print(counter)
         counter+= 1

         if (cv2.waitKey(5) & 0xFF== 27):
            break
    cap.release()
    cv2.destroyAllWindows()