from .sensors import *

import json
import pymongo
import datetime
import os

hostname = os.uname()[1]

if "static" in hostname:
    db_string = "clinostate-static"
else:
    db_string = "clinostate"

mongo_client = pymongo.MongoClient("mongodb://golfserver:27017")
clinostate_db = mongo_client[db_string]
cultivation_col = clinostate_db["cultivation"]

def send():
    
    results = {
            "l0": ambient_light_i2c0.get(),
            "l1": ambient_light_i2c1.get(),
            "t0": temperature_0.get(),
            "t1": temperature_1.get(),
            "date": datetime.datetime.now(tz=datetime.timezone.utc)
        }
    
    try:
        cultivation_col.insert_one(results)
    except:
        print("LT: No connection to mongodb")


