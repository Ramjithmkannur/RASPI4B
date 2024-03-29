import os
import sys
import RPi.GPIO as GPIO
import requests
import json
from datetime import datetime
import Adafruit_DHT

# Setup GPIO pins
light_pin = 18
fan_pin = 23
ac_pin = 24

# Set up DHT11 sensor
DHT11_PIN = 25

# Set up Window and door
window_pin = 11
door_pin = 16

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.OUT)
GPIO.setup(fan_pin, GPIO.OUT)
GPIO.setup(ac_pin, GPIO.OUT)
GPIO.setup(door_pin, GPIO.OUT)
GPIO.setup(window_pin, GPIO.OUT)

app = Flask(__name__)

# Read data from DHT11 sensor
def read_dht11_data():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11_PIN)
    if humidity is not None and temperature is not None:
        result = {'temperature': temperature, 'humidity': humidity}
    else:
        result = {'temperature': None, 'humidity': None}

    return result

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
    if status == 'open':
        GPIO.input(door_pin, GPIO.HIGH)
    elif status == 'closed':
        GPIO.input(door_pin, GPIO.LOW)
        

# Function to get status of the window
def window_status():
    if status == 'open':
        GPIO.input(window_pin, GPIO.HIGH)
    elif status == 'closed':
        GPIO.input(window_pin, GPIO.LOW)
        
 # Create the /status endpoint
@app.route('/api/status', methods=['GET'])
def status():
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
        'temperature': dh11_data['temperature'],
        'humidity': dh11_data['humidity'],
        'door_status': 'open' if door == GPIO.HIGH else 'closed',
        'window': 'open' if window == GPIO.HIGH else 'closed',
    }

    return jsonify(status)

# Define a route to handle POST requests for controlling the devices
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
                door_status(status)
                # Update the door status after setting its value
                status_dict = {'door_status': 'open' if GPIO.input(door_pin) else 'closed'}
            elif device_name == 'window':
                window_status(status)
                # Update the window status after setting its value
                status_dict = {'window': 'open' if GPIO.input(window_pin) else 'closed'}

            if device_name in ['light', 'fan', 'ac']:
                # Update the status of the controllable device
                status_dict[device_name] = 'on' if status == 'true' else 'off'

        # Return the updated status in the response
        return jsonify(status_dict)

    else:
        return jsonify({'error': 'No devices specified in the request'}), 400

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(light_pin, GPIO.OUT)
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.setup(ac_pin, GPIO.OUT)
    GPIO.setup(door_pin, GPIO.OUT)
    GPIO.setup(window_pin, GPIO.OUT)
    app.run(debug=True, host='0.0.0.0', port=8000)

