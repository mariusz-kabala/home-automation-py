from flask import Blueprint, request, abort
from config import yeelights, philipsEyeCares, groups

mod_rooms = Blueprint('rooms', __name__, url_prefix='/rooms')

@mod_rooms.route('/', methods=['GET'])
def rooms_list():
    results = dict()

    all = yeelights.copy()
    all.update(philipsEyeCares)

    for deviceName, deviceSettings in all.items():
        room = deviceSettings.get('room')
        if room not in results:
            results[room] = {
                "devices": list(),
                "groups": list(),
            }

        devices = results[room].get("devices")

        if deviceName not in devices:
            devices.append(deviceName)

    for groupName, groupSettings in groups.items():
        room = groupSettings.get('room')
        if room not in results:
            results[room] = {
                "devices": list(),
                "groups": list(),
            }

        roomGroups = results[room].get('groups')

        if groupName not in roomGroups:
            roomGroups.append(groupName)

    return results
    
