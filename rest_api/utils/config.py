from pymongo import MongoClient
from googleapiclient.discovery import build
from google.oauth2 import service_account
# MongoDB
DATABASE_HOST = "n1-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017,n2-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017"
DATABASE_NAME = "b94ecjrd86s6anh"
DATABASE_USERNAME = "ul2v16oblukyq47xnois"
DATABASE_PASSWORD = "KiNqFFi9gvXROPEkqp0z"

client = MongoClient("mongodb://{}:{}@{}/{}?replicaSet=rs0".format(DATABASE_USERNAME, DATABASE_PASSWORD,
                                                                  DATABASE_HOST, DATABASE_NAME))
mydb = client[DATABASE_NAME]

#google drive
scope = ['https://www.googleapis.com/auth/drive']
key_file_location = '/Users/jokkojja/Desktop/diplom/diplom/google_drive/hopeful-sound-387705-801fd71458ae.json'
credentials = service_account.Credentials.from_service_account_file(
key_file_location)

scoped_credentials = credentials.with_scopes(scope)
service = build('drive', 'v3', credentials=scoped_credentials)


method = 'sha256'

