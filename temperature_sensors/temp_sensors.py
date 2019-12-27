import datetime

from pi_funcs.funcs import get_ds18b20_sensor
from flask_restplus import Resource, fields

from . import api, TEMPERATURE_SENSOR_MAPPING

# TODO: TEST CODE
# def get_ds18b20_sensor(sensor_name):
#     return 1000
# TODO: END TEST CODE


TempModel = api.model('TempModel',
                      {'sensor_name': fields.String(),
                       'raw_value': fields.String(),
                       # 'service_description': fields.String(),
                       # 'plugin_output': fields.String(),
                       # 'return_code': fields.String(),
                       # 'status_time': fields.String(),
                       'status_time_utc': fields.String(),
                       # 'hostname': fields.String(default='NO_HOSTNAME'),
                       # 'message': fields.String(allow_null=True)
                       })

TempResponseModel = api.model('TempResponseModel',
                              {
                                'data': fields.List(fields.Nested(TempModel))
                              })

# TODO: remove param after updating
@api.route('/temperature/<sensor_name>')
class TemperaturesResource(Resource):
    @api.marshal_with(TempResponseModel)
    def get(self, sensor_name):
        response = []

        for one_sensor, sensor_id in TEMPERATURE_SENSOR_MAPPING.items():
            one_response = dict(status_time_utc=datetime.datetime.utcnow().isoformat(),
                                sensor_name=one_sensor,
                                service_description="{} Temperature".format(one_sensor.capitalize()),
                                status_time=datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
                                hostname='UNUSED_FIELD',
                                error=0
                                )
            try:
                sensor_temp = get_ds18b20_sensor(sensor_id)
            except:
                sensor_temp = "ERROR OCCURRED FOR {}".format(one_sensor)
                one_response['error'] = 2  # Critical status

            one_response['raw_value'] = sensor_temp
            one_response['plugin_output'] = "{0} Temperature: {1}F".format(one_sensor.capitalize(), sensor_temp)
            one_response['return_code'] = one_response['error']

            response.append(one_response)

        return {'data': response}
