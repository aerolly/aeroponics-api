from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import redis
import os
import threading
import simplejson as json
import psycopg2
import time
from psycopg2.extras import RealDictCursor

import settings


load_dotenv()



r = redis.Redis(host=os.getenv('REDIS_IP'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)


conn = psycopg2.connect(
         user = os.environ.get('SQL_USER'),
         password = os.environ.get('SQL_PASS'),
         host = os.environ.get('SQL_IP'),
         port = os.environ.get('SQL_PORT'),
         database = os.environ.get('SQL_DB'))


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('')
def send_data(data):
  socketio.emit('data', json.loads(data))

############################################################
# DB Query Functions
############################################################

# General DB View function
def getResultSetFromDB(funcName, params):
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.callproc(funcName, params)
        result = json.dumps(cursor.fetchall())
        cursor.close()
        return result


# Modify function
def modifyDB(funcName, params):
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc(funcName, params)
        result=json.dumps(cursor.fetchall())

    # Return status and error message
    return result

#############################################################

class Sensor(Resource):
  def get(self):
    return getResultSetFromDB('"Device".view_availablesensors' , [])

class Controller(Resource):
  def get(self):
    return getResultSetFromDB('"Device".view_availablecontrollers' , [])

class Command(Resource):
  def post(self):
    print(request.data)
    r.publish('scheduler', request.data)
    return 200

class System(Resource):
  def get(self):
    initialState = {}

    for key in r.scan_iter("*"):
      # delete the key
      value = r.get(key).decode('utf-8')

      try: 
        initialState[key.decode('utf-8')] = int(value)
      except ValueError:
        initialState[key.decode('utf-8')] = value

    return initialState
  def post(self):
    data = json.loads(request.data)
    r.set(data['key'], data['value'])

    try: 
      val = int(data['value'])
    except ValueError:
      val = data['value']

    send_data(json.dumps({
      'key': data['key'],
      'result': val
    }))
    return 200

api.add_resource(Sensor, '/sensor')
api.add_resource(Controller, '/controller')
api.add_resource(Command, '/command')
api.add_resource(System, '/system')

def handleRedisData():
  try:
    p.subscribe('data')
  except:
    print('Could not subscribe')

  while True:
    for message in p.listen():
      try:
        msg = message['data'].decode('utf-8')
        print('Received event.', msg)

        payload = json.loads(msg)

        r.set(payload.key, payload.result)

        send_data(msg)
      except UnicodeError:
        print('Error decoding Redis message')
    time.sleep(1)

if __name__ == '__main__':
    redisData = threading.Thread(target=handleRedisData)

    redisData.start()

    socketio.run(app, host='0.0.0.0', debug=True)

    redisData.join()
