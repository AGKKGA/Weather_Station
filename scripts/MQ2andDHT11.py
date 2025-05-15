import serial
import time
import sqlite3
from datetime import datetime

# Configuration
port = 'COM4'  # Update with the correct COM port
baud_rate = 9600  # Match the baud rate with Arduino

def get_db_connection():
    conn = sqlite3.connect('weather_station.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_data(temperature, humidity, mq2_raw_value, voltage, air_quality):
    try:
        conn = get_db_connection()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute("INSERT INTO weather_station (temperature, humidity, mq2_raw_value, voltage, air_quality, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                     (temperature, humidity, mq2_raw_value, voltage, air_quality, timestamp))
        conn.commit()
        conn.close()
        print("Data inserted successfully into the database.")
    except Exception as e:
        print(f"Error inserting data into database: {e}")

try:
    # Establish serial connection to Arduino
    ser = serial.Serial(port, baud_rate, timeout=1)
    time.sleep(2)  # Stabilize connection
    print("Connected to Arduino on", port)

    while True:
        data = ser.readline().decode().strip()

        if data:
            print(f"Received Data: {data}")
            parts = data.split(", ")
            try:
                temperature = float(parts[0].split(": ")[1].replace("°C", ""))
                humidity = float(parts[1].split(": ")[1].replace("%", ""))
                mq2_raw_value = int(parts[2].split(": ")[1])
                voltage = float(parts[3].split(": ")[1])
                air_quality = parts[4].split(": ")[1].strip()

                print(f"Temperature: {temperature}°C, Humidity: {humidity}%, MQ2 Raw Value: {mq2_raw_value}, Voltage: {voltage:.2f}V, Air Quality: {air_quality}")

                insert_data(temperature, humidity, mq2_raw_value, voltage, air_quality)
            except (IndexError, ValueError) as e:
                print(f"Error parsing data: {e}. Data parts: {parts}")

        time.sleep(2)

except serial.SerialException as e:
    print(f"Error: Could not open serial port. {e}")
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
