import sqlite3

# Connect to the database
conn = sqlite3.connect('weather_station.db')
c = conn.cursor()

# Query to list all tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch and print the table names
tables = c.fetchall()
if tables:
    print("Tables in the database:")
    for table in tables:
        print(table[0])
else:
    print("No tables found.")

# Close the connection
conn.close()
