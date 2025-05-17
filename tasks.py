from invoke import task
import subprocess

@task
def dev(ctx):
    """Run both the data collection script and the Flask app."""
    try:
        # Run the data collection script in the background
        data_process = subprocess.Popen(["python", "scripts/MQ2andDHT11.py"])
        print("Data collection started...")

        # Run the Flask app
        flask_process = subprocess.Popen(["python", "weather_app/app.py"])
        print("Flask app started at http://0.0.0.0:5000")

        # Keep both processes running
        data_process.wait()
        flask_process.wait()

    except KeyboardInterrupt:
        print("Shutting down...")
        data_process.terminate()
        flask_process.terminate()
    finally:
        print("Processes terminated.")
