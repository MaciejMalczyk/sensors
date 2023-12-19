from modules import *
from multiprocessing import Process
import time
import sys
import signal

semaphore = True

def sigterm_handler(signal, frame):
    print("Killing processes")
    global semaphore
    semaphore = False
    print("P1 kill")
    p1.kill()
    p1.close()
    print("P2 kill")
    p2.kill()
    p2.close()
    print("P3 kill")
    p3.kill()
    p3.close()
    print("Pcam kill")
    pcam.kill()
    pcam.close()
    print("Exit")
    sys.exit()


signal.signal(signal.SIGTERM, sigterm_handler)

def task1():
    while semaphore:
        light_temperature.send()
        time.sleep(120)

def task2():
    while semaphore:
        acceleration.send()
        time.sleep(150/1000)

def task3():
    while semaphore:
        watering.send()
        time.sleep(60)

def task_cameras():
    while semaphore:
        cameras.send()
        time.sleep(600)

try:
    p1 = Process(target=task1)
    p2 = Process(target=task2)
    p3 = Process(target=task3)
    pcam = Process(target=task_cameras)
    p1.start()
    p1.join()
    p2.start()
    p2.join()
    p3.start()
    p3.join()
    pcam.start()
    pcam.join()

except:
    print("Exiting...")
    sys.exit()
