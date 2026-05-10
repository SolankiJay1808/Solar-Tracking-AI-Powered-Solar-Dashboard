from flask import Flask, jsonify
from flask_cors import CORS
import serial
import time

app = Flask(__name__)
CORS(app)

# CHANGE THIS PORT
PORT = 'COM3'

# Connect Arduino
arduino = serial.Serial(PORT, 9600, timeout=1)

time.sleep(2)

@app.route('/')
def home():
    return "Solar Tracking Backend Running"

@app.route('/sensor-data')
def sensor_data():
    try:
        # Read serial data
        data = arduino.readline().decode('utf-8').strip()

        print("Raw Data:", data)

        values = data.split(',')

        if len(values) != 4:
            return jsonify({
                "error": "Invalid data received",
                "raw": data
            })

        response = {
            "ldr_left": values[0],
            "ldr_right": values[1],
            "servo_angle": values[2],
            "voltage": values[3]
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == '__main__':
    app.run()