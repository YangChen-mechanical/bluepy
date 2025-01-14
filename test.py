# import time

# import bluepy.btle
# import bluepy.sensortag


# import asyncio
# from bleak import BleakScanner

# async def run_bleak_scan():
#     print("Scanning for BLE devices...")
#     devices = await BleakScanner.discover()
#     for device in devices:
#         if device.details['props']['Alias'] == 'CC2650 SensorTag':
#             print(f"Device found: {device.name}, MAC Address: {device.address}")
#             # print(device.details)


# asyncio.run(run_bleak_scan())

# tag = bluepy.sensortag.SensorTag('54:6C:0E:52:F3:19')

# tag.IRtemperature.enable()
# tag.humidity.enable()
# tag.barometer.enable()
# tag.battery.enable()
# tag.lightmeter.enable()

# # Some sensors (e.g., temperature, accelerometer) need some time for initialization.
# # Not waiting here after enabling a sensor, the first read value might be empty or incorrect.
# time.sleep(1.0)

# while True:


#     data = {}
#     try:
#         # data['temperature'] = tag.humidity.read()[0]  # set ambient temperature to d1
#         data['humidity'] = tag.humidity.read() # set humidity to d2
#         # data['barometer'] = tag.barometer.read()[1]  # set barometer to d3
#         # data['light'] = tag.lightmeter.read()  # set light to d5
#         data['battery'] = tag.battery.read()  # set battery level to d4
#     except:
#         print('except')
#         time.sleep(5)
#         tag.disconnect()

#         break



#     print(data)
# time.sleep(6)



import time
import bluepy.sensortag
        
tag = bluepy.sensortag.SensorTag('54:6C:0E:52:F3:19')

time.sleep(1.0)
tag.IRtemperature.enable()
for i in range(5):
    tag.waitForNotifications(1.0)
    print(tag.IRtemperature.read())
tag.disconnect()