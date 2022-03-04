import os
import paho.mqtt.client as mqtt
from .logger import logger
import requests
from dotenv import load_dotenv

load_dotenv()


client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    client.subscribe("garage/+")


def on_message(client, userdata, msg):
    logger.info("making request to garage")
    requests.get('http://192.168.1.243/s/p')

def start():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    logger.info("MQTT is running")

    client.loop_forever()

if __name__ == '__main__':
    start()
