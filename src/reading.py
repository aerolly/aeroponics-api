import redis
import os
import simplejson as json
import time

import settings

r = redis.Redis(host=os.getenv('REDIS_IP'), port=os.getenv('REDIS_PORT'), db=0)

temp = json.dumps({
  'command': 'sensor',
  'options': {
    'key': 'pressure',
  }
})

pressure = json.dumps({
  'command': 'sensor',
  'options': {
    'key': 'temperature',
  }
})

while True:
  print('SENDING')
  r.publish('scheduler', temp)
  r.publish('scheduler', pressure)
  time.sleep(10)
