import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)

# Set up input pin for LDR
ldr_pin = 4
GPIO.setup(ldr_pin, GPIO.IN)

# Threshold value
threshold = 100

# Main loop
while True:
    if GPIO.input(ldr_pin) > threshold:
        print("It's Sunny")
    else:
        print("It's Dark")
    time.sleep(0.1)

# Clean up
GPIO.cleanup()