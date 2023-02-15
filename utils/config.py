from pymongo import MongoClient

irebase_creds_folder = 'firebase'

# MongoDB
DATABASE_HOST = "n1-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017,n2-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017"
DATABASE_NAME = "b94ecjrd86s6anh"
DATABASE_USERNAME = "ul2v16oblukyq47xnois"
DATABASE_PASSWORD = "KiNqFFi9gvXROPEkqp0z"

client = MongoClient("mongodb://{}:{}@{}/{}?replicaSet=rs0".format(DATABASE_USERNAME, DATABASE_PASSWORD,
                                                                  DATABASE_HOST, DATABASE_NAME))
mydb = client[DATABASE_NAME]

method = 'sha256'
