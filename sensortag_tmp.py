import asyncio
from bleak import BleakScanner
import threading
import time
import bluepy.btle
import bluepy.sensortag

# sudo systemctl restart bluetooth

def handle_conn(addr):
    tag = 0
    try:
        tag = bluepy.sensortag.SensorTag(addr)
    except bluepy.btle.BTLEException:
        print('no')
        return
    
    tag.humidity.enable()
    tag.battery.enable()
    while True:
        data = {}
        try:
            data['humidity'] = tag.humidity.read() # set humidity to d2
            data['battery'] = tag.battery.read()  # set battery level to d4
        except:
            print('except')
            time.sleep(1)
            tag.disconnect()

            break
        time.sleep(5)
        print(addr, data)

        

async def run_bleak_scan():
    while True:  
        print("Scanning for BLE devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name == 'CC2650 SensorTag':
                print(f"Device found: {device.name}, MAC Address: {device.address}")
                await asyncio.sleep(2)  
                thread = threading.Thread(target=handle_conn, args=(device.address,))
                thread.start()
        # time.sleep(5)
        await asyncio.sleep(5)  
                

if __name__ == "__main__":
    asyncio.run(run_bleak_scan())                     

    while 1:
        time.sleep(60)
        

