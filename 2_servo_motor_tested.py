import RPi.GPIO as GPIO
import time

servo1_pin = 13
servo2_pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

def set_servo_angle(pin, angle):
    duty_cycle = angle / 18.0 + 3
    pwm = GPIO.PWM(pin, 100)
    pwm.start(10)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    pwm.stop()

while True:
    try:
        # Set servo 1 to angle 45
        set_servo_angle(servo1_pin, 120)
        while True:
            try:
                # Wait for 2 seconds
                time.sleep(2)
                break
            except KeyboardInterrupt:
                GPIO.cleanup()

        # Set servo 2 to angle 135
        set_servo_angle(servo2_pin, 120)
        while True:
            try:
                # Wait for 2 seconds
                time.sleep(2)
                break
            except KeyboardInterrupt:
                GPIO.cleanup()

    except KeyboardInterrupt:
        GPIO.cleanup()
        break