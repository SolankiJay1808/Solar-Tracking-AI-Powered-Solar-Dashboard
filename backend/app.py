from flask import Flask, jsonify
from flask_cors import CORS
import serial
import time
import requests

app = Flask(__name__)
CORS(app)

# CHANGE THIS PORT
PORT = 'COM3'
API_KEY = '6c87f822ebdd5f83c409031881eee79b'
CITY = 'Jaipur'

# Connect Arduino
arduino = serial.Serial(PORT, 9600, timeout=1)

time.sleep(2)

@app.route('/')
def home():
    return "Solar Tracking Backend Running"

@app.route('/sensor-data')
def sensor_data():

    try:

        # READ ARDUINO DATA
        data = arduino.readline().decode('utf-8').strip()

        values = data.split(',')

        # WEATHER API
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

        weather_response = requests.get(weather_url).json()

        temperature = weather_response['main']['temp']

        humidity = weather_response['main']['humidity']

        weather = weather_response['weather'][0]['main']

        response = {

            "ldr_left": values[0],

            "ldr_right": values[1],

            "servo_angle": values[2],

            "voltage": values[3],

            "temperature": temperature,

            "humidity": humidity,

            "weather": weather
        }

        return jsonify(response)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
if __name__ == '__main__':
    app.run()