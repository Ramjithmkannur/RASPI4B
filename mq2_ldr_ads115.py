import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
#from adafruit_ads1x15.ads1115 import AnalogIn
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Define the LDR and MQ-7 sensor channels
ldr_channel = AnalogIn(ads, ADS.P0)
mq7_channel = AnalogIn(ads, ADS.P1)

# Define the conversion factor for the ADC (mV per bit)
conversion_factor = 3.0 / 32768.0

def read_channel(channel):
    # Read the specified ADC channel.
    value = channel.value
    # Convert the ADC value to a voltage value (mV).
    voltage = value * conversion_factor * 6.144
    return voltage

while True:
    # Read the LDR and MQ-7 sensor values.
    ldr_value = read_channel(ldr_channel)
    mq7_value = read_channel(mq7_channel)
    # Print the LDR and MQ-7 sensor values.
    print("LDR value: {:.2f} mV, MQ-7 value: {:.2f} mV".format(ldr_value, mq7_value))
    #print("MQ-7 value: {:.2f} mV".format(mq7_value))
    # Wait for a while before reading again.
    time.sleep(1)