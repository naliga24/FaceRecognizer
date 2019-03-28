#!/usr/bin/env python
#-*- coding: utf-8 -*-
import dbConfig

# def selectSemesterInfoSemesterName(semesterName):
#     mydb = dbConfig.config()
#     cursor = mydb.cursor()
#     sql = "SELECT COUNT(SEMESTER_NAME)"
#     sql += " FROM semester_info"
#     sql += " WHERE SEMESTER_NAME = '"+semesterName+"'"
#     print(sql)
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     mydb.close()  
#     #print(result[0][0])
#     if result[0][0] == 1:
#      return True
#     else:
#      return False 

if __name__== "__main__":
    selectSemesterInfoSemesterName('s/74')
