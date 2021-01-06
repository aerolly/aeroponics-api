from flask_restful import Resource
import utility.postgres_client as ps

class Controller(Resource):
  def get(self):
    return ps.getResultSetFromDB('"Device".view_availablecontrollers' , [])
