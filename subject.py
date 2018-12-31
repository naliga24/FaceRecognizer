#!/usr/bin/env python
#-*- coding: utf-8 -*-
import dbConfig

def selectSubjectInfoSubjectCodeName(subjectCodeName):
    mydb = dbConfig.config()
    cursor = mydb.cursor()
    sql = "SELECT COUNT(SUBJECT_CODE_NAME)"
    sql += " FROM subject_info"
    sql += " WHERE SUBJECT_CODE_NAME = '"+subjectCodeName+"'"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    mydb.close() 
    #print(result[0][0])
    if result[0][0] == 1:
     return True
    else:
     return False 

if __name__== "__main__":
    selectSubjectInfoSubjectCodeName('cos1101')
