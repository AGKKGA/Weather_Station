from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('weather_station.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM weather_station ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/history')
def history():
    conn = get_db_connection()
    data = conn.execute("""
                        SELECT * FROM weather_station
                        WHERE strftime('%M', timestamp) % 5 = 0
                        ORDER BY timestamp DESC
                        LIMIT 50
                    """).fetchall()
    conn.close()
    return render_template('history.html', data=data)

@app.route('/api/latest')
def api_latest():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM weather_station ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    
    # Convert the SQLite Row to a dictionary
    if data:
        data_dict = {
            'temperature': data['temperature'],
            'humidity': data['humidity'],
            'mq2_raw_value': data['mq2_raw_value'],
            'voltage': data['voltage'],
            'air_quality': data['air_quality'],
            'timestamp': data['timestamp']
        }
        return jsonify(data_dict)
    else:
        return jsonify({'error': 'No data available'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)