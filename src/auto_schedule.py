# Auto-scheduling script, sends commands to pi based on data in db
import psql_utility as ps
import datetime_utility as dtu
import redis
import os
import sys
import simplejson as json
import datetime
import time


# Redis
r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=os.getenv('REDIS_PORT'), db=0)
p = r.pubsub(ignore_subscribe_messages=True)


while True:
    try:
        # Check if scheduling is set to auto
        autoMode = r.get('autoMode').decode('utf-8')

        if autoMode == '0':
            while not autoMode:
                # to avoid excessive querying
                time.sleep(1)
                autoMode = r.get('autoMode').decode('utf-8')

        # Get current scheduling jobs from SQL server
        jobs = ps.getResultSetFromDBNoJS('"Device".view_schedulerinfo',[])
        print(jobs)

        # store children pids
        children = []

        # Separate each row into a separate thread
        for j in jobs:
            pid = os.fork()
            if pid == 0:
                # Store device ID, we run this until day ends
                deviceID = j['SchedulerDeviceID']

                # Query DB for schedule info
                schedulerInfo = ps.getResultSetFromDBNoJS('"Device".view_schedulerinfo_single', [deviceID])

                # Query handles time info, run until stop time (query returns nothing)
                while schedulerInfo:
                    while schedulerInfo[0]['SchedulerTimeUntilStart'] > 0:
                        # Time remaining is in minutes, convert to seconds and wait
                        time.sleep(schedulerInfo[0]['SchedulerTimeUntilStart'] * 60)

                    print(f"at: {datetime.datetime.now()}")
                    print("executing the following:\n" +json.dumps(schedulerInfo,indent=2))
                    # Send command to redis
                    r.publish('scheduler', json.dumps({
                    'command': schedulerInfo[0]['DeviceType'],
                    'options': {
                        'key': schedulerInfo[0]['RedisKey'],
                        'action': 1,
                        'waitTime': schedulerInfo[0]['SchedulerSecondsToKeepActive']
                    }
                    }))

                    # Sleep for interval or wait for sensor value
                    time.sleep(schedulerInfo[0]['SchedulerSecondsBetweenActivation'])

                # exit process once end time has passed
                os._exit(0);

            else:
                children.append(pid);

        # parent shouldn't do anything after everything stops
        while datetime.datetime.now().minute < 20:
            # If automatic scheduling turned off, kill everything
            time.sleep(1)
            autoMode = r.get('autoMode').decode('utf-8')
            if autoMode == '0':
                for child in children:
                    try:
                        print(f"at: {datetime.datetime.now()}")
                        print("killing: " + child)
                        os.kill(child, 9)
                    except:
                        print(f"failed to kill child: {child}")

                break

        
        # end everything at 8:00 PM
        if autoMode != 0:
            for child in children:
                try:
                    print(f"at: {datetime.datetime.now()}")
                    print("killing: " + child)
                    os.kill(child, 9)
                except:
                    print(f"failed to kill child: {child}")

            # sleep until 4:00 AM
            print(f"at: {datetime.datetime.now()}")
            print(f"sleeping for: {dtu.secondsBeforeTime(4)} seconds")
            time.sleep(dtu.secondsBeforeTime(4))

        except KeyboardInterrupt:
            print('Keyboard Interrupt... Shutting down.')

            for child in children:
                try:
                    print(f"at: {datetime.datetime.now()}")
                    print("killing: " + child)
                    os.kill(child, 9)
                except:
                    print(f"failed to kill child: {child}")
            sys.exit()


                
