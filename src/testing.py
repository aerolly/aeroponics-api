import psql_utility as ps
import os
import datetime_utility as dtu

print(dtu.secondsBeforeTime(4))
# atest = ps.getResultSetFromDB('"Device".view_schedulerinfo_single', [1])
# print(atest)

ps.closeDB()