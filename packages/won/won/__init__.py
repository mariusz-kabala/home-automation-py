import paho.mqtt.client as mqtt
from .config import devices, MQTT_HOST, MQTT_PORT, URL_PREFIX, HTTP_PORT
import re
from wakeonlan import send_magic_packet
from .logger import logger
from .consul import register_in_consul
from flask import Flask
from datetime import datetime

client = mqtt.Client()
startTime = datetime.now()
app = Flask(__name__)

def get_device_mac_address(device):
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



@app.route('/{}/turn_on/<name>'.format(URL_PREFIX), methods=['GET',])
def turn_on_device(name):
    device = get_device_mac_address(name)

    if device is None:
        return ('', 404)

    send_magic_packet(device)

    return ('', 200)

@app.route('/{}/health'.format(URL_PREFIX), methods=['GET',])
def health_check():
    return ({
        "status": True,
        "startedAt": startTime.strftime("%d/%m/%Y %H:%M:%S")
    }, 200)

def start():
    client.on_connect = on_connect
    client.on_message = on_message

    register_in_consul()

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    logger.info("MQTT is running")

    client.loop_start()

    app.run(debug=False, use_reloader=False, port=HTTP_PORT, host='0.0.0.0')


if __name__ == '__main__':
    start()    


    
