import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the ultrasonic sensor
TRIG_PIN = 29
ECHO_PIN = 31

# Initialize the GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Function to get the distance from the ultrasonic sensor
def get_distance():
    # Send a 10 microsecond pulse to trigger the sensor
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Measure the time it takes for the pulse to return
    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()

    # Calculate the distance
    duration = end_time - start_time
    distance = duration * 17150
    distance = round(distance, 2)
    return distance

# Print the distance with two decimal places every 2 seconds
while True:
    distance = get_distance()
    print("Distance: {:.2f} cm".format(distance))
    time.sleep(2)

# Clean up the GPIO pins
GPIO.cleanup()