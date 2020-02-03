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
    client.subscribe("home/senseHat/displayOn")
    client.subscribe("home/senseHat/displayOff")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.error('Disconnected from MQTT')


def on_message(client, userdata, msg):
    logger.info("New MQTT message. Topic: %s, payload: %s",
                msg.topic, str(msg.payload.decode("utf-8", "ignore")))

    if "home/alert" in msg.topic:
        display.show_alert()
        return

    if "home/senseHat/displayOn" in msg.topic:
        display.on()
        return

    if "home/senseHat/displayOff" in msg.topic:
        display.off()
        return

    if "home/senseHat/showMsg" in msg.topic:
        try:
            payload = json.loads(str(msg.payload.decode("utf-8", "ignore")))
        except:
            logger.error("Invalid payload in showMsg command")
            return

        logger.info("Showing custom message %s", payload.get("message"))
        display.show_msg(payload.get("message"))
        return


client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect


def start():
    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    logger.info('Application started')

    client.loop_forever()


if __name__ == '__main__':
    start()
