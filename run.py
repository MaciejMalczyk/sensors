from modules import *
from multiprocessing import Process
import time
import signal

def sigterm_handler(signal, frame):
    p1.terminate()
    p2.terminate()
    p3.terminate()
    pcam.terminate()
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)

def task1():
    while True:
        light_temperature.send()
        time.sleep(120)

def task2():
    while True:
        acceleration.send()
        time.sleep(150/1000)

def task3():
    while True:
        watering.send()
        time.sleep(60)

def task_cameras():
    while True:
        cameras.send()
        time.sleep(600)


try:
    p1 = Process(target=task1)
    p2 = Process(target=task2)
    p3 = Process(target=task3)
    pcam = Process(target=task_cameras)
    p1.start()
    p2.start()
    p3.start()
    pcam.start()
    p1.join()
    p2.join()
    p3.join()
    pcam.join()
except KeyboardInterrupt:
    p1.terminate()
    p2.terminate()
    p3.terminate()
    pcam.terminate()

