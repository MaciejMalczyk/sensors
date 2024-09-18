import os
import pymongo
import cv2
import datetime

from . import max_cam_res
from systemd import journal
from fabric import Connection

host = "clinostate.server"

conn = Connection(
    host=host,
    user="img",
    port=8022,
    connect_kwargs={
        "key_filename": "/home/golf/.ssh/img"
    }
)

hostname = os.uname()[1]

if "static" in hostname:
    db_string = "clinostate-static"
else:
    db_string = "clinostate"


mongo_client = pymongo.MongoClient(f"mongodb://{host}:27017")
clinostate_db = mongo_client[db_string]
cameras_col = clinostate_db["images"]

def capture(dev_video):
    try:
        [cam_width, cam_height] = max_cam_res.get_max_res(f'/dev/video{dev_video}')
        img = f"{db_string}_{datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')}.jpg"
        cap = cv2.VideoCapture(dev_video)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 5)
        cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(str(img), frame)
        cap.release()
        conn.put(img, remote='/home/img/images')
        return img
    except:
        journal.send(f"CAM: Capturing img{dev_video} failed")
        print(f"CAM: Capturing img{dev_video} failed", f'{datetime.datetime.now()}')

def send():

    results = {
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    img0 = capture(0)

    if img0:
        results["img0"] = f"http://{host}:8080/{img0}"

    img2 = capture(2)

    if img2:
        results["img2"] = f"http://{host}:8080/{img2}"



    if len(results) > 1:
        try:
            journal.send("CAM: Mongodb: sending")
            print("CAM: Mongodb: sending", f'{datetime.datetime.now()}')
            cameras_col.insert_one(results)
        except:
            journal.send("CAM: No connection to mongodb")
            print("CAM: No connection to mongodb", f'{datetime.datetime.now()}')

        try:
            os.remove(img0)
        except:
            journal.send("CAM: No img0 file")
            print("CAM: No img0 file", f'{datetime.datetime.now()}')

        try:
            os.remove(img2)
        except:
            journal.send("CAM: No img2 file")
            print("CAM: No img2 file", f'{datetime.datetime.now()}')

    else:
        journal.send("CAM: No cameras avaiable!")
        print("CAM: No cameras avaiable!", f'{datetime.datetime.now()}')
        raise Exception("CAM: No cameras avaiable!")
        return


