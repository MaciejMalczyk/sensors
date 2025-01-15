from modules import acceleration, cameras, watering, light_temperature
import threading
import time
import sys
import signal
import datetime

from systemd import journal

semaphore = threading.Event()

def sigterm_handler(signal, frame):
    journal.send("Main: Sigterm!")
    print("Main: Sigterm!", f'{datetime.datetime.now()}')
    semaphore.set()
    sys.exit()

def exception_handler(exception):
    journal.send(f"Killing processes: {exception}")
    print(f"Killing processes: {exception}", f'{datetime.datetime.now()}')
    semaphore.set()
    sys.exit()

signal.signal(signal.SIGTERM, sigterm_handler)

def thread_light_temp():
    while not semaphore.is_set():
        try:
            light_temperature.send()
        except Exception as exception:
            exception_handler(exception)
        semaphore.wait(120)

def thread_acc():
    while not semaphore.is_set():
        try:
            acceleration.send()
        except Exception as exception:
            exception_handler(exception)
        semaphore.wait(150/1000)

def thread_water():
    while not semaphore.is_set():
        try:
            watering.send()
        except Exception as exception:
            exception_handler(exception)
        semaphore.wait(60)

def thread_cameras():
   while not semaphore.is_set():
       try:
           cameras.send()
       except Exception as exception:
           exception_handler(exception)
       semaphore.wait(600)

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
