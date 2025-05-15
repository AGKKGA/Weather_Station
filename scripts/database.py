import serial
import sqlite3
import time
from datetime import datetime

# Configuration
port = 'COM4'  # Update this to your actual port
baud_rate = 9600

try:
    # Connect to Arduino Nano
    ser = serial.Serial(port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for the connection to establish
    print("Connected to Arduino Nano on", port)

    # Connect to the SQLite database
    conn = sqlite3.connect('weather_station.db')
    c = conn.cursor()

    while True:
        try:
            # Read data from serial port
            data = ser.readline().decode().strip()

            if data:
                # Split and process the received data
                parts = data.split(",")
                if len(parts) == 5:
                    temperature = float(parts[0].split(": ")[1])
                    humidity = float(parts[1].split(": ")[1])
                    mq2_raw_value = float(parts[2].split(": ")[1])
                    voltage = float(parts[3].split(": ")[1])
                    air_quality = parts[4].split(": ")[1]

                    # Create a timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Insert data into the database
                    c.execute("INSERT INTO weather_station VALUES (?, ?, ?, ?, ?, ?)", 
                              (temperature, humidity, mq2_raw_value, voltage, air_quality, timestamp))
                    conn.commit()

                    print(f"Data Stored: T={temperature}°C, H={humidity}%, MQ2={mq2_raw_value}, V={voltage}V, AQ={air_quality}, Time={timestamp}")
                else:
                    print(f"Invalid data format: {data}")

            # Wait for 2 seconds before next reading
            time.sleep(2)

        except (ValueError, IndexError) as e:
            print(f"Error parsing data: {e}, Received Data: {data}")

except serial.SerialException as e:
    print(f"Serial port error: {e}")

except KeyboardInterrupt:
    print("Data collection stopped.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")
