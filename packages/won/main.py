import os
from mqtt import client
from config import devices
import re
from wakeonlan import send_magic_packet
from logger import logger


def get_device_mac_address(device):
    print(device)
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", device.lower()):
        return device

    return devices.get(device)


def on_connect(client, userdata, flags, rc):
    client.subscribe("home/wot/+")


def on_message(client, userdata, msg):
    arr = str(msg.topic).split('/')

    device = get_device_mac_address(arr[2])

    if device is None:
        logger.error('Device %s not found, can not send magic packet', device)
        return

    send_magic_packet(device)
    logger.info('Magic packet to %s has been sent', device)



if __name__ == '__main__':
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    logger.info("Application is running")
    client.loop_forever()
