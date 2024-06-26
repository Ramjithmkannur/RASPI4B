import RPi.GPIO as GPIO
import time

# Set up GPIO
led_pin = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)

# Turn on LED
GPIO.output(led_pin, GPIO.HIGH)
time.sleep(1)  # Keep the LED on for 5 seconds

# Turn off LED
GPIO.output(led_pin, GPIO.LOW)

# Clean up GPIO
GPIO.cleanup()
