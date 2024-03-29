import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
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

# Define the lookup table for the MQ-7 sensor
mq7_lut = [
    0, 50, 100, 200, 500, 1000, 2000, 5000, 10000
]

def read_channel(channel):
    # Read the specified ADC channel.
    value = channel.value
    # Convert the ADC value to a voltage value (mV).
    voltage = value * conversion_factor * 6.144
    return voltage

def read_mq7(value):
    # Find the index of the closest number
    # in the lookup table
    closest = min(range(len(mq7_lut)), key=lambda i: abs(mq7_lut[i]-value))
    # Return the smoke detection value
    return mq7_lut[closest]

def read_ldr(value):
    # Convert the ADC value (in millivolts) to a light value (in lux)
    # The LDR sensitivity is 100k ohm at 1 lux
    # The LDR resistance is inversely proportional to the light
    # The voltage divider rule can be used to calculate the light value
    # Rt = 100k ohm * Vout / Vin
    # Rt = 100k ohm * (1.65 V - 0.222 V) / 0.222 V
    # Rt = 601 k ohm
    # Rg = 10 k ohm
    # Rt / (Rt + Rg) = Vout / Vin
    # Vout = (Rt * Vin) / (Rt + Rg) = 0.222 V
    # Convert the ADC value (in millivolts) to a light value (in lux)
    ldr_value = read_channel(ldr_channel)
    ldr_lux = (ldr_value - 0.222) * (601 + 10) / 10

    # Convert the ADC value (in millivolts) to a smoke detection value (in ppm)
    mq7_value = read_channel(mq7_channel)
    mq7_ppm = read_mq7(mq7_value)

    # Print the MQ-7 and LDR sensor values
    print("MQ-7 value: {:.2f} ppm, LDR value: {:.2f} lux".format(
        mq7_ppm, ldr_lux
    ))

    # Wait for a while before reading again
    time.sleep(1)