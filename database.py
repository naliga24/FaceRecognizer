#!/usr/bin/env python
#-*- coding: utf-8 -*-
import mysql.connector
import cv
import sys
from PIL import Image
import base64
#import cStringIO
import PIL.Image
import io

def select_subject_info():
    mydb = mysql.connector.connect(
    host="us-cdbr-iron-east-01.cleardb.net",
    user="b2742dd9273833",
    passwd="99f7887d5ff6a81",
    database="heroku_766db354cb15187",
    )
    cursor = mydb.cursor()
    sql = "SELECT * FROM subject_info"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row[0]+' '+row[1]+' '+row[2])
    mydb.close() 

def insert_class_attendace_info(studentId,subjectId):
    mydb = mysql.connector.connect(
    host="us-cdbr-iron-east-01.cleardb.net",
    user="b2742dd9273833",
    passwd="99f7887d5ff6a81",
    database="heroku_766db354cb15187",
    )
    cursor = mydb.cursor()
    #image = Image.open("frame.jpg", "rb")
    blob_value = open('frame.jpg', 'rb').read()
    encodestring = base64.b64encode(blob_value)
    sql ="SELECT COUNT(*)"
    sql += " FROM student_info"
    sql += " WHERE student_id = '"+studentId+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result[0][0])
    if result[0][0] == 1:
      sql = "INSERT INTO class_attendance_info (class_attendance_id, class_attendance_date ,class_attendance_time, subject_id, student_id, semester_id, image_info)"
      sql += " SELECT DATE_FORMAT( CURRENT_DATE , '%y%m%d' ) * 10000 +"
      sql += " (SELECT COUNT( class_attendance_date ) FROM class_attendance_info"
      sql += " WHERE class_attendance_date = CURRENT_DATE ) + 1,"
      sql += " DATE_FORMAT( CURRENT_DATE,'%Y-%m-%d' )," 
      sql += " TIME_FORMAT( CURRENT_TIME,'%h:%m:%s' ),"
      sql += " (SELECT subject_id FROM subject_info WHERE subject_name = '"+subjectId+"'),"
      sql += " '"+studentId+"',"
      sql += " (SELECT semester_id FROM semester_info ORDER BY semester_id DESC LIMIT 1),"
      sql += " '"+encodestring+"'"
      cursor.execute(sql)
      mydb.commit()
    mydb.close() 

def select_class_attendace_info():
    mydb = mysql.connector.connect(
    host="us-cdbr-iron-east-01.cleardb.net",
    user="b2742dd9273833",
    passwd="99f7887d5ff6a81",
    database="heroku_766db354cb15187",
    )
    cursor = mydb.cursor()
    sql = "SELECT a.class_attendance_id ,  DATE_FORMAT( a.class_attendance_date,'%Y-%m-%d' ) , TIME_FORMAT( a.class_attendance_time,'%h:%m:%s' ) , a.image_info , b.subject_name , c.student_id  ,c.student_first_name , c.student_last_name , d.semester_name , e.teacher_first_name , e.teacher_last_name"
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

if __name__== "__main__":
    #insert_class_attendace_info('6005004780','cos1103')
    #select_subject_info()
    select_class_attendace_info()