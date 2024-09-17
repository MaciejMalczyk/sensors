from .sensors import *

import json
import pymongo
import datetime
import os

from systemd import journal

hostname = os.uname()[1]

host = "clinostate.server"

if "static" in hostname:
    db_string = "clinostate-static"
else:
    db_string = "clinostate"

mongo_client = pymongo.MongoClient(f"mongodb://{host}:27017")
clinostate_db = mongo_client[db_string]
cultivation_col = clinostate_db["acceleration"]

def send():

    results = {
            "g": accel.get(),
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }
    
    try:
        cultivation_col.insert_one(results)
    except:
        journal.send("Acc: No connection to mongodb")
        print("Acc: No connection to mongodb", f'{datetime.datetime.now()}:')
        raise Exception("Acc: No connection to mongodb")
        return
