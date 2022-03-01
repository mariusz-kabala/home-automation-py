import os
from flask import Flask
import paho.mqtt.client as mqtt
from rpi_rf import RFDevice

client = mqtt.Client()
app = Flask(__name__)

map = {
    'up': 9703026,
    'down': 9703028,
    'stop': 9703032
}
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
    rfdevice.tx_code(9703026, "default", pulselength)
    rfdevice.cleanup()
    pass


def move_screen_down():
    rfdevice.tx_code(9703028, "default", pulselength)
    rfdevice.cleanup()
    pass


def stop_screen():
    rfdevice.tx_code(9703032, "default", pulselength)
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
