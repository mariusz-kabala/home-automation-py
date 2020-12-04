from flask import Blueprint, request, abort
from config import groups, yeelights, philipsEyeCares
from miio.philips_eyecare import PhilipsEyecare
from miio.yeelight import Yeelight
from devices.yeelight.command import Command as YeelightCommand, MAPPER as YEELIGHT_MAPPER
from devices.philips_eyecare.command import Command as PhilipsEyeCareCommand, MAPPER as PHILIPS_EYECARE_MAPPER

mod_groups = Blueprint('groups', __name__, url_prefix='/groups')


def get_group_status(statuses, mapper):
    result = dict()

    for key in mapper.keys():
        value_type = mapper.get(key)

        for status in statuses:
            if status is None or key not in status:
                continue
            elif value_type is bool:
                if key not in result or result[key] is False:
                    result[key] = status[key]
            elif value_type is int:
                if key not in result or (type(status[key]) is int
                                         and type(result[key]) is int
                                         and status[key] > result[key]):
                    result[key] = status[key]

    return result


def get_yeelight_status(deviceName: str):
    device = yeelights.get(deviceName)
    yeelight = Yeelight(ip=device.get('ipAddress'), token=device.get('token'))
    command = YeelightCommand(light=yeelight, deviceName=deviceName)

    return command.get_status()


def get_philips_eye_care_status(deviceName: str):
    device = philipsEyeCares.get(deviceName)
    philips = PhilipsEyecare(ip=device.get('ipAddress'),
                             token=device.get('token'))
    command = PhilipsEyeCareCommand(device=philips, deviceName=deviceName)

    return command.get_status()


def get_devices_list(settings, devicesType):
    if devicesType in settings:
        return settings[devicesType]

    return tuple()


@mod_groups.route('/', methods=['GET'])
def groups_list():
    result = dict()

    for groupName, groupSettings in groups.items():
        yeelights = get_devices_list(groupSettings, 'yeelights')
        philipsEyeCares = get_devices_list(groupSettings, 'philipsEyeCares')

        statuses = list(map(get_yeelight_status, yeelights)) + list(
            map(get_philips_eye_care_status, philipsEyeCares))
        status = get_group_status(statuses,
                                  YEELIGHT_MAPPER | PHILIPS_EYECARE_MAPPER)

        result[groupName] = {
            "status": status,
            "devices": yeelights + philipsEyeCares
        }

    return result


@mod_groups.route('/<group>', methods=['GET'])
def details(group):
    if group not in groups:
        return abort(404)

    groupSettings = groups.get(group)
    yeelights = get_devices_list(groupSettings, 'yeelights')
    philipsEyeCares = get_devices_list(groupSettings, 'philipsEyeCares')
    statuses = list(map(get_yeelight_status, yeelights)) + list(
        map(get_philips_eye_care_status, philipsEyeCares))
    status = get_group_status(statuses,
                              YEELIGHT_MAPPER | PHILIPS_EYECARE_MAPPER)

    result = {
        "status": status,
        "devices": yeelights + philipsEyeCares
    }

    return result
