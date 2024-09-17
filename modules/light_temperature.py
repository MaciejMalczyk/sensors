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
cultivation_col = clinostate_db["cultivation"]

def send():
    # 23.6 comes from apds9960 documentation: 
    # https://docs.broadcom.com/doc/AV02-4191EN
    # RGBC Characteristics
    
    l0 = ambient_light_i2c0.get()
    l1 = ambient_light_i2c1.get()
    results = {
            "l0": l0,
            "l1": l1,
            "l0[uW/cm^2]": l0/23.6,
            "l1[uW/cm^2]": l1/23.6,
            "t0": temperature_0.get(),
            "t1": temperature_1.get(),
            "date": datetime.datetime.now(tz=datetime.timezone.utc)
        }
    
    try:
        cultivation_col.insert_one(results)
    except:
        journal.send("LT: No connection to mongodb")
        print("LT: No connection to mongodb", f'{datetime.datetime.now()}:')
        raise Exception("LT: No connection to mongodb")
        return


