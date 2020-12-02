import threading, time
from config import yeelights, philipsEyeCares
from miio.philips_eyecare import PhilipsEyecare
from miio.yeelight import Yeelight
from devices.yeelight.command import Command as YeelightCommand
from devices.philips_eyecare.command import Command as PhilipsEyeCareCommand
import os


class SetInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.setDaemon(True)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

device_commands = list()

for deviceName, deviceSettings in yeelights.items():
    yeelight = Yeelight(ip=deviceSettings.get('ipAddress'),
                        token=deviceSettings.get('token'))
    command = YeelightCommand(light=yeelight, deviceName=deviceName)
    command.refresh_status()
    device_commands.append(command)

for deviceName, deviceSettings in philipsEyeCares.items():
    philips = PhilipsEyecare(ip=deviceSettings.get('ipAddress'),
                                token=deviceSettings.get('token'))
    command = PhilipsEyeCareCommand(device=philips, deviceName=deviceName)
    command.refresh_status()
    device_commands.append(command)


def check_devices_status():
    for command in device_commands:
        command.refresh_status()

def check_device_reachability():
    for command in device_commands:
        command.check_reachability()


def start_checking():
    SetInterval(3, check_devices_status)
    SetInterval(1, check_device_reachability)