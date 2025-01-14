from modules import *
import threading
import time
import sys
import signal
import os
import datetime

from systemd import journal

semaphore = True

def sigterm_handler(signal, frame):
    journal.send("Main: Sigterm!")
    print("Main: Sigterm!", f'{datetime.datetime.now()}')
    global semaphore
    semaphore = False
    sys.exit()

def exception_handler(exception):
    journal.send(f"Killing processes: {exception}")
    print(f"Killing processes: {exception}", f'{datetime.datetime.now()}')
    global semaphore
    semaphore = False
    sys.exit()

signal.signal(signal.SIGTERM, sigterm_handler)

def thread_light_temp():
    while semaphore:
        try:
            light_temperature.send()
        except Exception as exception:
            exception_handler(exception)
        time.sleep(120)

def thread_acc():
    while semaphore:
        try:
            acceleration.send()
        except Exception as exception:
            exception_handler(exception)
        time.sleep(150/1000)

def thread_water():
    while semaphore:
        try:
            watering.send()
        except Exception as exception:
            exception_handler(exception)
        time.sleep(60)

def thread_cameras():
   while semaphore:
       try:
           cameras.send()
       except Exception as exception:
           exception_handler(exception)
       time.sleep(600)

try:
    th_lt = threading.Thread(target=thread_light_temp)
    th_acc = threading.Thread(target=thread_acc)
    th_w = threading.Thread(target=thread_water)
    th_cam = threading.Thread(target=thread_cameras)
    th_lt.start()
    th_acc.start()
    th_w.start()
    th_cam.start()

except:
    print("Exiting...")
    sys.exit()
