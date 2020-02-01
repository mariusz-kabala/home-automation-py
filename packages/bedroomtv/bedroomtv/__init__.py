import paho.mqtt.client as mqtt
import os
from .logger import logger

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    logger.info('Connected with result code %d', rc)

    client.subscribe("home/tv/bedroom/turnOn")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.error('Disconnected from MQTT')


def on_message(client, userdata, msg):
    logger.info("Turning on bedroom tv")
    os.system(
        "tvservice --off && echo 'on 0' | cec-client -s -d 1 && tvservice --preferred")


client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect


def start():
    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    logger.info('Application started')

    client.loop_forever()


if __name__ == '__main__':
    start()
