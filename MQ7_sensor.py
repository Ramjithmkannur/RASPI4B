import RPi.GPIO as GPIO

import time

# Set the GPIO mode

GPIO.setmode(GPIO.BCM)

# Define the sensor pin

analog_pin = 25

# Define the LED pin

led_pin = 18

# Read data from the carbon monoxide sensor

def read_co_sensor(analog_pin):

    GPIO.setup(analog_pin, GPIO.IN)

    analog_value = GPIO.input(analog_pin)

    return analog_value

# Set up the LED pin as an output

GPIO.setup(led_pin, GPIO.OUT)

try:

    while True:

        co_value = read_co_sensor(analog_pin)

        print(f"Carbon Monoxide Level: {co_value}")

        # Control the LED based on carbon monoxide levels

        if co_value > 500:

            GPIO.output(led_pin, GPIO.HIGH)  # Turn on the LED

        else:

            GPIO.output(led_pin, GPIO.LOW)  # Turn off the LED

        time.sleep(1)

except KeyboardInterrupt:

    GPIO.cleanup()
    
import RPi.GPIO as GPIO
import time

# Set the GPIO mode

GPIO.setmode(GPIO.BCM)

# Define the sensor pin

analog_pin = 25

# Define the LED pin

led_pin = 18

# Read data from the carbon monoxide sensor

def read_co_sensor(analog_pin):

    GPIO.setup(analog_pin, GPIO.IN)

    analog_value = GPIO.input(analog_pin)

    return analog_value

# Set up the LED pin as an output

GPIO.setup(led_pin, GPIO.OUT)

try:

    while True:

        co_value = read_co_sensor(analog_pin)

        print(f"Carbon Monoxide Level: {co_value}")

        # Control the LED based on carbon monoxide levels

        if co_value > 500:

            GPIO.output(led_pin, GPIO.HIGH)  # Turn on the LED

        else:

            GPIO.output(led_pin, GPIO.LOW)  # Turn off the LED

        time.sleep(1)

except KeyboardInterrupt:

    GPIO.cleanup()