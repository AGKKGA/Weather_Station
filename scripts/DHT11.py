import serial
import time

baud_rate = 9600

try:
    # Replace 'COM5' with the correct port you found
    ser = serial.Serial('COM4', baud_rate, timeout=1)  
    time.sleep(2)  # Wait for connection to establish
    print("Serial port opened successfully.")

    while True:
        data = ser.readline().decode().strip()
        if data:
            print(f"Received: {data}")
        time.sleep(1)

except serial.SerialException as e:
    print(f"Error: Could not open serial port. {e}")
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
