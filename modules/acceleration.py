from .sensors import *

import json
import pymongo
import datetime

def send():
    results = {
            "g": accel.get(),
            "date": str(datetime.datetime.now()),
        }
    
    mongo_client = pymongo.MongoClient("mongodb://192.168.88.247:27017")
    clinostate_db = mongo_client["clinostate"]
    cultivation_col = clinostate_db["acceleration"]
    cultivation_col.insert_one(results)
 
