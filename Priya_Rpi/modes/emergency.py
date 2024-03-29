import requests
import time
from mq2_sensor import MQ2Sensor  # Assuming you have a library for interfacing with the MQ2 sensor
from flask import Flask, jsonify, request
from smokedetfeatures.powermanage import init_power_management

app = Flask(__name__)

# Function to detect smoke and determine severity level
def detect_smoke():
    mq2_sensor = MQ2Sensor()  # Initialize the MQ2 sensor
    smoke_ppm = mq2_sensor.read_ppm()  # Read smoke concentration in ppm

    # Define severity levels based on ppm ranges
    if smoke_ppm < 200:
        severity = "Low"
    elif 200 <= smoke_ppm < 700:
        severity = "Moderately High"
    elif 700 <= smoke_ppm < 4000:
        severity = "High"
    else:
        severity = "Dangerous"

    return smoke_ppm, severity

# Function to retrieve user address from Flask API
def get_user_address():
    # Send GET request to Flask API to retrieve user's address
    response = requests.get("http://localhost:5000/user/address")

    # Extract user's address from the response JSON
    user_address = response.json().get("address")
    return user_address

# Function to fetch emergency numbers from Emergency Number API
def get_emergency_numbers():
    url = "https://emergencynumberapi.com/api/?country_code=US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "police": data.get("police"),
            "fire": data.get("fire"),
            "ambulance": data.get("ambulance")
        }
    else:
        return None

# Function to send emergency alert
def send_emergency_alert(address, severity, local_services):
    # Extract local emergency numbers
    police_number = local_services.get("police")
    fire_number = local_services.get("fire")
    ambulance_number = local_services.get("ambulance")

    # Compose message with address and severity
    message = f"Emergency at {address}. Severity: {severity}"

    # Send alert to local emergency services
    requests.post(police_number, json={"message": message})
    requests.post(fire_number, json={"message": message})
    requests.post(ambulance_number, json={"message": message})
    
# Function to activate power management
def activate_power_management():
    # Turn off all electrical appliances
    # Here, you can add code to control other GPIO pins to turn off appliances
    # For demonstration purposes, let's print a message
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"The power appliances are turned off as the smoke detected is moderately high at {time_now}"
    print("Activating power management:", message)

    # Switch electricity of home to backup generators or battery backups
    GPIO.output(POWER_RELAY_PIN, GPIO.LOW)

    # Post message to Flask API
    requests.post("http://localhost:5000/power_off", json={"message": message})

# Function to switch to backup generators or battery
def switch_to_backup():
    # Here, you can add code to switch to backup generators or battery
    # For demonstration purposes, let's print a message
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"The backup generators or battery have been switched on at {time_now}"
    print("Switching to backup generators or battery:", message)

    # Post message to Flask API
    requests.post("http://localhost:5000/switch_to_backup", json={"message": message})

# Route to retrieve stored smoke detection events
@app.route('/smoke_events', methods=['GET'])
def get_smoke_events():
    return jsonify(smoke_events), 200

# Route to handle power off event
@app.route('/power_off', methods=['POST'])
def power_off():
    request_data = request.json
    message = request_data.get("message")
    print("Received power off message:", message)
    # Perform any additional actions if required
    return jsonify({"status": "Received power off message"}), 200

# Route to handle switch to backup event
@app.route('/switch_to_backup', methods=['POST'])
def switch_to_backup():
    request_data = request.json
    message = request_data.get("message")
    print("Received switch to backup message:", message)
    # Perform any additional actions if required
    return jsonify({"status": "Received switch to backup message"}), 200


# Route to send emergency alert
@app.route('/emergency_alert', methods=['POST'])
def emergency_alert():
    # Example request body: {"address": "123 Main St", "severity": "high"}
    request_data = request.json
    address = request_data.get("address")
    severity = request_data.get("severity")

    # Fetch local emergency numbers
    local_services = get_emergency_numbers()

    if local_services:
        # Send emergency alert
        send_emergency_alert(address, severity, local_services)
        return jsonify({"status": "Emergency alert sent"}), 200
    else:
        return jsonify({"error": "Failed to fetch emergency numbers"}), 500

# Route to send notification to the user
@app.route('/send_notification', methods=['POST'])
def send_notification():
    # Example request body: {"message": "Notification message"}
    request_data = request.json
    message = request_data.get("message")

    # Send notification to the user
    user_endpoint = "http://localhost:5000/user/notification"
    response = requests.post(user_endpoint, json={"message": message})

    if response.status_code == 200:
        return jsonify({"status": "Notification sent"}), 200
    else:
        return jsonify({"error": "Failed to send notification"}), 500

# Main function
def main():
    while True:
        # Detect smoke and determine severity
        smoke_ppm, severity = detect_smoke()
        
        #running power management
        init_power_management()

        # If smoke is detected
        if severity != "Moderate":
            # Retrieve user's address from Flask API
            user_address = get_user_address()

            # Send emergency alert
            response = requests.post("http://localhost:5000/emergency_alert", json={"address": user_address, "severity": severity})
            if response.status_code == 200:
                print("Emergency alert sent successfully.")
            else:
                print("Failed to send emergency alert.")

            # Send notification to the user
            response = requests.post("http://localhost:5000/send_notification", json={"message": "Emergency alert: " + severity})
            if response.status_code == 200:
                print("Notification sent successfully.")
            else:
                print("Failed to send notification.")

        time.sleep(300)  # Check for smoke every 5 minutes

if __name__ == "__main__":
    main()
