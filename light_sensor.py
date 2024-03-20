import board
import busio
import adafruit_tsl2591

# Set up I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create the sensor object
sensor = adafruit_tsl2591.TSL2591(i2c)

# Read light levels
while True:
    print("Lux: {}".format(sensor.lux))
    time.sleep(2)  # Read every 2 seconds
