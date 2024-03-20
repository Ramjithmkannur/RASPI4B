import RPi.GPIO as GPIO
import time

# Set up GPIO
pir_pin = 18  # Use any GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)

# Check for motion detection
try:
    while True:
        if GPIO.input(pir_pin) == GPIO.HIGH:
            print("Motion detected!")
        else:
            print("No motion detected.")
        time.sleep(2)  # Check every 2 seconds

except KeyboardInterrupt:
    GPIO.cleanup()
