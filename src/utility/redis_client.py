import redis
import os

import settings

# Connect to redis server
r = redis.Redis(host=os.getenv('REDIS_IP'), port=os.getenv('REDIS_PORT'), db=0)

# Create redis pubsub object
p = r.pubsub(ignore_subscribe_messages=True)
