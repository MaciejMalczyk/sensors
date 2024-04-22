from .apds9960 import *
import smbus
from time import sleep

port = 0
bus = smbus.SMBus(port)
apds = device.APDS9960(bus)

def get():

    apds.enableLightSensor()
    sleep(1)
    val = apds.readAmbientLight()
    return float(val)
