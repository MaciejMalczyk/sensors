from .sensors import *

import json
import pymongo
import datetime

mongo_client = pymongo.MongoClient("mongodb://golfserver:27017")
clinostate_db = mongo_client["clinostate"]
cultivation_col = clinostate_db["acceleration"]

def send():
    results = {
            "g": accel.get(),
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }
    
    try:
        cultivation_col.insert_one(results)
    except:
        print("No connection to mongodb")
 
