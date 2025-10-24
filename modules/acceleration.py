from .sensors import accel

import pymongo
import datetime
import os

from systemd import journal

target = "clinostate.server"
db = os.uname()[1].removesuffix("-cultivation")

mongo_client = pymongo.MongoClient(f"mongodb://{target}:27017")
clinostate_db = mongo_client[db]
cultivation_col = clinostate_db["acceleration"]


def send():
    results = {
        "g": accel.get(),
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    try:
        cultivation_col.insert_one(results)
    except Exception as err:
        journal.send(f"Acc: No connection to mongodb: {err}")
        raise Exception(f"Acc: No connection to mongodb: {err}: {datetime.datetime.now()}")
        return
