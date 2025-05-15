import sqlite3

# Connect to the database
conn = sqlite3.connect('weather_station.db')
c = conn.cursor()

# Specify the table name you want to delete
table_name = "weather_station"  # Change this if needed

try:
    # Drop the table if it exists
    c.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    print(f"Table '{table_name}' deleted successfully.")
except sqlite3.Error as e:
    print(f"Error deleting table: {e}")
finally:
    conn.close()
