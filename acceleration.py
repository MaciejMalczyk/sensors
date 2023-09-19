from modules import *

import json
import pymongo
import datetime
import time

def send():
    begin = round(time.time()*1000)
    results = {
            "g": accel.get(),
            "t": time.time(),
        }
    
    mongo_client = pymongo.MongoClient("mongodb://192.168.1.102:27017")
    clinostate_db = mongo_client["clinostate"]
    cultivation_col = clinostate_db["acceleration"]
    cultivation_col.insert_one(results)
    
while True:
    send()
 
