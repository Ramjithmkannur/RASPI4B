import RPi.GPIO as GPIO
import time

# Set up GPIO
servo_pin = 18  # Use any GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM object
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency

# Rotate the servo
try:
    pwm.start(2.5)  # Initial position
    time.sleep(2)

    pwm.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
    time.sleep(2)

    pwm.ChangeDutyCycle(12.5)  # Rotate to 180 degrees
    time.sleep(2)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
