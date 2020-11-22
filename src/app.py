from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import redis
import os
import threading
import simplejson as json
import time
import sys
import traceback
import psql_utility as ps
import sendMail as sm

import settings




if __name__ == '__main__':
  # Connect to redis server
  r = redis.Redis(
    host=os.getenv('REDIS_IP'),
    port=os.getenv('REDIS_PORT'),
    db=0,
    socket_connect_timeout=3
    )

  # Create redis pubsub object
  p = r.pubsub(ignore_subscribe_messages=True)

  # Define flask server
  app = Flask(__name__)

  # Define rest api server
  api = Api(app)

  # Allow cross origin communication
  CORS(app, resources={r"/*": {"origins": "*"}})

  # Define socket io server
  socketio = SocketIO(app, cors_allowed_origins='*')

  # Send email if rpi not connectable
  def rpiConnectCheck():
    rpi_ip = os.getenv('RPI_IP')

    disconnectMsg = 'Subject: Unable To Connect To RPI\n\nHEEEEEEEEEEEEEEEEEEEEELP'
    reconnectMsg = 'Subject: Connection reestablished to RPI\n\n\nnvm'

    while True:
      try:
        response = os.system(f"ping -c 1 -t 2 {rpi_ip}")
        if response != 0:
          # two prevent duds, must be two missed packets in a row
          time.sleep(1)
          response = os.system(f"ping -c 1 -t 2 {rpi_ip}")
          if response != 0:
            sm.sendDevMail(disconnectMsg)
            while response != 0:
              time.sleep(10)
              response = os.system(f"ping -c 1 -t 2 {rpi_ip}")
            sm.sendDevMail(reconnectMsg)
        else:
          time.sleep(10)
      except:
        print('Something went wrong checking connection')

  # Server to client communication endpoint
  @socketio.on('')
  def send_data(data):
    socketio.emit('data', json.loads(data))


  # Utility function to parse number if possible
  def parseNumber(number):
    try:
      return float(number)
    except ValueError as error:
      return number


  # Endpoint definitions

  class Sensor(Resource):
    def get(self):
      return ps.getResultSetFromDB('"Device".view_availablesensors' , [])

    def post(self):
      data = json.loads(request.data.decode('utf-8'))
      return ps.modifyDB('"Device"."Insert_SensorReading"', [data['id'], data['reading']])


  class Controller(Resource):
    def get(self):
      return ps.getResultSetFromDB('"Device".view_availablecontrollers' , [])

  class Command(Resource):
    # Send a command to be scheduled
    def post(self):
      print(request.data)
      r.publish('scheduler', request.data)
      return 200

  class System(Resource):
    # Get value from the current system state
    def get(self):
      initialState = {}

      for key in r.scan_iter("*"):
        # delete the key
        value = r.get(key).decode('utf-8')

        initialState[key.decode('utf-8')] = parseNumber(value)

      return initialState

    # Set a value for the system state
    def post(self):
      data = json.loads(request.data)
      r.set(data['key'], data['value'])

      val = parseNumber(data['value'])

      send_data(json.dumps({
        'key': data['key'],
        'result': val
      }))
      return 200

  # Define URL extension for each endpoint definition
  api.add_resource(Sensor, '/sensor')
  api.add_resource(Controller, '/controller')
  api.add_resource(Command, '/command')
  api.add_resource(System, '/system')

  # Loop until redis data arrives
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

          r.set(payload['key'], payload['result'])
          r.set('time', payload['time'])

          send_data(msg)
        except UnicodeError:
          print('Error decoding Redis message')
        except redis.exceptions.TimeoutError:
          print('Redis connection timed out')
        except redis.exceptions.ConnectionError:
          print('Could not establish Redis connection')
      time.sleep(1)
  try:
    redisData = threading.Thread(target=handleRedisData)
    rpiConnStatus = threading.Thread(target=rpiConnectCheck)

    rpiConnStatus.start()
    redisData.start()

    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

    redisData.join()
    rpiConnStatus.join()
  except KeyboardInterrupt:
    print("Shutdown requested...exiting")
  except Exception:
    traceback.print_exc(file=sys.stdout)
  finally:
    ps.closeDB()
    sys.exit(0)
