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
import json
import urllib
from gtts import gTTS
import classAttendance
import subject
import semester
import line
import time
import requests
import position

#api_key = os.environ['AIzaSyBu87xwiRb4bzfjLyFsGNFzGI1dLCVQhcM'] #error

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
    [images, labels, people]= get_images(path, (256, 256))
    #print([images, labels])

    labels= np.asarray(labels, dtype= np.int32)
    
    # initializing eigen_model and training
    print("Initializing eigen FaceRecognizer and training...")
    sttime= time.clock()
    eigen_model= cv2.createLBPHFaceRecognizer()
    #eigen_model= cv2.createEigenFaceRecognizer()
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

def get_student_name(str):
    id = get_student_id(str)
    name = str.replace(id,'')
    return name

def text_to_voice(text):
    tts = gTTS(text=text,lang='th')
    tts.save('student-name.mp3')
    os.system('student-name.mp3')
    #time.sleep( 6 )

def get_student_id(str):
    id = str[::-1]
    id = id[0:10]
    id = id[::-1]
    return id

def inputStudentCodeNameKey():    
    tmp = raw_input('please type 10 digits of student code name!: ')
    while(tmp.isalpha() or len(tmp) != 10):
        print('wrong format input!')
        tmp = raw_input('please type 10 digits of student code name!: ')
    return tmp

def checkResult():
    tmp = raw_input('result is: '+people[final_label]+'\n please input "x" if result is correct \n please input "y" if result is not correct\n')
    while(tmp != 'x' and tmp != 'y'):
        print('wrong format input!')
        tmp = raw_input('result: '+people[final_label]+'\n please input "x" if result is correct \n please input "y" if result is not correct\n:')
    return tmp

def current_position():
    session = requests.Session()
    a = session.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBu87xwiRb4bzfjLyFsGNFzGI1dLCVQhcM' , headers = {'Content-Type': 'application/json'})
    print(a.text)
    geo_json = json.loads(a.text)
    lat = geo_json['location']['lat']
    lng = geo_json['location']['lng']
    return [lat, lng]

if __name__== "__main__":
    if len(sys.argv)!= 4:
        print("Wrong number of arguments! See the usage.\n")
        print("Usage: face_detrec_video.py <full/path/to/root/images/folder> <subject_name> <semester_name>")
        sys.exit()

    subjectNo = subject.selectSubjectInfoSubjectNo(sys.argv[2],sys.argv[3])
    arg_three= sys.argv[3] #semester name
    if type(subjectNo) != int:  
        print("Wrong subject name with semester name!. This subject name with semester name  doesn't exists.")
        sys.exit()
    # arg_two= sys.argv[2] #subject_name
    arg_one= sys.argv[1]
    eigen_model, people= train_model(arg_one)

    #starts recording video from camera and detects & predict subjects
    cap= cv2.VideoCapture(0)

    counter= 0
    last_20= [0 for i in range(20)]
    final_5= []
    box_text= "นักศึกษา: "
    studentCodeNameKey = inputStudentCodeNameKey()
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

            [predicted_label, predicted_conf ]= eigen_model.predict(np.asarray(crop_gray_frame)) #finding result
            print(predicted_label, predicted_conf,counter,last_20)
            last_20.append(predicted_label)
            last_20= last_20[1:]
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
                    if len(final_5)== 1:
                        final_label= majority(final_5)
                        print(final_5)
                        print("Student is "+ people[final_label])
                        picture_name= "frame.jpeg"
                        cv2.imwrite(picture_name, frame)
                        line.line_pic(people[final_label])
                        line.line_googlemaps()
                        classAttendanceLat , classAttendanceLng = position.current_position()
                        resultFlag = checkResult()
                        if resultFlag == 'x':
                            classAttendance.insert_class_attendace_info(get_student_id(people[final_label]),subjectNo,studentCodeNameKey,classAttendanceLat,classAttendanceLng)
                            text_to_voice(unicode(people[final_label],"utf-8"))
                        final_5= []
                        studentCodeNameKey = inputStudentCodeNameKey()



         cv2.imshow("Video Window", frame)
         counter+= 1

         if (cv2.waitKey(5) & 0xFF== 27):
            break
    cap.release()
    cv2.destroyAllWindows()