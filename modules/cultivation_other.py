from .sensors import ambient_light, temperature, magnetometer
import config
import pymongo
import datetime
import os

from systemd import journal

target = "clinostate.server"
db = os.uname()[1].removesuffix("-cultivation")

try:
    mongo_client = pymongo.MongoClient(f"mongodb://{target}:27017")
    clinostate_db = mongo_client[db]
    cultivation_col = clinostate_db["cultivation"]

except Exception as err:
    print(f"CO: Mongodb error: {err}: {datetime.datetime.now()}")
    journal.send(f"CO: Mongodb error: {err}")


def send():
    # 23.6 comes from apds9960 documentation:
    # https://docs.broadcom.com/doc/AV02-4191EN
    # RGBC Characteristics

    try:
        l0 = ambient_light.get(config.i2c[1])
    except:
        print(f"CO: ambient_light_i2c0 failed to read: {datetime.datetime.now()}")
        journal.send("CO: ambient_light_i2c0 failed to read")
        l0 = -1

    try:
        l1 = ambient_light.get(config.i2c[0])
    except:
        print(f"CO: ambient_light_i2c1 failed to read: {datetime.datetime.now()}")
        journal.send("CO: ambient_light_i2c1 failed to read")
        l1 = -1

    try:
        t0 = temperature.get(0x19)
    except:
        print(f"CO: temperature 0x19 failed to read: {datetime.datetime.now()}")
        journal.send("CO: temperature 0x19 failed to read")
        t0 = -1

    try:
        t1 = temperature.get(0x1a)
    except:
        print(f"CO: temperature 0x1a failed to read: {datetime.datetime.now()}")
        journal.send("CO: temperature 0x1a failed to read")
        t1 = -1

    try:
        mg = magnetometer.get()
    except Exception as err:
        print(f"Magnetometer get error: {err}: {datetime.datetime.now()}")
        journal.send(f"Magnetometer get error: {err}")
        mg = [-1, -1, -1]

    results = {
        "l0": l0,
        "l1": l1,
        "l0[uW/cm^2]": l0/23.6,
        "l1[uW/cm^2]": l1/23.6,
        "t0": t0,
        "t1": t1,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
        "mg[Gauss]": mg
    }

    try:
        cultivation_col.insert_one(results)
    except Exception as err:
        journal.send(f"CO: No connection to mongodb: {err}")
        raise Exception(f"CO: No connection to mongodb: {err}: {datetime.datetime.now()}")
        return
