import mysql.connector

def config():
    return mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="root",
    database="cos4105",
    )