from flask import Flask
from api.mod_groups.controller import mod_groups
from api.mod_lights.controller import mod_lights
from api.mod_rooms.controller import mod_rooms

app = Flask(__name__)

app.register_blueprint(mod_groups)
app.register_blueprint(mod_lights)
app.register_blueprint(mod_rooms)
