import asyncio
from bleak import BleakScanner
import threading
# import bluepy.btle
# import bluepy.sensortag
import time
from bluepy import btle
from bluepy import sensortag

def handle_conn(addr):
    tag = 0
    try:

        print(addr)
        tag = sensortag.SensorTag(addr)
    except btle.BTLEException:
        return
    
    tag.IRtemperature.enable()
    tag.humidity.enable()
    tag.barometer.enable()
    tag.battery.enable()
    tag.lightmeter.enable()
    while True:
        data = {}
        try:
            # data['temperature'] = tag.humidity.read()[0]  # set ambient temperature to d1
            data['humidity'] = tag.humidity.read() # set humidity to d2
            # data['barometer'] = tag.barometer.read()[1]  # set barometer to d3
            # data['light'] = tag.lightmeter.read()  # set light to d5
            data['battery'] = tag.battery.read()  # set battery level to d4
        except:
            print('except')
            time.sleep(5)
            tag.disconnect()

            break

        print(addr, data)

        

async def run_bleak_scan():
    threads = []
    while True:  
        print("Scanning for BLE devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name == 'CC2650 SensorTag':
                print(f"Device found: {device.name}, MAC Address: {device.address}")
                thread = threading.Thread(target=handle_conn, args=(device.address,))
                threads.append(thread)
                thread.start()

            await asyncio.sleep(1)  

if __name__ == "__main__":
    asyncio.run(run_bleak_scan())

    while 1:
        time.sleep()
        

