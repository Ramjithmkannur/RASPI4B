#Sensor pin No 16
#vcc on pin No 1
#gnd on pin No 6
import RPi.GPIO as GPIO
import time

# Set up GPIO
sensor = 16 # Use any GPIO pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)

#check for ir sensor
print ("IR Sensor Ready......")
print ("")
# Check for motion ion
try:
    while True:
        if GPIO.input(sensor) == GPIO.LOW:
            print("Object detected!")
        else:
            print("No Object detected.")
        time.sleep(2)  # Check every 2 seconds

except KeyboardInterrupt:
    GPIO.cleanup()
