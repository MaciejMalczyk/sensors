from .sensors import ambient_light, temperature

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
    
    try:
        l0 = ambient_light.get(0)
    except:
        print("LT: ambient_light_i2c0 failed to read")
        journal.send("LT: ambient_light_i2c0 failed to read")
        l0 = -1

    try:
        l1 = ambient_light.get(1)
    except:
        print("LT: ambient_light_i2c1 failed to read")
        journal.send("LT: ambient_light_i2c1 failed to read")
        l1 = -1

    try:
        t0 = temperature.get(0x19)
    except:
        print("LT: temperature 0x19 failed to read")
        journal.send("LT: temperature 0x19 failed to read")
        t0 = -1

    try:
        t1 = temperature.get(0x1a)
    except:
        print("LT: temperature 0x1a failed to read")
        journal.send("LT: temperature 0x1a failed to read")
        t1 = -1


    results = {
            "l0": l0,
            "l1": l1,
            "l0[uW/cm^2]": l0/23.6,
            "l1[uW/cm^2]": l1/23.6,
            "t0": t0,
            "t1": t1,
            "date": datetime.datetime.now(tz=datetime.timezone.utc)
        }
    
    try:
        cultivation_col.insert_one(results)
    except:
        journal.send("LT: No connection to mongodb")
        print("LT: No connection to mongodb", f'{datetime.datetime.now()}:')
        raise Exception("LT: No connection to mongodb")
        return


