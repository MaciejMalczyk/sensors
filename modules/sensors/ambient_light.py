from .apds9960 import *
import smbus
from time import sleep

port = 0

try:
    bus = smbus.SMBus(port)
    apds = device.APDS9960(bus)
except:
    print("Error: `Cannot connect to sensor apds9960 i2c0")

def get():
    apds.enableLightSensor()
    sleep(1)
    val = apds.readAmbientLight()
    return float(val)
