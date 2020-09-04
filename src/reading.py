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

    time.sleep(5)

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

    time.sleep(5)

    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'lowerBed-solenoid',
        'action': 0
      }
    }))

def pump():
  autoMode = r.get('autoMode').decode('utf-8')

  if autoMode == '1':
    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'pump',
        'action': 1
      }
    }))

    time.sleep(10)

    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'pump',
        'action': 0
      }
    }))

schedule.every().day.at("11:00").do(pump)

schedule.every().day.at("7:35").do(sprayLower)
schedule.every().day.at("8:35").do(sprayLower)
schedule.every().day.at("9:35").do(sprayLower)
schedule.every().day.at("10:35").do(sprayLower)
schedule.every().day.at("12:35").do(sprayLower)
schedule.every().day.at("13:35").do(sprayLower)
schedule.every().day.at("15:35").do(sprayLower)
schedule.every().day.at("17:35").do(sprayLower)

schedule.every().day.at("7:30").do(sprayUpper)
schedule.every().day.at("8:30").do(sprayUpper)
schedule.every().day.at("9:30").do(sprayUpper)
schedule.every().day.at("10:30").do(sprayUpper)
schedule.every().day.at("12:30").do(sprayUpper)
schedule.every().day.at("13:30").do(sprayUpper)
schedule.every().day.at("15:30").do(sprayUpper)
schedule.every().day.at("17:30").do(sprayUpper)

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

def schedule():
  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
  handleSchedule = thread.Thread(target=schedule)
  dataTake = thread.Thread(target=takeData)

  handleSchedule.start()
  dataTake.start()

  handleSchedule.join()
  dataTake.join()
