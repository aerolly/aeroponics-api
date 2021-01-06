import time
import redis

from utility.redis_client import r, p

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
