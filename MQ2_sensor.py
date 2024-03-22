import RPi.GPIO as GPIO
import time

# Set up GPIO
smoke_pin = 18  # Use any GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(smoke_pin, GPIO.IN)

# Check for smoke detection
try:
    while True:
        if GPIO.input(smoke_pin) == GPIO.HIGH:
            print("Smoke detected!")
        else:
            print("No smoke detected.")
        time.sleep(2)  # Check every 2 seconds

except KeyboardInterrupt:
    GPIO.cleanup()
