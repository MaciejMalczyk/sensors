import os
import pymongo
import cv2
import datetime

mongo_client = pymongo.MongoClient("mongodb://golfserver:27017")
clinostate_db = mongo_client["clinostate"]
cameras_col = clinostate_db["images"]

def send():
    
    results = {
        "date": datetime.datetime.now(tz=datetime.timezone.utc)
    }
    
    check = 0
    
    os.chdir('./modules/cameras')
    
    try: 
        img0 = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")+".jpg"
        cap0 = cv2.VideoCapture(0)
        ret0, frame0 = cap0.read()
        rgb0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(str(img0), frame0)
        cap0.release()
        os.system('./send.sh '+img0)
        results["img0"] = "http://192.168.100.1:8080/"+img0
    except:
        print("Capturing img0 failed")
        check = check + 1
    
    try:
        img2 = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")+".jpg"
        cap2 = cv2.VideoCapture(2)
        ret2, frame2 = cap2.read()
        rgb2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(str(img2), frame2)
        cap2.release()
        os.system('./send.sh '+img2)
        results["img2"] = "http://192.168.100.1:8080/"+img2
    except:
        print("Capturing img2 failed")
        check = check + 1
    
    if check == 2:
        os.chdir('../../')
        return
    
    try:
        print("Mongodb: sending")
        cameras_col.insert_one(results)
    except:
        print("No connection to mongodb")

    try:
        os.remove(img0)
    except:
        print("No img0 file")
        
    try:
        os.remove(img2)
    except:
        print("No img2 file")

    os.chdir('../../')
