from modules import *
import asyncio
import json
from websockets.sync.client import connect

w100 = 17300

def client():
    w = (moisture.get()/17300)*100
    print(w)
    with connect("ws://192.168.1.145:8080") as websocket:
        websocket.send(json.dumps({
            "action": "pump",
            "data" : {
                "type": "cultivation",
                "value": w,
            }
        }))
        # message = websocket.recv()
        # print(f"Received {message}")

client()
