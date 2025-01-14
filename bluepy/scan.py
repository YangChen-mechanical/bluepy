import asyncio
from bleak import BleakScanner

async def run_bleak_scan():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        if device.details['props']['Alias'] == 'CC2650 SensorTag':
            print(f"Device found: {device.name}, MAC Address: {device.address}")
            # print(device.details)

if __name__ == "__main__":
    asyncio.run(run_bleak_scan())
