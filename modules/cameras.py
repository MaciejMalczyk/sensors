import os
import pymongo
import cv2
import datetime

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
    
    check = 0
    
    os.chdir('./modules/cameras')
    
    try: 
        img0 = db_string+"_"+datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")+".jpg"
        cap0 = cv2.VideoCapture(0)
        ret0, frame0 = cap0.read()
        rgb0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(str(img0), frame0)
        cap0.release()
        os.system('./send.sh '+img0)
        results["img0"] = "http://10.66.66.2:8080/"+img0
    except:
        print("CAM: Capturing img0 failed")
        check = check + 1
    
    try:
        img2 = db_string+"_"+datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")+".jpg"
        cap2 = cv2.VideoCapture(2)
        ret2, frame2 = cap2.read()
        rgb2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(str(img2), frame2)
        cap2.release()
        os.system('./send.sh '+img2)
        results["img2"] = "http://10.66.66.2:8080/"+img2
    except:
        print("CAM: Capturing img2 failed")
        check = check + 1
    
    if check == 2:
        os.chdir('../../')
        return
    
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

    os.chdir('../../')
