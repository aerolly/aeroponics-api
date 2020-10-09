import datetime as dt

def secondsBeforeTime(targetHour, targetMinute=0):
    hours = dt.datetime.now().hour
    mins = dt.datetime.now().minute
    secs = dt.datetime.now().second

    # If time given is less than current time, process as time tomorrow
    if hours > targetHour or (hours == targetHour and mins > targetMinute):  
        return (24 - hours + targetHour) * 3600 + (targetMinute - mins) * 60 + (-1*secs)
    else:
        return (targetHour - hours) * 3600 + (targetMinute - mins) * 60 + (-1*secs)

