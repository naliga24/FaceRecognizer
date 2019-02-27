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

googleCloudConfig = {
    'CLOUD_BUCKET_ATTENDANCE' : 'student_attendance',
    'PROJECT_ID' : '204186457948',
    'SERVICE_ACCOUNT_KEY' : 'my-project-1528106461323-83266a384e32.json',
    'GOOGLE_GEOLOCATION' : 'AIzaSyCSvNqw6mnNsFqGtCDX7oFDHdt_giIHPBc',
    }

lineConfig = {
    'LINE_API_KEY' : 'MsrOOSUVgB38JhrKhni36IEqDftOpZbUgVYwZZmpxQT'
    }

ipstackConfig = {
    'IPSTACK_API_KEY' : '5ce47b09f9ee6a9e089068f0a6042b44'
}
    
   
    