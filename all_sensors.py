import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_dht
import adafruit_tsl2591

# Set up GPIO
led_pin = 18
smoke_pin = 23  # Use any GPIO pin
pir_pin = 24  # Use any GPIO pin
servo_pin = 25  # Use any GPIO pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(smoke_pin, GPIO.IN)
GPIO.setup(pir_pin, GPIO.IN)

# Set up DHT sensor
dht_sensor = adafruit_dht.DHT22(board.D18)

# Set up I2C
i2c = busio.I2C(board.SCL, board.SDA)
tsl_sensor = adafruit_tsl2591.TSL2591(i2c)

# Set up servo motor
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency

def turn_on_led():
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(5)  # Keep the LED on for 5 seconds
    GPIO.output(led_pin, GPIO.LOW)

def detect_smoke():
    if GPIO.input(smoke_pin) == GPIO.HIGH:
        print("Smoke detected!")
    else:
        print("No smoke detected.")

def detect_motion():
    if GPIO.input(pir_pin) == GPIO.HIGH:
        print("Motion detected!")
    else:
        print("No motion detected.")

def rotate_servo():
    pwm.start(2.5)  # Initial position
    time.sleep(2)
    pwm.ChangeDutyCycle(7.5)  # Rotate to 90 degrees
    time.sleep(2)
    pwm.ChangeDutyCycle(12.5)  # Rotate to 180 degrees
    time.sleep(2)
    pwm.stop()

def read_light_sensor():
    print("Lux: {}".format(tsl_sensor.lux))

def read_temperature_humidity():
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        print("Temperature: {:.1f}°C, Humidity: {}%".format(temperature, humidity))
    except RuntimeError as e:
        print("Error reading DHT sensor: {}".format(e))

try:
    turn_on_led()
    detect_smoke()
    detect_motion()
    rotate_servo()
    read_light_sensor()
    read_temperature_humidity()

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
