import psql_utility as ps
import os
import datetime_utility as dtu

atest = ps.getResultSetFromDB('"Device".view_schedulerinfo_single', [3])
print(atest)

atest = ps.getResultSetFromDBNoJS('"Device".view_mostrecentsensordata', [6])
print(atest)

ps.closeDB()
