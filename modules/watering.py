from .sensors import *
import json
import datetime
import pymongo
from websockets.sync.client import connect
import os

hostname = os.uname()[1]

if "static" in hostname:
    ws_string = "ws://clinostate-static.local:8080"
    db_string = "clinostate-static"
else:
    ws_string = "ws://clinostate.local:8080"
    db_string = "clinostate"


mongo_client = pymongo.MongoClient("mongodb://golfserver:27017")
clinostate_db = mongo_client[db_string]
cultivation_col = clinostate_db["watering"]

def send():
    w = (moisture.get()/26928)*100
    if w < 0 :
        w = 0
    try:
        with connect(ws_string) as websocket:
            websocket.send(json.dumps({
                "action": "pump",
                "data" : {
                    "type": "cultivation",
                    "value": w,
                }
            }))
                
        results = {
            "w": w,
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }
            
        try:
            cultivation_col.insert_one(results)
        except:
            print("W: No connection to mongodb")
            
    except:
        print("No connection to clinostate backend!")
