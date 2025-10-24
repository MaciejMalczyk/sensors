from smbus2 import SMBus
import config

bus = SMBus(config.i2c[0])
device_address = 0x18

try:
    bus.write_byte_data(device_address, 0x20, 0b01110111)
    bus.write_byte_data(device_address, 0x23, 0b10001000)
except Exception as err:
    print(f"SACC: Cannot read data: {err}")


def get():
    def is_minus(v):
        if v > 2:
            v -= 4
            return v
        else:
            return v

    value = [0, 0, 0, 0, 0, 0]

    try:
        for i in range(6):
            value[i] = bus.read_byte_data(device_address, 0x28+i)

        x = -is_minus((value[1] * 256 + value[0])*(4/65535))
        y = -is_minus((value[3] * 256 + value[2])*(4/65535))
        z = -is_minus((value[5] * 256 + value[4])*(4/65535))
    except:
        x = -50
        y = -50
        z = -50

    return [x, y, z]
