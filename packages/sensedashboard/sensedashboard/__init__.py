import paho.mqtt.client as mqtt
import os
from .display import Display
from .sensors import Sensors
from .logger import logger
import json

client = mqtt.Client()
display = Display(client)
sensors = Sensors(client)

def on_connect(client, userdata, flags, rc):
    logger.info('Connected with result code %d', rc)

    client.subscribe("home/alert/+")
    client.subscribe("home/senseHat/showMsg")

def on_mqtt_connect(client, userdata, msg):
    if "home/alert" in msg.topic:
        display.show_alert()
        return

    if "home/senseHat/showMsg":
        payload = json.loads(str(msg.payload.decode("utf-8", "ignore")))
        display.show_msg(payload.message)

client.on_connect = on_connect

if __name__ == '__main__':
    client.on_connect = on_mqtt_connect

    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)
    
    client.loop_forever()
