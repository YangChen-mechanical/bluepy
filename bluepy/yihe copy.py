import time

import bluepy.btle
import bluepy.sensortag

def connect():
    tags = []
    # addresses = ['54:6c:0e:52:ef:c7', '54:6c:0e:43:ee:07']
    addresses = ['54:6C:0E:52:F3:19']
    while addresses:
        for addr in addresses:
            try:
                tags.append(bluepy.sensortag.SensorTag(addr))
                print('yes')
                addresses.remove(addr)
            except bluepy.btle.BTLEException:
                time.sleep(5)
                continue
    return tags


def re_connect(tag_addr):
    print('re_connect')
    try:
        tag = bluepy.sensortag.SensorTag(tag_addr)
    except:
        
        time.sleep(5)
        return re_connect(tag_addr)
    return tag


# addresses = ['54:6c:0e:52:ef:c7', '54:6c:0e:43:ee:07']
# addresses = ['54:6C:0E:52:F3:19']
addresses = ['54:6C:0E:53:37:0A']

tags = connect()
for tag in tags:
    tag.IRtemperature.enable()
    tag.humidity.enable()
    tag.barometer.enable()
    tag.battery.enable()
    tag.lightmeter.enable()

    # Some sensors (e.g., temperature, accelerometer) need some time for initialization.
    # Not waiting here after enabling a sensor, the first read value might be empty or incorrect.
    time.sleep(1.0)

while True:
    for i in range(len(tags)):
        tag = tags[i]
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
            tags[i] = re_connect(addresses[i])
            break
        # if data['humidity'] >= 99.99 or data['temperature'] <= -10 or data['temperature'] >= 40:
        #     print(data)
        #     continue

        print(f"homeassistant/sensor{i + 1}")
        print(data)
    time.sleep(6)