from .apds9960 import *
import smbus
from time import sleep

def get():
    port = 0
    bus = smbus.SMBus(port)
    apds = device.APDS9960(bus)

    apds.enableLightSensor()
    oval = -1
    sleep(1)
    val = apds.readAmbientLight()
    return val
