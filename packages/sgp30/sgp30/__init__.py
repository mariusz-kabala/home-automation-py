import time
import board
import busio
import adafruit_sgp30
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from helpers import set_interval
import json
import os
from logger import logger


i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

elapsed_sec = 0

influx = InfluxDBClient(os.environ['STATS_DB_HOST'], int(os.environ['STATS_DB_PORT']), os.environ['STATS_DB_USER'],
                        os.environ['STATS_DB_PASS'], os.environ['STATS_DB_DB'])

client = mqtt.Client()


def save_in_db():
    json_body = [
        {
            "measurement": "sgp30",
            "fields": {
                "eCO2": sgp30.eCO2,
                "TVOC": sgp30.TVOC,
            }
        }
    ]

    try:
        influx.write_points(json_body)
    except:
        logger.error('Can not write measurement into influxDB')


def publish_readings():
    client.publish("home/sensors/sgp30", json.dumps({
        "type": "sgp30",
        "state": {
            "eCO2": sgp30.eCO2,
            "TVOC": sgp30.TVOC,
        }
    }))


def publish_baselines():
    client.publish("home/sgp30/baseLines", json.dumps({
        "eCO2": sgp30.baseline_eCO2,
        "TVOC": sgp30.baseline_TVOC
    }), qos=0, retain=True)


def on_mqtt_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("home/sgp30/baseLines")


def on_mqtt_message(client, userdata, msg):
    msgJson = json.loads(str(msg.payload.decode("utf-8", "ignore")))

    logger.info('Applying baseline values eCO2: %d, TVOC: %d',
                msgJson.eCO2, msgJson.TVOC)

    sgp30.set_iaq_baseline(msgJson.eCO2, msgJson.TVOC)

    client.unsubscribe("home/sgp30/baseLines")


def read_sensor():
    global elapsed_sec
    save_in_db()
    publish_readings()
    elapsed_sec += 1
    if elapsed_sec > 10:
        elapsed_sec = 0
        publish_baselines()


def start():
    set_interval(read_sensor, 1)

    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message

    client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']), 60)

    client.loop_forever()
