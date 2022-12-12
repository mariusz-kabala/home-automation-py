import os
from dotenv import load_dotenv

load_dotenv()

devices = dict(
    homeSrv="EC:B1:D7:71:BA:AE",
    aboveGarageTV="A8:23:FE:0E:C0:1B",
    livingRoomTV="B0:37:95:68:0B:03",
    homeNas="C8:CB:B8:C8:EA:31",
    lgSoundBar="F8:B9:5A:E0:01:96"
)

MQTT_HOST = os.environ['MQTT_HOST']
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
URL_PREFIX = os.environ['URL_PREFIX']
CONSUL_HOST = os.environ['CONSUL_HOST']
CONSUL_PORT = os.environ['CONSUL_PORT']
HTTP_PORT = int(os.environ.get('HTTP_PORT', 8888))
