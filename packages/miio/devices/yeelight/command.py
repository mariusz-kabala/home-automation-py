from helpers.logger import logger
from mqtt import client
from string import Template
import json
from helpers.redis import save_hash, get_hash, rc
from typing import final
from helpers.ping import ping

MAPPER: final = {
    'isOn': bool,
    'brightness': int,
    'colorTemp': int,
    'rgb': int,
    'hsv': int,
    'dev': bool,
    'saveState': bool,
}


class Command:
    def __init__(self, light, deviceName):
        self.light = light
        self.name = deviceName

    def get_redis_key(self):
        template = Template('miio-yeelight-$name')
        return str(template.substitute(name=self.name))

    def get_status_topic(self):
        template = Template('$prefix/yeelight/$device/status')
        return str(template.substitute(prefix='home', device=self.name))

    def on(self, msg):
        try:
            self.light.on(transition=2)
        except:
            logger.error('Can not turn on device %s', self.name)
            return

        self.update_device_status(status={**self.get_status(), 'isOn': True})

    def off(self, msg):
        try:
            self.light.off()
        except:
            logger.error('Can not turn off device %s', self.name)
            return

        self.update_device_status(status={**self.get_status(), 'isOn': False})

    def brightness(self, msg):
        level = msg.get('level')

        if type(level) is not int:
            logger.error('Invalid brightness level provided for light: %s',
                         self.name)
            return

        try:
            self.light.on()
            self.light.set_brightness(level, 5)
        except:
            logger.error('Can not change brightness, device - %s', self.name)
            return

        self.update_device_status(status={
            **self.get_status(), 'isOn': True,
            'brightness': level
        })

    def toggle(self, msg):
        try:
            self.light.toggle()
        except:
            logger.error('Can not toggle device %s', self.name)
            return

        self.update_device_status(status=self.get_status(refresh=True))

    def get_status(self, refresh: bool = False):
        key = self.get_redis_key()

        if rc.exists(key) and refresh is not True:
            return get_hash(key, MAPPER)

        try:
            status = self.light.status()
        except:
            logger.error('Can not get status of device %s', self.name)
            return

        return {
            'isOn': status.is_on,
            'brightness': status.brightness,
            'colorTemp': status.color_temp,
            'rgb': status.rgb,
            'hsv': status.hsv,
            'dev': status.developer_mode,
            'saveState': status.save_state_on_change,
        }

    def status(self, msg):
        status = self.get_status(refresh=True)

        if status is None:
            return

        save_hash(key=self.get_redis_key(), data=status)
        self.send_device_status(status=status)

    def refresh_status(self):
        key = self.get_redis_key()
        status = self.get_status(refresh=True)

        if status is None:
            return

        if rc.exists(key):
            old_status = get_hash(key, MAPPER)
            if status != old_status:
                self.send_device_status(status=status)

        save_hash(key=self.get_redis_key(), data=status)

    def send_device_status(self, status):
        client.publish(self.get_status_topic(), json.dumps(status))

    def update_device_status(self, status):
        save_hash(key=self.get_redis_key(), data=status)
        self.send_device_status(status=status)

    def check_reachability(self):
        key = self.get_redis_key()

        if rc.exists(key):
            save_hash(key=key, data={"reachable": ping(host=self.light.ip)})
