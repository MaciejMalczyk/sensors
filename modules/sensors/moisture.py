from .ADS1x15 import *

ADS = ADS1115(1, 0x48)

def get():
    
    try:
        # set gain to 4.096V max
        ADS.setGain(ADS.PGA_4_096V)
        
        raw = ADS.readADC(0)
        #print("Moisture: ", raw)
    except:
        print("Error: ", raw)
    
    return raw
