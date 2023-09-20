from modules import *
from multiprocessing import Process
import time

def cam():
    while True:
        cameras.send()
        time.sleep(120)
        
def water():
    while True:
        watering.send()
        time.sleep(60)
        
def light_temp():
    while True:
        light_temperature.send()
        time.sleep(120)
        
def accel():
    while True:
        acceleration.send()


if __name__ == "__main__":
    p1 = Process(target=cam)
    p2 = Process(target=water)
    p3 = Process(target=light_temp)
    p4 = Process(target=accel)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
