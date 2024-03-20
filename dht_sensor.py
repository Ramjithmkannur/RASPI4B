import board
import adafruit_dht

# Set up DHT sensor
dht_pin = 18  # Use any GPIO pin
dht_sensor = adafruit_dht.DHT22(board.D18)

# Read temperature and humidity
while True:
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        print("Temperature: {:.1f}°C, Humidity: {}%".format(temperature, humidity))
        time.sleep(2)  # Read every 2 seconds
    except RuntimeError as e:
        print("Error reading DHT sensor: {}".format(e))
