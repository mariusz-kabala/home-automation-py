from influxdb import InfluxDBClient
import os
from sensedashboard.sense import sense
from sensedashboard.helpers import set_interval
import json


class Sensors:
    def __init__(self, mqtt):
        self.influx = InfluxDBClient(os.environ['STATS_DB_HOST'], int(os.environ['STATS_DB_PORT']), os.environ['STATS_DB_USER'],
                                     os.environ['STATS_DB_PASS'], os.environ['STATS_DB_DB'])

        self.client = mqtt

        self.interval = set_interval(lambda: self.read_sensors(), 3)

    def save_in_db(self, pressure: int, humidity: int, temp: int):
        json_body = [
            {
                "measurement": "sense_hat",
                "fields": {
                    "hat_pressure": pressure,
                    "hat_humidity": humidity,
                    "hat_temp": temp
                }
            }
        ]

        self.influx.write_points(json_body)

    def publish_in_mqtt(self, pressure: int, humidity: int, temp: int):
        self.client.publish("home/sensors/senseHat", json.dumps({
            "pressure": pressure,
            "humidity": humidity,
            "temp": temp
        }), qos=0, retain=True)

    def read_sensors(self):
        temp = round(sense.get_temperature(), 2)
        pressure = round(sense.get_pressure(), 2)
        humidity = round(sense.get_humidity(), 2)

        self.save_in_db(pressure, humidity, temp)
        self.publish_in_mqtt(pressure, humidity, temp)
