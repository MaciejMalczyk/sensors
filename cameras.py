import os
import pymongo
import cv2
import datetime

mongo_client = pymongo.MongoClient("mongodb://192.168.1.102:27017")
clinostate_db = mongo_client["clinostate"]
cameras_col = clinostate_db["images"]

os.chdir('./cameras')

img0 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
cap0 = cv2.VideoCapture(0)
ret0, frame0 = cap0.read()
rgb0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2BGRA)
cv2.imwrite(str(img0), frame0)
cap0.release()
os.system('./send.sh '+img0)

img2 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
cap2 = cv2.VideoCapture(2)
ret2, frame2 = cap2.read()
rgb2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2BGRA)
cv2.imwrite(str(img2), frame2)
cap2.release()
os.system('./send.sh '+img2)

results = {
    "img0": "http://192.168.1.102:8080/"+img0,
    "img2": "http://192.168.1.102:8080/"+img2
    }

cameras_col.insert_one(results)

os.remove(img0)
os.remove(img2)

