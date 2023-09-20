import os
import time
import ADS1x15

def get():

    ADS = ADS1x15.ADS1115(1, 0x48)

    # set gain to 4.096V max
    ADS.setGain(ADS.PGA_4_096V)
    
    raw = ADS.readADC(0)
    
    return raw
