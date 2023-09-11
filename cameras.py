import os
import subprocess
import pymongo
# 
# mongo_client = pymongo.MongoClient("mongodb://192.168.1.102:27017")
# clinostate_db = mongo_client["clinostate"]
# cameras_col = clinostate_db["cameras"]

os.chdir('./cameras')

os.system('./video0.sh')
video0 = subprocess.check_output("ls video0_*", shell=True)
img0 = video0.decode("utf-8")

os.system('./video2.sh')
video2 = subprocess.check_output("ls video2_*", shell=True)
img2 = video2.decode("utf-8")

results = {
    "img0": "http://192.168.1.102:8080/"+img0,
    "img2": "http://192.168.1.102:8080"+img2
    }

# cameras_col.insert_one(results)

os.remove(img0[:-1])
os.remove(img2[:-1])

