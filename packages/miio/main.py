import os
from helpers.logger import logger
from devices import yeelight
from mqtt import client


handlers = dict(
    yeelight=yeelight.handle_message
)


def on_connect(client, userdata, flags, rc):
    client.subscribe("home/vacuum/#")
    client.subscribe('home/yeelight/#')


def on_message(client, userdata, msg):
    arr = str(msg.topic).split('/')

    handler = handlers.get(arr[1])
    handler(msg)


if __name__ == '__main__':
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    logger.info("Application is running")
    client.loop_forever()
