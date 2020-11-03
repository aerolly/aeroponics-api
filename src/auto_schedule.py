# Auto-scheduling script, sends commands to pi based on data in db
import psql_utility as ps
import concurrent.futures
import datetime_utility as dtu
import redis
import os
import sys
import traceback
import simplejson as json
import datetime
import time


# Redis
r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)


def handleSchedulerJob(deviceID):
    schedulerInfo = ps.getResultSetFromDBNoJS('"Device".view_schedulerinfo_single', [deviceID])

    if schedulerInfo[0]['SchedulerTimeUntilStart'] > 0:
        time.sleep(schedulerInfo[0]['SchedulerTimeUntilStart'] * 60)

    # Query handles time info, run until stop time (query returns nothing)
    while schedulerInfo:
        autoMode = r.get('autoMode').decode('utf-8')
        if autoMode == '0':
            while not autoMode:
                time.sleep(1)
                autoMode = r.get('autoMode').decode('utf-8')

        print(f"at: {datetime.datetime.now()}")
        print("executing the following:\n" +json.dumps(schedulerInfo,indent=2))
        r.publish('scheduler', json.dumps({
        'command': schedulerInfo[0]['DeviceType'],
        'options': {
            'key': schedulerInfo[0]['RedisKey'],
            'action': 1,
            'waitTime': schedulerInfo[0]['SchedulerSecondsToKeepActive']
        }
        }))
        time.sleep(schedulerInfo[0]['SchedulerSecondsBetweenActivation'])


while True:
    try:
        # Check if scheduling is set to auto
        autoMode = r.get('autoMode').decode('utf-8')
        if autoMode == '0':
            while not autoMode:
                time.sleep(1)
                autoMode = r.get('autoMode').decode('utf-8')

        # Get current scheduling jobs from SQL server
        jobs = ps.getResultSetFromDBNoJS('"Device".view_schedulerinfo',[])
        print(jobs)

        # Separate each row into a separate thread
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for j in jobs:
                executor.submit(handleSchedulerJob, j['SchedulerDeviceID'])

        # sleep until 4:00 AM
        print(f"at: {datetime.datetime.now()}")
        print(f"sleeping for: {dtu.secondsBeforeTime(4)} seconds")
        time.sleep(dtu.secondsBeforeTime(4))

    except KeyboardInterrupt:
        print('Keyboard Interrupt... Shutting down.')
        ps.closeDB()
        sys.exit(0)
    except Exception:
        traceback.print_exc(file=sys.stdout)



                
