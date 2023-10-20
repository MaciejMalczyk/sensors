from .sensors import *

import json
import pymongo
import datetime

def send():
    results = {
            "g": accel.get(),
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }
    
    mongo_client = pymongo.MongoClient("mongodb://golfserver:27017")
    clinostate_db = mongo_client["clinostate"]
    cultivation_col = clinostate_db["acceleration"]
    cultivation_col.insert_one(results)
 
