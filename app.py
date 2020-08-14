from dotenv import load_dotenv
from flask import Flask
import redis
import os

load_dotenv()

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
