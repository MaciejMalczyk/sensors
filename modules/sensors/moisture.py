from .ADS1x15 import *
import config

try:
    ADS = ADS1115(config.i2c[0], 0x48)
except:
    print("Moisture error")

def get():

    raw = -1
    
    try:
        # set gain to 4.096V max
        ADS.setGain(ADS.PGA_4_096V)
        
        raw = ADS.readADC(0)
        # print("Moisture: ", raw)
    except:
        print("SM: Error: ", raw)
    
    return raw
