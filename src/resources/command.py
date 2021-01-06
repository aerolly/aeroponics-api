from flask_restful import Resource
from utility.redis_client import r

class Command(Resource):
  # Send a command to be scheduled
  def post(self):
    r.publish('scheduler', request.data)
    return 200
