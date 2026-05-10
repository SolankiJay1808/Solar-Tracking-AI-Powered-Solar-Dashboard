from flask import Flask, jsonify
from flask_cors import CORS
import serial
import time
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# CHANGE THIS PORT
PORT = 'COM3'
API_KEY = '6c87f822ebdd5f83c409031881eee79b'
CITY = 'Jaipur'

# Connect Arduino
arduino = serial.Serial(PORT, 9600, timeout=1)

time.sleep(2)
# DATABASE SETUP
conn = sqlite3.connect('database.db', check_same_thread=False)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    ldr_left TEXT,

    ldr_right TEXT,

    servo_angle TEXT,

    voltage TEXT,

    temperature TEXT,

    humidity TEXT,

    weather TEXT,

    timestamp TEXT
)
''')

conn.commit()

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
        # SAVE TO DATABASE
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
INSERT INTO sensor_data (
    ldr_left,
    ldr_right,
    servo_angle,
    voltage,
    temperature,
    humidity,
    weather,
    timestamp
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (

    values[0],
    values[1],
    values[2],
    values[3],
    str(temperature),
    str(humidity),
    str(weather),
    timestamp
))

        conn.commit()

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
@app.route('/history')
def history():

    try:

        cursor.execute('''
        SELECT * FROM sensor_data
        ORDER BY id DESC
        LIMIT 20
        ''')

        rows = cursor.fetchall()

        history_data = []

        for row in rows:

            history_data.append({

                "id": row[0],

                "ldr_left": row[1],

                "ldr_right": row[2],

                "servo_angle": row[3],

                "voltage": row[4],

                "temperature": row[5],

                "humidity": row[6],

                "weather": row[7],

                "timestamp": row[8]
            })

        return jsonify(history_data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
if __name__ == '__main__':
    app.run()