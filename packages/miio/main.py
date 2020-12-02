import os
from helpers.logger import logger
from devices import yeelight, philips_eyecare
from mqtt import client
from api import app
from checker import start_checking
import threading
import sys
import signal


handlers = dict(
    yeelight=yeelight.handle_message,
    philipsEyeCare=philips_eyecare.handle_message
)


def on_connect(client, userdata, flags, rc):
    client.subscribe("home/vacuum/#")
    client.subscribe('home/yeelight/#')
    client.subscribe('home/philipsEyeCare/#')

    logger.info("Connection to MQTT has been made")


def on_message(client, userdata, msg):
    arr = str(msg.topic).split('/')

    handler = handlers.get(arr[1])
    handler(msg)


def signal_handler(signal, frame):
    logger.info("Application has been killed")
    sys.exit(0)


if __name__ == '__main__':
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    # httpWorker = threading.Thread(target=app.run)
    # httpWorker.setDaemon(True)

    # signal.signal(signal.SIGINT, signal_handler)
    
    logger.info("Application is running")
    
    # httpWorker.start()
    # client.loop_forever()
    # start_checking()
    app.run(debug=True)
