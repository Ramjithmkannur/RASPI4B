import os
import sys
import RPi.GPIO as GPIO
import requests
import json
from datetime import datetime
from mq2_sensor import MQ2Sensor
import Adafruit_DHT

# Initialize the MQ2 sensor
mq2_sensor = MQ2Sensor(smoke_pin)

# Setup GPIO pins
light_pin = 18
fan_pin = 23
ac_pin = 24
door_pin = 11
window_pin = 16
smoke_pin = 9

# Set up DHT11 sensor
DHT11_PIN = 25

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.OUT)
GPIO.setup(fan_pin, GPIO.OUT)
GPIO.setup(ac_pin, GPIO.OUT)
GPIO.setup(door_pin, GPIO.OUT)
GPIO.setup(window_pin, GPIO.OUT)
GPIO.setup(smoke_pin, GPIO.OUT)

app = Flask(__name__)

# Read data from DHT11 sensor
def read_dht11_data():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11_PIN)
    if humidity is not None and temperature is not None:
        result = {'temperature': temperature, 'humidity': humidity}
    else:
        result = {'temperature': None, 'humidity': None}

    return result

# Smoke detection management
def smoke_status(status):
    if status == 'smoke detected':
        mq2_sensor.detect_smoke()
    elif status == 'no smoke detected':
        mq2_sensor.clear_smoke()

# Light status management
def light_status(status):
    if status == 'on':
        GPIO.output(light_pin, GPIO.HIGH)
    elif status == 'off':
        GPIO.output(light_pin, GPIO.LOW)

# Fan status management
def fan_status(status):
    if status == 'on':
        GPIO.output(fan_pin, GPIO.HIGH)
    elif status == 'off':
        GPIO.output(fan_pin, GPIO.LOW)

# AC status management
def ac_status(status):
    if status == 'on':
        GPIO.output(ac_pin, GPIO.HIGH)
    elif status == 'off':
        GPIO.output(ac_pin, GPIO.LOW)

# Function to get status of the door
def door_status():
    if GPIO.input(door_pin) == GPIO.HIGH:
        return 'open'
    else:
        return 'closed'

# Function to get status of the window
def window_status():
    if GPIO.input(window_pin) == GPIO.HIGH:
        return 'open'
    else:
        return 'closed'

# Create the /status endpoint
@app.route('/api/status', methods=['GET'])
def status():
    smoke = mq2_sensor.get_smoke_status()
    light = GPIO.input(light_pin)
    fan = GPIO.input(fan_pin)
    ac = GPIO.input(ac_pin)
    dh11_data = read_dht11_data()
    door = door_status()
    window = window_status()

    status = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'light': 'on' if light == GPIO.HIGH else 'off',
        'fan': 'on' if fan == GPIO.HIGH else 'off',
        'ac': 'on' if ac == GPIO.HIGH else 'off',
        'smoke':'smoke detected' if smoke else 'no smoke detected',
        'temperature': dh11_data['temperature'],'humidity': dh11_data['humidity'],
        'door_status': 'open' if door == 'open' else 'closed',
        'window': 'open' if window == 'open' else 'closed',
    }

    return jsonify(status)

# Define a route tohandle POST requests for controlling the devices
@app.route('/api/control', methods=['POST'])
def control_devices():
    req_data = request.get_json()

    if 'devices' in req_data:
        devices = req_data['devices']

        for device_name, status in devices.items():
            if device_name == 'light':
                light_status(status)
            elif device_name == 'fan':
                fan_status(status)
            elif device_name == 'ac':
                ac_status(status)
            elif device_name == 'door':
                if status == 'open':
                    GPIO.output(door_pin, GPIO.LOW)
                elif status == 'close':
                    GPIO.output(door_pin, GPIO.HIGH)
            elif device_name == 'window':
                if status == 'open':
                    GPIO.output(window_pin, GPIO.LOW)
                 elif status == 'close':
                    GPIO.output(door_pin, GPIO.HIGH)
            elif device_name == 'smoke':
                if status == 'smoke detected':
                    mq2_sensor.detect_smoke()
                elif status == 'no smoke detected':
                    mq2_sensor.clear_smoke()

    return jsonify({'status': 'Devices updated'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
