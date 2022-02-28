import os
from flask import Flask
import paho.mqtt.client as mqtt

client = mqtt.Client()
app = Flask(__name__)

def on_connect(client, userdata, flags, rc):
    client.subscribe("home/wot/+")


def on_message(client, userdata, msg):
    arr = str(msg.topic).split('/')


def move_screen_up():
    pass


def move_screen_down():
    pass


def stop_screen():
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
