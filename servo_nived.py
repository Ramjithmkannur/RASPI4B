import RPi.GPIO as GPIO
import time

servo1_pin = 7
servo2_pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Create a PWM object
pwm = GPIO.PWM(servo2_pin, 50)

# Function to set servo angle
def set_servo_angle(angle):
    duty_cycle = (angle / 18.0) + 2
    pwm.ChangeDutyCycle(duty_cycle)

# Set initial position
set_servo_angle(0)
time.sleep(1)

# Rotate servo 90 degrees
set_servo_angle(190)
time.sleep(1)

# Print message
print("Servo motor successfully moved 90 degrees")

# Clean up GPIO
pwm.stop()
GPIO.cleanup()