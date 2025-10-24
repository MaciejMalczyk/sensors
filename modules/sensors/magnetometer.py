from smbus2 import SMBus
import config

try:
    bus = SMBus(config.i2c[0])
    device_address = 0x0D

    # From QMC5883L documentation
    bus.write_byte_data(device_address, 0x0b, 0x01)
    # Setup device: Over sample ratio: 512; Range: 2 Gauss; Data rate: 200Hz; Mode: Continuous;
    bus.write_byte_data(device_address, 0x09, 0x0d)

except Exception as err:
    print(f"SM: No magnetometer device found: {err}")


def get():
    try:
        # Read status regster. If bit 0 == 1 that data is ready
        ready = bus.read_byte_data(device_address, 0x06)

        if (bin(ready)[-1] == "1"):
            # ["x", "y", "z"]
            ret = [0, 0, 0]
            for i in range(0, 6, 2):
                lsb = bus.read_byte_data(device_address, 0x00+i)
                msb = bus.read_byte_data(device_address, 0x01+i)
                sign = msb >> 7

                if sign == 0:
                    val = -(2 - (-(((msb & 0b01111111) << 8) + lsb) + pow(2, 15)) * 2/pow(2, 15))
                else:
                    val = (-(((msb & 0b01111111) << 8) + lsb) + pow(2, 15)) * 2/pow(2, 15)

                ret[int(i/2)] = val
            return ret
        else:
            print("SM: Magnetometer data not ready")
            return [-1, -1, -1]

    except Exception as err:
        print(f"SM: Magnetometer measurment error: {err}")


def get_temperature():
    try:
        t_lsb = bus.read_byte_data(device_address, 0x07)
        t_msb = bus.read_byte_data(device_address, 0x08)
        t_val = (t_msb << 8) + t_lsb

        return t_val
    except Exception as err:
        print(f"SM: Magnetometer temperature measurment error: {err}")
