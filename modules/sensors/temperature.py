from smbus2 import SMBus
import config

from systemd import journal

try:
    bus = SMBus(config.i2c[0])

except Exception as err:
    print(f"Sensors: Temperature: Error: {err}")
    journal.send(f"Sensors: Temperature: Error:: {err}")

def get(address):
    try:
        temp = 0

        data = bus.read_word_data(address, 0x05)
        buf2 = (data & 0xff00) >> 8
        buf1 = (data & 0xff) & 0x1f

        if buf1 & 0x10 == 0x10:
            buf1 = buf1 & 0x0F
            temp = (buf1 * 16 + buf2 / 16) - 256

        temp = buf1 * 16 + buf2 / 16.0

        return temp

    except Exception as err:
        print(f"Sensors: Temperature: Read sensor error: {err}")
        journal.send(f"Sensors: Temperature: Read sensor error: {err}")



