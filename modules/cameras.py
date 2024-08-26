import os
import pymongo
import cv2
import datetime

from fabric import Connection

#maximum width and height of image produced by used cameras.
cam_width = 2592 #1600
cam_height = 1944 #1200

conn = Connection(
    host="golfserver",
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


mongo_client = pymongo.MongoClient("mongodb://golfserver:27017")
clinostate_db = mongo_client[db_string]
cameras_col = clinostate_db["images"]

def send():

    results = {
        "date": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    try:
        img0 = db_string+"_"+datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")+".jpg"
        cap0 = cv2.VideoCapture(0)
        cap0.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
        cap0.set(cv2.CAP_PROP_BRIGHTNESS, 5)
        cap0.set(cv2.CAP_PROP_AUTO_WB, 0)
        cap0.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        ret0, frame0 = cap0.read()
        rgb0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(str(img0), frame0)
        cap0.release()
        conn.put(img0, remote='/images')
        results["img0"] = "http://10.66.66.2:8080/"+img0
    except:
        print("CAM: Capturing img0 failed")

    try:
        img2 = db_string+"_"+datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")+".jpg"
        cap2 = cv2.VideoCapture(2)
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
        cap2.set(cv2.CAP_PROP_BRIGHTNESS, 5)
        cap2.set(cv2.CAP_PROP_AUTO_WB, 0)
        cap2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        cap2.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret2, frame2 = cap2.read()
        rgb2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(str(img2), frame2)
        cap2.release()
        conn.put(img2, remote='/images')
        results["img2"] = "http://10.66.66.2:8080/"+img2
    except:
        print("CAM: Capturing img2 failed")

    if len(results) > 1:
        try:
            print("CAM: Mongodb: sending")
            cameras_col.insert_one(results)
        except:
            print("CAM: No connection to mongodb")

        try:
            os.remove(img0)
        except:
            print("CAM: No img0 file")

        try:
            os.remove(img2)
        except:
            print("CAM: No img2 file")

    else:
        raise Exception("CAM: No cameras avaiable!")
        return


