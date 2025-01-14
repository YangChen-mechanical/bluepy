import asyncio
import bluepy.sensortag
import time

import asyncio
from bleak import BleakScanner
import threading
import time
import bluepy.btle
import bluepy.sensortag

async def handle_conn(addr):
    try:
        print(f"Attempting to connect to SensorTag at {addr}...")
        tag = bluepy.sensortag.SensorTag(addr)
    except bluepy.btle.BTLEException as e:
        print(f"Failed to connect to {addr}: {e}")
        return

    try:
        # Enable desired sensors
        print("Enabling sensors...")
        tag.humidity.enable()
        tag.battery.enable()
        await asyncio.sleep(1)  # Give sensors time to initialize

        while True:
            try:
                # Read sensor data
                data = {
                    "humidity": tag.humidity.read(),
                    "battery": tag.battery.read(),
                }
                print(f"Data from {addr}: {data}")
                await asyncio.sleep(2)  # Adjust polling frequency as needed
            except bluepy.btle.BTLEException as e:
                print(f"Error reading data from {addr}: {e}")
                break
    except Exception as e:
        print(f"Unexpected error with {addr}: {e}")
    finally:
        print(f"Disconnecting from {addr}...")
        try:
            tag.disconnect()
        except Exception as e:
            print(f"Error during disconnect: {e}")
        print(f"Disconnected from {addr}")

async def run_bleak_scan():
    while True:  
        print("Scanning for BLE devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name == 'CC2650 SensorTag':
                print(f"Device found: {device.name}, MAC Address: {device.address}")
                asyncio.create_task(handle_conn(device.address))
        await asyncio.sleep(5)  # 每次扫描后等待5秒，避免频繁扫描
                

if __name__ == "__main__":
    asyncio.run(run_bleak_scan())                     

    while 1:
        time.sleep(60)
        

