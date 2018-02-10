from garden.extensions import api_manager, auth_func
from garden.models import User, Location, Sensor, SensorReading, MeasurementType
from flask_restless import ProcessingException

# This uses flask-restless to generate a REST API for these objects
api_manager.create_api(User, methods=['GET', 'PUT', 'POST', 'DELETE'], preprocessors={
    'GET_SINGLE': [auth_func],
    'GET_MANY': [auth_func],
    'DELETE_SINGLE': [auth_func],
    'DELETE_MANY': [auth_func],
    'PATCH_SINGLE': [auth_func],
    'PATCH_MANY': [auth_func],
    'POST': [auth_func]
})

api_manager.create_api(Location, methods=['GET', 'PUT', 'POST', 'DELETE'])

api_manager.create_api(Sensor, methods=['GET', 'PUT', 'POST', 'DELETE'])

api_manager.create_api(MeasurementType, methods=['GET', 'PUT', 'POST', 'DELETE'])

api_manager.create_api(SensorReading, methods=['GET', 'PUT', 'POST', 'DELETE'])

