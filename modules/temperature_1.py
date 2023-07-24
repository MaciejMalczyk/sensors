import board
import adafruit_mcp9808

# Do one reading
def get():
    with board.I2C() as i2c:
        t = adafruit_mcp9808.MCP9808(i2c, 0x1a)

        # Finally, read the temperature property and print it out
        return t.temperature
