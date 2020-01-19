from helpers.logger import logger
from config import lights
from devices.yeelight.command import Command
from miio.yeelight import Yeelight
import json

devices = dict()

for deviceName in lights:
    device = lights.get(deviceName)
    yeelight = Yeelight(ip=device.get('ipAddress'), token=device.get('token'))

    devices[deviceName] = yeelight


def handle_message(msg):
    logger.info('New message topic: %s, message: %s',
                msg.topic, str(msg.payload))

    splitted = msg.topic.split('/')
    deviceName = splitted[2]
    toExec = splitted[3]

    light = devices.get(deviceName)
    try:
        jsonMsg = json.loads(str(msg.payload.decode("utf-8", "ignore")))
    except:
        jsonMsg = {}

    if light is None:
        logger.error(
            'Device %s is not supported, update config file', deviceName)
        return

    command = Command(light=light, deviceName=deviceName)

    handlers = dict(
        turnOn=command.on,
        turnOff=command.off,
        getStatus=command.status,
        setBrightness=command.brightness,
    )

    commandToExec = handlers.get(toExec)

    if (commandToExec is None):
        logger.error('Not supported command %s for device %s',
                     commandToExec, deviceName)
        return

    commandToExec(jsonMsg)

    del command
