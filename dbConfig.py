import mysql.connector

# def config():
#     return mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     passwd="root",
#     database="cos4105",
#     )

def config():
    return mysql.connector.connect(
    host="us-cdbr-iron-east-01.cleardb.net",
    user="b2742dd9273833",
    passwd="99f7887d5ff6a81",
    database="heroku_766db354cb15187",
    )