import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# MQ-2 sensor
mq2_gas_pin = 14  # Change this to the appropriate pin number
GPIO.setup(mq2_gas_pin, GPIO.IN)

# MQ-7 sensor
mq7_gas_pin = 15  # Change this to the appropriate pin number
GPIO.setup(mq7_gas_pin, GPIO.IN)

# LED indicator
led_pin = 18  # Change this to the appropriate pin number
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        # Read MQ-2 sensor value
        mq2_gas_state = GPIO.input(mq2_gas_pin)

        # Read MQ-7 sensor value
        mq7_gas_state = GPIO.input(mq7_gas_pin)

        # Check if either sensor detects gas
        if mq2_gas_state or mq7_gas_state:
            # Turn on LED indicator
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            # Turn off LED indicator
            GPIO.output(led_pin, GPIO.LOW)

        # Wait for a short period before checking again
        time.sleep(0.5)

except KeyboardInterrupt:
    # Clean up GPIO pins
    GPIO.cleanup()