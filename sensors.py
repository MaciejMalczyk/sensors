from modules import *
from websockets.sync.client import connect

import asyncio
import json

def send():
    results = {
            "l0": ambient_light_i2c0.get(),
            "l1": ambient_light_i2c1.get(),
            "t0": temperature_0.get(),
            "t1": temperature_1.get(),
            "g": accel.get(),
            "W": moisture.get()
        }

    with connect("ws://clinostate.local:8080") as websocket:
        data = {
            "action": "sensors",
            "data": results
        }
        websocket.send(json.dumps(data))


    print(results)

send()
