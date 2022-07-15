from pymongo import MongoClient
import os

"""mongo db setup"""
try:
    db_client = MongoClient(host=os.environ['MONGODB_HOSTNAME'],
                            port=int(os.environ['MONGO_PORT']),
                            username=os.environ['MONGO_INITDB_ROOT_USERNAME'],
                            password=os.environ['MONGO_INITDB_ROOT_PASSWORD'],
                            authSource=os.environ['MONGO_AUTH_SOURCE'])
    db = db_client['test-db']
except Exception as err:
    print("Could not connect to MongoDB: ", err)