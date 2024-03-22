import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)
ldr_pin = 7
GPIO.setup(ldr_pin, GPIO.IN)

def detect_light():
    while True:
        # Read the value from the LDR sensor
        ldr_value = GPIO.input(ldr_pin)

        # If the LDR value is 1 (light detected), print a message
        if ldr_value == 0:
            print("It's DARK")
        else:
            print("It's light")

        # Wait for a second before checking again
        time.sleep(1)

# Run the light detection function
detect_light()