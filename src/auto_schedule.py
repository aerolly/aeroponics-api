# Auto-scheduling script, sends commands to pi based on data in db
import concurrent.futures
import redis
import os
import sys
import traceback
import simplejson as json
import datetime
import time

import utility.datetime as dtu
import utility.postgres_client as ps

from utility.redis_client import r, p

def handleSchedulerJob(deviceID):
    schedulerInfo = ps.getResultSetFromDBNoJS('"Device".view_schedulerinfo_single', [deviceID])

    if schedulerInfo[0]['SchedulerTimeUntilStart'] > 0:
        time.sleep(schedulerInfo[0]['SchedulerTimeUntilStart'] * 60)

    # Query handles time info, run until stop time (query returns nothing)
    while schedulerInfo:
        # for jobs that rely on a sensor's value
        if schedulerInfo[0]['SchedulerSecondsToKeepActive'] is None:
            curSensorInfo = ps.getResultSetFromDBNoJS('"Device".view_mostrecentsensordata', [schedulerInfo[0]['SchedulerSensorToCheckID']])
            if curSensorInfo[0]['SensorReading'] <= schedulerInfo[0]['SchedulerSensorActivationValue']:
                r.publish('scheduler', json.dumps({
                'command': schedulerInfo[0]['DeviceType'],
                'options': {
                    'key': schedulerInfo[0]['RedisKey'],
                    'action': 1,
                }
                }))

                # wait until sensor meets turn off condition
                count = 0
                while curSensorInfo[0]['SensorReading'] <= schedulerInfo[0]['SchedulerSensorDeactivateValue']:
                    time.sleep(5)
                    curSensorInfo = ps.getResultSetFromDBNoJS('"Device".view_mostrecentsensordata', [schedulerInfo[0]['SchedulerSensorToCheckID']])
                    count += 1
                    if(count >= 5): # In case of errors, don't run for longer than 20 seconds
                        break

                r.publish('scheduler', json.dumps({
                'command': schedulerInfo[0]['DeviceType'],
                'options': {
                    'key': schedulerInfo[0]['RedisKey'],
                    'action': 0,
                }
                }))
            else:
                time.sleep(20)

        # for jobs that rely on a timer
        else:
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

        # Refresh scheduler info
        schedulerInfo = ps.getResultSetFromDBNoJS('"Device".view_schedulerinfo_single', [deviceID])

        # sleep if not auto mode
        autoMode = r.get('autoMode').decode('utf-8')
        if autoMode == '0':
            while not autoMode:
                time.sleep(1)
                autoMode = r.get('autoMode').decode('utf-8')
        


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

        time.sleep(5)

        # sleep until 4:00 AM
        # print(f"at: {datetime.datetime.now()}")
        # print(f"sleeping for: {dtu.secondsBeforeTime(4)} seconds")
        # time.sleep(dtu.secondsBeforeTime(4))

    except KeyboardInterrupt:
        print('Keyboard Interrupt... Shutting down.')
        ps.closeDB()
        sys.exit(0)
    except Exception:
        traceback.print_exc(file=sys.stdout)



                
