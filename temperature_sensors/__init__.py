import os
from flask import Flask
from flask_restplus import Api

app = Flask(__name__)

# Get the senors and zip them to make a dict
sensor_names = os.environ.get('SENSOR_NAMES').split(',')
sensor_ids = os.environ.get('SENSOR_IDS').split(',')
TEMPERATURE_SENSOR_MAPPING = dict(zip(sensor_names, sensor_ids))

from .status import api as ns1

api = Api(app)
api.add_namespace(ns1)
import temperature_sensors.temp_sensors
