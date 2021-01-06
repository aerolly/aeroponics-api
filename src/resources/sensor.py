import json
from flask_restful import Resource
import utility.postgres_client as ps

class Sensor(Resource):
  def get(self):
    return ps.getResultSetFromDB('"Device".view_availablesensors' , [])

  def post(self):
    data = json.loads(request.data.decode('utf-8'))
    return ps.modifyDB('"Device"."Insert_SensorReading"', [data['id'], data['reading']])
