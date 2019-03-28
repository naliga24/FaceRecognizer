#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import with_statement
from __future__ import absolute_import
from PIL import Image
import base64
#import cStringIO
import PIL.Image
import io
import requests
import os
import dbConfig
from google.cloud import storage


def get_public_url():
    return 'https://storage.cloud.google.com/'+dbConfig.googleCloudConfig['CLOUD_BUCKET_ATTENDANCE']+'/'

def insert_class_attendace_info(studentCodeName,subjectNo,classAttendanceStudentKeyCodeName,classAttendanceLat,classAttendanceLng):
    mydb = dbConfig.config()
    cursor = mydb.cursor()
    # image = Image.open("frame.jpeg", "rb") #comment
    # blob_value = open('frame.jpeg', 'rb').read() #comment
    # encodestring = base64.b64encode(blob_value)
    sql ="SELECT COUNT(STUDENT_CODE_NAME)"
    sql += " FROM student_info"
    sql += " WHERE STUDENT_CODE_NAME = '"+studentCodeName+"'"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    print('COUNT(STUDENT_CODE_NAME) = '+str(result[0][0]))
    if result[0][0] == 1:
      sql = "INSERT INTO class_attendance_info (CLASS_ATTENDANCE_CODE , CLASS_ATTENDANCE_DATE , CLASS_ATTENDANCE_TIME , SUBJECT_NO , STUDENT_NO , CLASS_ATTENDANCE_IMAGE , CLASS_ATTENDANCE_STUDENT_KEY_CODE_NAME , CLASS_ATTENDANCE_LAT , CLASS_ATTENDANCE_LNG , CONFIRM_STATUS_NO)"
      sql += " SELECT DATE_FORMAT( SUBSTRING(DATE_ADD(NOW(), INTERVAL 7 HOUR), 1,10) , '%y%m%d' ) * 10000 +"
      sql += " (SELECT COUNT( CLASS_ATTENDANCE_DATE ) FROM class_attendance_info"
      sql += " WHERE CLASS_ATTENDANCE_DATE = SUBSTRING(DATE_ADD(NOW(), INTERVAL 7 HOUR), 1,10) ) + 1,"
      sql += " SUBSTRING(DATE_ADD(NOW(), INTERVAL 7 HOUR), 1,10)," 
      sql += " ADDTIME(CURRENT_TIME(), '07:00:00'),"
      sql += " "+str(subjectNo)+","
      sql += " (SELECT STUDENT_NO FROM student_info WHERE STUDENT_CODE_NAME = '"+studentCodeName+"'),"
      sql += " CONCAT('"+str(get_public_url())+"',DATE_FORMAT( SUBSTRING(DATE_ADD(NOW(), INTERVAL 7 HOUR), 1,10) , '%y%m%d' ) * 10000 +"
      sql += " (SELECT COUNT( CLASS_ATTENDANCE_DATE ) FROM class_attendance_info"
      sql += " WHERE CLASS_ATTENDANCE_DATE = SUBSTRING(DATE_ADD(NOW(), INTERVAL 7 HOUR), 1,10) ) + 1 ,'.jpeg' ),"
      sql += " '"+classAttendanceStudentKeyCodeName+"',"
      sql += " '"+repr(classAttendanceLat)+"',"
      sql += " '"+repr(classAttendanceLng)+"',"
      sql += " '1'"
      print(sql)
      cursor.execute(sql)
      mydb.commit()
    elif result[0][0] == 0:
      print("Can't insert classAttendanceInfo, studentCodeName of '"+studentCodeName+"'"+" not found in database systems.")
    sql = "SELECT CLASS_ATTENDANCE_CODE"
    sql += " FROM class_attendance_info"
    sql += " ORDER BY CLASS_ATTENDANCE_CODE DESC LIMIT 1"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    mydb.close() 
    print(result)
    print(result[0][0]) 
    if result[0][0]:
        os.rename('frame.jpeg', result[0][0]+'.jpeg')
        # blob_value = open(result[0][0]+'.jpeg', 'rb')
        # r = requests.post('http://localhost:9000/receiveImgFromFaceRecognizer', files={'studentImage': blob_value})
        # print(r.text)
        # blob_value.close()
        # os.remove(result[0][0]+'.jpeg')

    #create bucket
 

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = dbConfig.googleCloudConfig['SERVICE_ACCOUNT_KEY']
    client = storage.Client(project=dbConfig.googleCloudConfig['PROJECT_ID'])

    # create new bucket 
    # bucket = client.bucket(dbConfig.googleCloudConfig['CLOUD_BUCKET_ATTENDANCE'])
    # bucket.location = 'us'
    # bucket.create()

    # upload image to existing bucket
    bucket = client.get_bucket(dbConfig.googleCloudConfig['CLOUD_BUCKET_ATTENDANCE'])
    blob = bucket.blob(result[0][0]+'.jpeg')
    blob.upload_from_filename( result[0][0]+'.jpeg')
    os.remove(result[0][0]+'.jpeg')


def select_class_attendace_info():
    mydb = dbConfig.config()
    cursor = mydb.cursor()
    sql = "SELECT a.class_attendance_id ,  a.class_attendance_date , a.class_attendance_time , a.CLASS_ATTENDANCE_IMAGE , b.subject_name , c.student_id  ,c.student_first_name , c.student_last_name , d.semester_name , e.teacher_first_name , e.teacher_last_name"
    sql += " FROM class_attendance_info a , subject_info b , student_info c , semester_info d , teacher_info e"
    sql += " WHERE a.subject_id = b.subject_id"
    sql += " AND a.student_id = c.student_id"
    sql += " AND a.semester_id = d.semester_id"
    sql += " AND b.teacher_id = e.teacher_id"
    sql += " ORDER BY a.class_attendance_date ASC , a.class_attendance_time ASC"

    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print('\nclass_attendance_id:'+row[0]+'\nclass_attendance_date:'+str(row[1])+'\nclass_attendance_time:'+str(row[2])+'\nsubject_name:'+row[4]+'\nstudent_id:'+row[5]+'\nstudent_first_name:'+row[6]+'\nstudent_last_name:'+row[7]+'\nsemester_name:'+row[8]+'\nteacher_first_name:'+row[9]+'\nteacher_last_name'+row[10]+'\n')
        decodestring=base64.b64decode(row[3])
        file_like=io.BytesIO(decodestring)
        #file_like=cStringIO.StringIO(result[0][6])
        img=PIL.Image.open(file_like)
        img.show()
    mydb.close() 

def test():
    print(dbConfig.googleCloudConfig['CLOUD_BUCKET_ATTENDANCE'])

if __name__== "__main__":
    #insert_class_attendace_info('6005004780','cos1103','s/74','x','x','x')
    #select_subject_info()
    #select_class_attendace_info()
    #selectSubjectInfoSubjectCodeName('cos1102')
    #print(selectSubjectInfoSubjectCodeName('cos1102'))
    test()