import asyncio
import os
import sys
import csv
from datetime import datetime
from bleak import BleakScanner, BleakClient, BleakError
from flask import Flask, jsonify
from threading import Thread

HRM_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HRM_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

app = Flask(__name__)

heart_rate_data = []
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_file = f"heart_rate_data_{now}.csv"

async def heart_rate_handler(sender, data):
    global heart_rate_data

    flags = data[0]
    contact_sensor_status = (flags >> 1) & 0b11
    has_energy_expended = (flags >> 3) & 0b1
    has_rr_interval = (flags >> 4) & 0b1
    is_short = flags & 0b1

    if is_short:
        heart_rate = int.from_bytes(data[1:3], byteorder="little")
    else:
        heart_rate = int(data[1])

    energy_expended = None
    rr_intervals = None

    if has_energy_expended:
        energy_expended = int.from_bytes(data[3:5], byteorder="little")
        if has_rr_interval:
            rr_intervals = [
                int.from_bytes(data[i: i + 2], byteorder="little")
                for i in range(5, len(data), 2)
            ]
    else:
        if has_rr_interval:
            rr_intervals = [
                int.from_bytes(data[i: i + 2], byteorder="little")
                for i in range(2, len(data), 2)
            ]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Timestamp: {timestamp}, Heart rate: {heart_rate}, RR intervals: {rr_intervals}")

    heart_rate_data.append((timestamp, heart_rate, rr_intervals))

    with open(csv_file, "a") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([timestamp, heart_rate, rr_intervals])


async def connect_and_subscribe(address):
    async with BleakClient(address) as client:
        try:
            await client.start_notify(HRM_CHARACTERISTIC_UUID, heart_rate_handler)
            await asyncio.sleep(1800.0)
        except BleakError as e:
            print(f"Error while connecting: {e}")
        finally:
            await client.stop_notify(HRM_CHARACTERISTIC_UUID)


async def scan_and_connect():
    input("Press Enter to begin scanning... ")
    while True:
        devices = await BleakScanner.discover()
        for d in devices:
            if HRM_SERVICE_UUID in d.metadata["uuids"]:
                address = d.address
                print(f"Connecting to HRM device at address {address}")
                try:
                    await connect_and_subscribe(address)
                except Exception as e:
                    print(f"Error while connecting to HRM device at address {address}: {e}")


@app.route("/heart_rate", methods=["GET"])
def get_heart_rate():
    global heart_rate_data
    if len(heart_rate_data) > 0:
        timestamp, heart_rate, _ = heart_rate_data[-1]
        return jsonify({"Timestamp": timestamp, "Heart_rate": heart_rate})
    else:
        return jsonify({"error": "No heart rate data available"}), 404


def run_flask_app():
    app.run(host="0.0.0.0", port=5000)

def main():
    # Start the Flask app on a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    with open(csv_file, "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Heart_rate", "RR intervals"])

    # Start the BLE scanning and connecting process
    asyncio.run(scan_and_connect())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(scan_and_connect())
    except KeyboardInterrupt:
        print("Closing the connection...")
    finally:
        loop.close()

if __name__ == "__main__":
    main()
