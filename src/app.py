import redis
import os
import threading
import simplejson as json
import time
import sys
import traceback

import utility.postgres_client as ps
from utility.redis_client import r, p

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from resources.command import Command
from resources.controller import Controller
from resources.sensor import Sensor
from resources.system import System

import settings

if __name__ == '__main__':
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
