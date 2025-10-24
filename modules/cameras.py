import os
import pymongo
import cv2
import datetime

from . import camera_scripts
from systemd import journal
from fabric import Connection

target = "clinostate.server"
db = os.uname()[1].removesuffix("-cultivation")

conn = Connection(
    host=target,
    user="img",
    port=8022,
    connect_kwargs={
        "key_filename": "/home/golf/.ssh/img"
    }
)


mongo_client = pymongo.MongoClient(f"mongodb://{target}:27017")
clinostate_db = mongo_client[db]
cameras_col = clinostate_db["images"]


def capture(dev_video):
    try:
        [cam_width, cam_height] = camera_scripts.get_max_res(f'/dev/video{dev_video}')
        img = f"{hostname}_{datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')}.jpg"
        cap = cv2.VideoCapture(dev_video)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 5)
        cap.set(cv2.CAP_PROP_AUTO_WB, 0)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        ret, frame = cap.read()
        cv2.imwrite(str(img), frame)
        cap.release()
        conn.put(img, remote='/home/img/images')
        return img
    except Exception as err:
        journal.send(f"CAM: Capturing img{dev_video} failed: {err}")
        print(f"CAM: Capturing img{dev_video} failed: {err}: {datetime.datetime.now()}")


def send():

    results = {
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    cameras = camera_scripts.get_camera_devices()

    for c in cameras:
        c_img = capture(int(c[10:]))
        if c_img:
            results[f"img{int(c[10:])}"] = f"http://{target}:8080/{c_img}"

        try:
            os.remove(c_img)
        except Exception as err:
            journal.send(f"CAM: No img{c_img} file: {err}")
            print(f"CAM: No img{c_img} file: {err}: {datetime.datetime.now()}")

    if len(results) > 1:
        try:
            journal.send("CAM: Mongodb: sending")
            print("CAM: Mongodb: sending", f'{datetime.datetime.now()}')
            cameras_col.insert_one(results)
        except Exception as err:
            journal.send(f"CAM: No connection to mongodb: {err}")
            print(f"CAM: No connection to mongodb: {err}: {datetime.datetime.now()}")

    else:
        journal.send("CAM: No cameras avaiable!")
        raise Exception(f"CAM: No cameras avaiable!: {datetime.datetime.now()}")
        return
