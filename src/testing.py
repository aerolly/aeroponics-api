import psql_utility as ps
import os
import datetime_utility as dtu

atest = ps.getResultSetFromDB('"Device".view_availablesensors', [])
print(atest)

ps.closeDB()
