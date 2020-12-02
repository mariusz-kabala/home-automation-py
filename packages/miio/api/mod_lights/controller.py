from flask import Blueprint, request, abort
from config import yeelights, philipsEyeCares
from miio.philips_eyecare import PhilipsEyecare
from miio.yeelight import Yeelight
from devices.yeelight.command import Command as YeelightCommand, MAPPER as YEELIGHT_MAPPER
from devices.philips_eyecare.command import Command as PhilipsEyeCareCommand, MAPPER as PHILIPS_EYECARE_MAPPER

mod_lights = Blueprint('lights', __name__, url_prefix='/lights')


@mod_lights.route('/', methods=['GET'])
def lights_list():
    result = dict()

    for lightName, lightSettings in yeelights.items():
        yeelight = Yeelight(ip=lightSettings.get('ipAddress'),
                            token=lightSettings.get('token'))
        command = YeelightCommand(light=yeelight, deviceName=lightName)

        result[lightName] = {"status": command.get_status()}

    for deviceName, deviceSettings in philipsEyeCares.items():
        device = PhilipsEyecare(ip=deviceSettings.get('ipAddress'),
                             token=deviceSettings.get('token'))
        command = PhilipsEyeCareCommand(device=device, deviceName=deviceName)

        result[deviceName] = {"status": command.get_status()}

    return result


@mod_lights.route('/<deviceName>', methods=['GET'])
def details(deviceName):
    if deviceName in yeelights:
        settings = yeelights.get(deviceName)
        yeelight = Yeelight(ip=settings.get('ipAddress'),
                            token=settings.get('token'))
        command = YeelightCommand(light=yeelight, deviceName=deviceName)

        return {"status": command.get_status()}

    if deviceName in philipsEyeCares:
        settings = philipsEyeCares.get(deviceName)
        philips = PhilipsEyecare(ip=settings.get('ipAddress'),
                                 token=settings.get('token'))
        command = PhilipsEyeCareCommand(device=philips, deviceName=deviceName)

        return {"status": command.get_status()}

    return abort(404)
