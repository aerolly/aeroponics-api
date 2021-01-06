import redis
import os
import threading
import simplejson as json
import time
import sys
import traceback
import sentry_sdk

import settings

from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration

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

from processes.redis_pubsub import handleRedisData
from processes.connection_check import handleConnectionCheck

if __name__ == '__main__':
  sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration(), RedisIntegration()],
    traces_sample_rate=1.0
  )

  # Define flask server
  app = Flask(__name__)

  # Define rest api server
  api = Api(app)

  # Allow cross origin communication
  CORS(app, resources={r"/*": {"origins": "*"}})

  # Define socket io server
  socketio = SocketIO(app, cors_allowed_origins='*')

  # Server to client communication endpoint
  @socketio.on('')
  def send_data(data):
    socketio.emit('data', json.loads(data))

  # Define URL extension for each endpoint definition
  api.add_resource(Sensor, '/sensor')
  api.add_resource(Controller, '/controller')
  api.add_resource(Command, '/command')
  api.add_resource(System, '/system')

  try:
    redisData = threading.Thread(target=handleRedisData)
    rpiConnStatus = threading.Thread(target=handleConnectionCheck)

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
