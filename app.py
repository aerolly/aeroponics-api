from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
import redis
import os

load_dotenv()

r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)