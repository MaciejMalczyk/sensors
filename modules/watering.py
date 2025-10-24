from .sensors import moisture
import json
import datetime
import pymongo
from websockets.sync.client import connect
import os

from systemd import journal

target = "clinostate.server"
db = os.uname()[1].removesuffix("-cultivation")
ws_string = f"ws://{db}.local:8080"


mongo_client = pymongo.MongoClient(f"mongodb://{target}:27017")
clinostate_db = mongo_client[db]
cultivation_col = clinostate_db["watering"]


def send():
    w = (moisture.get()/26928)*100
    if w < 0:
        w = 0
    try:
        with connect(ws_string) as websocket:
            websocket.send(json.dumps({
                "action": "pump",
                "data": {
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
        except Exception as err:
            journal.send("W: No connection to mongodb")
            raise Exception(f"W: No connection to mongodb: {err}: {datetime.datetime.now()}")
            return
    except Exception as err:
        journal.send("W: No connection to clinostate backend!")
        print(f"W: No connection to clinostate backend!: {err}: {datetime.datetime.now()}")
