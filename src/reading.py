import redis
import os
import simplejson as json
import time
import threading
import schedule
import time

import settings

r = redis.Redis(host=os.getenv('REDIS_IP'), port=os.getenv('REDIS_PORT'), db=0)

def sprayLower():
  autoMode = r.get('autoMode').decode('utf-8')

  if autoMode == '1':
    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'lowerBed-solenoid',
        'action': 1
      }
    }))

    time.sleep(3)

    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'lowerBed-solenoid',
        'action': 0
      }
    }))

def sprayUpper():
  autoMode = r.get('autoMode').decode('utf-8')

  if autoMode == '1':
    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'upperBed-solenoid',
        'action': 1
      }
    }))

    time.sleep(3)

    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'upperBed-solenoid',
        'action': 0
      }
    }))

def pump():
  autoMode = r.get('autoMode').decode('utf-8')

  if autoMode == '1':
    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'system-pump',
        'action': 1
      }
    }))

    time.sleep(10)

    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'system-pump',
        'action': 0
      }
    }))

schedule.every().day.at("12:00").do(pump)

schedule.every().day.at("07:35").do(sprayLower)
schedule.every().day.at("08:05").do(sprayLower)
schedule.every().day.at("08:35").do(sprayLower)
schedule.every().day.at("09:05").do(sprayLower)
schedule.every().day.at("09:35").do(sprayLower)
schedule.every().day.at("10:05").do(sprayLower)
schedule.every().day.at("10:35").do(sprayLower)
schedule.every().day.at("11:05").do(sprayLower)
schedule.every().day.at("11:35").do(sprayLower)
schedule.every().day.at("12:05").do(sprayLower)
schedule.every().day.at("12:35").do(sprayLower)
schedule.every().day.at("13:05").do(sprayLower)
schedule.every().day.at("13:35").do(sprayLower)
schedule.every().day.at("15:35").do(sprayLower)
schedule.every().day.at("17:35").do(sprayLower)

schedule.every().day.at("07:30").do(sprayLower)
schedule.every().day.at("08:00").do(sprayLower)
schedule.every().day.at("08:30").do(sprayLower)
schedule.every().day.at("09:00").do(sprayLower)
schedule.every().day.at("09:30").do(sprayLower)
schedule.every().day.at("10:00").do(sprayLower)
schedule.every().day.at("10:30").do(sprayLower)
schedule.every().day.at("11:00").do(sprayLower)
schedule.every().day.at("11:30").do(sprayLower)
schedule.every().day.at("12:00").do(sprayLower)
schedule.every().day.at("12:30").do(sprayLower)
schedule.every().day.at("13:00").do(sprayLower)
schedule.every().day.at("13:30").do(sprayLower)
schedule.every().day.at("15:30").do(sprayLower)
schedule.every().day.at("17:30").do(sprayLower)

def takeData():
  temp = json.dumps({
    'command': 'sensor',
    'options': {
      'key': 'pressure',
    }
  })

  pressure = json.dumps({
    'command': 'sensor',
    'options': {
      'key': 'temperature',
    }
  })

  while True:
    r.publish('scheduler', temp)
    r.publish('scheduler', pressure)
    time.sleep(5)

def scheduler():
  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
  handleSchedule = threading.Thread(target=scheduler)
  dataTake = threading.Thread(target=takeData)

  handleSchedule.start()
  dataTake.start()

  handleSchedule.join()
  dataTake.join()
