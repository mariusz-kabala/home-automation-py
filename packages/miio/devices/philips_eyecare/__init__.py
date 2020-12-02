from helpers.logger import logger
from config import philipsEyeCares
from .command import Command
from miio.philips_eyecare import PhilipsEyecare
import json

devices = dict()

for deviceName in philipsEyeCares:
    device = philipsEyeCares.get(deviceName)    
    devices[deviceName] = PhilipsEyecare(ip=device.get('ipAddress'), token=device.get('token'))


def handle_message(msg):
    logger.info('New message topic: %s, message: %s',
                msg.topic, str(msg.payload))

    splitted = msg.topic.split('/')
    deviceName = splitted[2]
    toExec = splitted[3]

    device = devices.get(deviceName)

    if device is None:
        logger.error(
            'Device %s is not supported, update config file', deviceName)
        return

    try:
        jsonMsg = json.loads(str(msg.payload.decode("utf-8", "ignore")))
    except:
        jsonMsg = {}

    command = Command(device=device, deviceName=deviceName)

    handlers = dict(
        turnOn=command.on,
        turnOff=command.off,
        getStatus=command.status,
        setBrightness=command.brightness,
        ambientOn=command.ambient_on,
        ambientOff=command.ambient_off,
        eyecareOn=command.eyecare_on,
        eyecareOff=command.eyecare_off,
        smartNightLightOn=command.smart_night_light_on,
        smartNightLightOff=command.smart_night_light_off,
    )

    commandToExec = handlers.get(toExec)

    if (commandToExec is None):
        logger.error('Not supported command %s for device %s',
                     toExec, deviceName)
        return

    commandToExec(jsonMsg)

    del command
