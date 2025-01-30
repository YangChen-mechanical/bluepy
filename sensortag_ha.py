import asyncio
from bleak import BleakScanner
import threading
import time
import bluepy.btle
import bluepy.sensortag
import json
import paho.mqtt.client as mqtt

# sudo systemctl restart bluetooth

# MQTT Configuration
HA_BROKER = "azure.nocolor.pw"       # Replace with your Home Assistant MQTT broker address
HA_PORT = 1883                       # Default MQTT port
HA_USERNAME = "feiyue"                # Replace with your MQTT username
HA_PASSWORD = "123456789"             # Replace with your MQTT password

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(HA_USERNAME, HA_PASSWORD)
mqtt_client.connect(HA_BROKER, HA_PORT, 60)
mqtt_client.loop_start()

def publish_discovery(unique_id, state_topic):
    """Publish MQTT discovery message for a temperature sensor."""
    discovery_topic = f"homeassistant/sensor/sensortag_{unique_id}_temperature/config"
    temp_config = {
        "name": f"SensorTag {unique_id} Temperature",
        "state_topic": state_topic,
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value }}"
    }
    mqtt_client.publish(discovery_topic, json.dumps(temp_config), retain=True)
    print(f"[DISCOVERY] Published discovery for SensorTag {unique_id} Temperature on {discovery_topic}")




def handle_conn(addr):

    tag = 0
    try:
        tag = bluepy.sensortag.SensorTag(addr)
    except bluepy.btle.BTLEException:
        print('no')
        return
    
    tag.humidity.enable()
    tag.battery.enable()
    tag.lightmeter.enable()
    time.sleep(2)
    while True:
        data = {}
        try:
            data['humidity'] = tag.humidity.read() # set humidity to d2
            data['battery'] = tag.battery.read()  # set battery level to d4
            data['light'] = tag.lightmeter.read()  # set light to d5
        except:
            print('except')
            time.sleep(1)
            tag.disconnect()

            break
        
        temperature_value = data['humidity'][0]
        b = data['battery']
        print(addr, data)
        if 15 < temperature_value < 40:
            unique_id = addr.replace(":", "").upper()
            state_topic = f"homeassistant/sensor/sensortag_{unique_id}_temperature/state"
            publish_discovery(unique_id, state_topic)
            mqtt_client.publish(state_topic, temperature_value, retain=True)
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
        

