import time
import board
import busio
import adafruit_lis3dh

def get():
    i2c = board.I2C()
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)


    # Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
    lis3dh.range = adafruit_lis3dh.RANGE_2_G
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  Divide them by 9.806 to convert to Gs.
    x, y, z = [
        value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    ]
    
    return [x,y,z]


