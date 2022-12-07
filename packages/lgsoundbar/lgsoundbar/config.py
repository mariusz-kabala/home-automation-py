import os
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_TOPIC = 'home/livingroom/soundbar'
DEVICE_IP = os.environ['DEVICE_IP']
HTTP_PORT = int(os.environ.get('HTTP_PORT', 8888))
URL_PREFIX = os.environ['URL_PREFIX']
CONSUL_HOST = os.environ['CONSUL_HOST']
CONSUL_PORT = os.environ['CONSUL_PORT']
