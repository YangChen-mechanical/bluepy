import asyncio
from bleak import BleakScanner
import threading
import time
import bluepy.btle
import bluepy.sensortag
import json
import paho.mqtt.client as mqtt

# sudo systemctl restart bluetooth

def handle_conn(addr):
    BROKER = "industrial.api.ubidots.com"
    PORT = 1883
    TOPIC = "/v1.6/devices/chen-test-device/"+addr
    USERNAME = "BBUS-6vtrAbM2jQ0bJc1u7dZZHZSMOwXKhv"

    client = mqtt.Client()
    client.username_pw_set(USERNAME)
    tag = 0
    try:
        tag = bluepy.sensortag.SensorTag(addr)
    except bluepy.btle.BTLEException:
        print('no')
        return
    
    tag.humidity.enable()
    tag.battery.enable()
    time.sleep(2)
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
        
        h = data['humidity'][0]
        b = data['battery']
        print(addr, data)
        if 15 < h < 40:
            payload = {
                "value": h,
                "timestamp": int(time.time() * 1000),
                "context": {
                    "battery": b
                }
            }
            client.connect(BROKER, PORT)
            client.publish(TOPIC, json.dumps(payload), qos=1)
            time.sleep(300)
        

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
        

