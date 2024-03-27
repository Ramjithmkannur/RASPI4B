import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)

# Pin connected to the LDR sensor
ldr_pin = 4

# Set up the LDR pin as an input
GPIO.setup(ldr_pin, GPIO.IN)

# Function to detect if it is light or dark
def rc_time(ldr_pin):
    # Initialize the count variable
    count = 0
    
    # Output on the pin for 100ms
    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    time.sleep(0.1)
    
    # Change the pin back to input
    GPIO.setup(ldr_pin, GPIO.IN)
    
    # Count until the pin goes high
    while GPIO.input(ldr_pin) == GPIO.LOW:
        count += 1
    
    # Return the count value
    return count

# Print a message and wait for a key press
def print_message():
    print("Press Enter to start or Ctrl+C to stop.")
    input()

# Continuous loop to detect if it is light or dark
while True:
    try:
        print("Detecting light...")
        count = rc_time(ldr_pin)
        if count > 100000:
            print("It's dark!")
        else:
            print("It's light!")
        time.sleep(1)
    
    except KeyboardInterrupt:
        # Clean up GPIO pins
        GPIO.cleanup()
        break

print_message()