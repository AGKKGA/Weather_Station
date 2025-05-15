import serial
import time

# Configuration
port = 'COM4'  # Update with your correct COM port
baud_rate = 9600  # Same as in the Arduino code

try:
    # Establish serial connection
    ser = serial.Serial(port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for the connection to stabilize
    print("Connected to Arduino Nano on", port)

    while True:
        # Read data from serial port
        data = ser.readline().decode().strip()

        if data:
            try:
                # Extract raw value and voltage from the received data
                if "Raw Value" in data:
                    parts = data.split(",")
                    raw_value = int(parts[0].split(": ")[1])
                    voltage = float(parts[1].split(": ")[1])

                    # Basic air quality interpretation
                    
                    if voltage < 0.5:
                        air_quality = "Clean Air"
                    elif 0.5 < voltage <= 2.2:
                        air_quality = "Moderate Pollution"
                    elif 2.2 < voltage <= 3.5:
                        air_quality = "High Pollution"
                    else:
                        air_quality = "Severe Pollution"

                    # Print the air quality
                    print(f"Raw Value: {raw_value}, Voltage: {voltage:.2f}V, Air Quality: {air_quality}")
            except (IndexError, ValueError):
                print(f"Invalid data received: {data}")

except serial.SerialException as e:
    print(f"Error: Could not open serial port. {e}")
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
