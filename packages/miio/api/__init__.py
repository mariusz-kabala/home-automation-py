from flask import Flask
from api.mod_groups.controller import mod_groups
from api.mod_lights.controller import mod_lights

app = Flask(__name__)

app.register_blueprint(mod_groups)
app.register_blueprint(mod_lights)