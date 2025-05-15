import sqlite3
from datetime import datetime

# Connection to database
conn = sqlite3.connect('weather_station.db')
c = conn.cursor()

# Retrieve all data from the weather_station table
c.execute("SELECT * FROM weather_station")
rows = c.fetchall()

# Check if the table has any data
if rows:
    print("Data in the table:")
    for row in rows:
        print(f"Temperature: {row[0]}°C, Humidity: {row[1]}%, MQ2 Raw Value: {row[2]}, Voltage: {row[3]}V, Air Quality: {row[4]}, Timestamp: {row[5]}")
else:
    print("The table is empty or does not exist.")

# Close the connection
conn.close()
