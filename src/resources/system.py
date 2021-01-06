from flask_restful import Resource
from utility.redis_client import r

# Utility function to parse number if possible
def parseNumber(number):
  try:
    return float(number)
  except ValueError as error:
    return number

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
