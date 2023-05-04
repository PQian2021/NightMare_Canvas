import websocket._app
import json
import time
import csv
from datetime import datetime
from flask import Flask, jsonify
import threading

app = Flask(__name__)


ACCESS_TOKEN = "36cf5bb2-c434-4205-82aa-17f732edc6ad"

# WebSocket URL
websocket_url = f"wss://dev.pulsoid.net/api/v1/data/real_time?access_token={ACCESS_TOKEN}"

# Shared variable to store the latest heart rate value
latest_heart_rate = {"timestamp": "", "heart_rate": 0}

# CSV file to store heart rate data
csv_file = "heart_rate_data.csv"
def on_open(ws):
    print("WebSocket connection opened")

def on_message(ws, message):
    global latest_heart_rate
    try:
        data = json.loads(message)
        heart_rate = data["data"]["heart_rate"]
        timestamp = datetime.fromtimestamp(data["measured_at"]/1000).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Timestamp: {timestamp}, Heart rate: {heart_rate}")

        # Update the latest heart rate value
        latest_heart_rate = {"timestamp": timestamp, "heart_rate": heart_rate}

        # Save data to CSV file
        with open(csv_file, "a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([timestamp, heart_rate])

    except json.JSONDecodeError:
        print("Received plain text heart rate:", message)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("WebSocket connection closed")

@app.route('/heart_rate', methods=['GET'])
def get_heart_rate():
    return jsonify(latest_heart_rate)

def run_websocket():
    global ws
    ws = websocket._app.WebSocketApp(
        websocket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    while True:
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

def run_api():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file = f"heart_rate_data_{now}.csv"

    with open(csv_file, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Heart_rate"])
    websocket_thread = threading.Thread(target=run_websocket)
    api_thread = threading.Thread(target=run_api)

    websocket_thread.start()
    api_thread.start()

    websocket_thread.join()
    api_thread.join()