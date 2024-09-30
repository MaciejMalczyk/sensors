from .apds9960 import *
import smbus
from time import sleep

def get(port):

    try:
        bus = smbus.SMBus(port)
        apds = device.APDS9960(bus)
    except:
        print(f"SAL: `Cannot connect to sensor apds9960 i2c{port}")

    apds.enableLightSensor()
    sleep(1)
    val = apds.readAmbientLight()
    return float(val)
