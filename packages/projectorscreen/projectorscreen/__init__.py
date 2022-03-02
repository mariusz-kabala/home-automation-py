import os
from flask import Flask
import paho.mqtt.client as mqtt
from .logger import logger
from rpi_rf import RFDevice

client = mqtt.Client()
app = Flask(__name__)

pulselength = 350

rfdevice = RFDevice(17)
rfdevice.enable_tx()

def on_connect(client, userdata, flags, rc):
    client.subscribe("projector-screen/+")


def on_message(client, userdata, msg):
    arr = str(msg.topic).split('/')

    if arr[1] == "up":
        move_screen_up()
    elif arr[1] == "down":
        move_screen_down()
    elif arr[1] == "stop":
        stop_screen()


def move_screen_up():
    rfdevice.tx_code(9703026, None, pulselength)
    rfdevice.cleanup()
    pass


def move_screen_down():
    rfdevice.tx_code(9703028, None, pulselength)
    rfdevice.cleanup()
    pass


def stop_screen():
    rfdevice.tx_code(9703032, None, pulselength)
    rfdevice.cleanup()
    pass

@app.route('/up', methods=['GET',])
def move_up_route():
    move_screen_up()

    return ('', 200)

@app.route('/down', methods=['GET',])
def move_down_route():
    move_screen_down()

    return ('', 200)

@app.route('/stop', methods=['GET',])
def stop_route():
    stop_screen()

    return ('', 200)


def start():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    logger.info("Projector screen manager is running")

    client.loop_start()

    app.run(debug=False, use_reloader=False, port=int(os.environ['HTTP_PORT']), host='0.0.0.0')

if __name__ == '__main__':
    start()
