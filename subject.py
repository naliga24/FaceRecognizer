#!/usr/bin/env python
#-*- coding: utf-8 -*-
import dbConfig

# def selectSubjectInfoSubjectCodeName(subjectCodeName):
#     mydb = dbConfig.config()
#     cursor = mydb.cursor()
#     sql = "SELECT COUNT(SUBJECT_CODE_NAME)"
#     sql += " FROM subject_info"
#     sql += " WHERE SUBJECT_CODE_NAME = '"+subjectCodeName+"'"
#     print(sql)
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     mydb.close() 
#     #print(result[0][0])
#     if result[0][0] == 1:
#      return True
#     else:
#      return False 

def selectSubjectInfoSubjectNo(subjectCodeName,semesterName):
    mydb = dbConfig.config()
    cursor = mydb.cursor()
    sql = "SELECT SUBJECT_NO"
    sql += " FROM subject_info"
    sql += " WHERE SUBJECT_CODE_NAME = '"+subjectCodeName+"'"
    sql += " AND SEMESTER_NO = (SELECT SEMESTER_NO FROM semester_info WHERE SEMESTER_NAME = '"+semesterName+"')"
    sql += " LIMIT 1"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    mydb.close() 
    if result:  
       return result[0][0]
if __name__== "__main__":
    selectSubjectInfoSubjectNo('cos1102','1/62')
