import board
import adafruit_mcp9808

def get(address):
    with board.I2C() as i2c:
        t = adafruit_mcp9808.MCP9808(i2c, address)

        # Finally, read the temperature property and print it out
        return t.temperature

