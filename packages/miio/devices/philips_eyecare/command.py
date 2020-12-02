from miio.philips_eyecare import PhilipsEyecare
from helpers.logger import logger
from string import Template
from mqtt import client
import json
from helpers.redis import save_hash, get_hash, rc
from typing import final
from helpers.ping import ping

POWER_STATUS: final = dict(off=False, on=True)

MAPPER: final = {
    'isOn': bool,
    'brightness': int,
    'ambient': bool,
    'eyecare': bool,
    'scene': int,
    'reminder': bool,
    'smartNightLight': bool,
    'delayOffCountdown': int,
}


class Command:
    def __init__(self, device: PhilipsEyecare, deviceName: str):
        self.device = device
        self.name = deviceName

    def get_redis_key(self):
        template = Template('miio-philips-eyecare-$name')
        return str(template.substitute(name=self.name))

    def on(self, msg):
        try:
            self.device.on()
        except:
            logger.error('Can not turn on device %s', self.name)
            return

        self.update_device_status(status={**self.get_status(), 'isOn': True})

    def off(self, msg):
        try:
            self.device.off()
        except:
            logger.error('Can not turn off device %s', self.name)
            return

        self.update_device_status(status={**self.get_status(), 'isOn': False})

    def ambient_off(self, msg):
        try:
            self.device.ambient_off()
        except:
            logger.error('Can not turn off ambient - device %s', self.name)
            return

        self.update_device_status(status={
            **self.get_status(), 'ambient': False
        })

    def ambient_on(self, msg):
        try:
            self.device.ambient_off()
        except:
            logger.error('Can not turn on ambient - device %s', self.name)
            return

        self.update_device_status(status={
            **self.get_status(), 'ambient': True
        })

    def eyecare_off(self, msg):
        try:
            self.device.ambient_off()
        except:
            logger.error('Can not turn off eyecare - device %s', self.name)
            return

        self.update_device_status(status={
            **self.get_status(), 'eyecare': False
        })

    def eyecare_on(self, msg):
        try:
            self.device.ambient_on()
        except:
            logger.error('Can not turn on eyecare - device %s', self.name)
            return

        self.update_device_status(status={
            **self.get_status(), 'isOn': True,
            'eyecare': True
        })

    def smart_night_light_on(self, msg):
        try:
            self.device.smart_night_light_on()
        except:
            logger.error('Can not turn on smart night light - device %s',
                         self.name)
            return

        self.update_device_status(status={
            **self.get_status(), 'smartNightLight': True
        })

    def smart_night_light_off(self, msg):
        try:
            self.device.smart_night_light_off()
        except:
            logger.error('Can not turn off smart night light - device %s',
                         self.name)
            return

        self.update_device_status(status={
            **self.get_status(), 'smartNightLight': False
        })

    def brightness(self, msg):
        level = msg.get('level')

        if type(level) is not int:
            logger.error('Invalid brightness level provided for device: %s',
                         self.name)
            return

        self.device.on()
        self.device.set_brightness(level)

        self.update_device_status(status={
            **self.get_status(), 'isOn': True,
            'brightness': level
        })

    def get_status_topic(self):
        template = Template('$prefix/philipsEyeCare/$device/status')
        return str(template.substitute(prefix='home', device=self.name))

    def get_status(self, refresh: bool = False):
        key = self.get_redis_key()

        if rc.exists(key) and refresh is not True:
            return get_hash(key, MAPPER)

        try:
            status = self.device.status()
        except:
            logger.error('Can get status of device %s', self.name)
            return

        return {
            'isOn': POWER_STATUS.get(status.power),
            'brightness': status.ambient_brightness,
            'ambient': status.ambient,
            'eyecare': status.eyecare,
            'scene': status.scene,
            'reminder': status.reminder,
            'smartNightLight': status.smart_night_light,
            'delayOffCountdown': status.delay_off_countdown,
        }

    def status(self, msg):
        status = self.get_status(refresh=True)

        if status is None:
            return

        save_hash(key=self.get_redis_key(), data=status)
        self.send_device_status(status=status)

    def send_device_status(self, status):
        client.publish(self.get_status_topic(), json.dumps(status))

    def update_device_status(self, status):
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

    def check_reachability(self):
        key = self.get_redis_key()

        if rc.exists(key):
            save_hash(key=key, data={"reachable": ping(host=self.device.ip)})
