from helpers.logger import logger
from mqtt import client
from string import Template
import json


class Command:
    def __init__(self, light, deviceName):
        self.light = light
        self.name = deviceName

    def get_status_topic(self):
        template = Template('$prefix/yeelight/$device/status')
        return str(template.substitute(prefix='home', device=self.name))

    def on(self, msg):
        try:
            self.light.on(transition=2)
        except:
            logger.error('Can not turn on device %s', self.name)
            return

        client.publish(self.get_status_topic(), json.dumps({'isOn': True}))
        self.status(msg=None)

    def off(self, msg):
        try:
            self.light.off()
        except:
            logger.error('Can not turn off device %s', self.name)
            return

        client.publish(self.get_status_topic(), json.dumps({'isOn': False}))
        self.status(msg=None)

    def status(self, msg):
        try:
            status = self.light.status()
        except:
            logger.error('Can get status of device %s', self.name)
            return

        client.publish(self.get_status_topic(), json.dumps({
            'isOn': status.is_on,
            'brightness': status.brightness,
            'colorTemp': status.color_temp,
            'rgb': status.rgb,
            'hsv': status.hsv,
            'dev': status.developer_mode,
            'saveState': status.save_state_on_change,
        }))

    def brightness(self, msg):
        level = msg.get('level')

        if type(level) is not int:
            logger.error(
                'Invalid brightness level provided for light: %s', self.name)
            return

        self.light.on()
        self.light.set_brightness(level, 5)

        client.publish(self.get_status_topic(), json.dumps(
            {'isOn': True, 'brightness': level}))
        self.status(msg=None)
