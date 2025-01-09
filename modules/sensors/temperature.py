from smbus2 import SMBus

bus = SMBus(1)

def get(address):
    temp = 0
    data = bus.read_word_data(address, 0x05)
    buf2 = (data & 0xff00) >> 8
    buf1 = (data & 0xff) & 0x1f
    if buf1 & 0x10 == 0x10:
        buf1 = buf1 & 0x0F
        temp = (buf1 * 16 + buf2 / 16) - 256

    temp = buf1 * 16 + buf2 / 16.0

    return temp


