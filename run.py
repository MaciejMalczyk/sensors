from modules import *
import threading
import time
import sys
import signal

semaphore = True

def sigterm_handler(signal, frame):
    print("Killing processes")
    global semaphore
    semaphore = False
    sys.exit()


signal.signal(signal.SIGTERM, sigterm_handler)

def thread_light_temp():
    while semaphore:
        light_temperature.send()
        time.sleep(120)

def thread_acc():
    while semaphore:
        acceleration.send()
        time.sleep(150/1000)

def thread_water():
    while semaphore:
        watering.send()
        time.sleep(60)

def thread_cameras():
    while semaphore:
        cameras.send()
        time.sleep(600)

try:
    th_wt = threading.Thread(target=thread_light_temp, args=(1,))
    th_acc = threading.Thread(target=thread_acc, args=(1,))
    th_w = threading.Thread(target=thread_water, args=(1,))
    th_cam = threading.Thread(target=thread_cameras, args=(1,))
    th_wt.start()
    th_acc.start()
    th_w.start()
    th_cam.start()

except:
    print("Exiting...")
    sys.exit()
