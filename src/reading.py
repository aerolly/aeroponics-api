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
        'key': 'genesis-lowerBed-solenoid',
        'action': 1,
        'waitTime': 10
      }
    }))

def sprayUpper():
  autoMode = r.get('autoMode').decode('utf-8')

  if autoMode == '1':
    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'genesis-upperBed-solenoid',
        'action': 1,
        'waitTime': 10
      }
    }))

def pump():
  autoMode = r.get('autoMode').decode('utf-8')

  if autoMode == '1':
    r.publish('scheduler', json.dumps({
      'command': 'controller',
      'options': {
        'key': 'genesis-system-pump',
        'action': 1,
        'waitTime': 30
      }
    }))

schedule.every().day.at("08:03").do(pump)
schedule.every().day.at("12:00").do(pump)

schedule.every().day.at("07:05").do(sprayLower)
schedule.every().day.at("07:20").do(sprayLower)
schedule.every().day.at("07:35").do(sprayLower)
schedule.every().day.at("07:50").do(sprayLower)
schedule.every().day.at("09:05").do(sprayLower)
schedule.every().day.at("09:20").do(sprayLower)
schedule.every().day.at("09:35").do(sprayLower)
schedule.every().day.at("09:50").do(sprayLower)
schedule.every().day.at("10:05").do(sprayLower)
schedule.every().day.at("10:20").do(sprayLower)
schedule.every().day.at("10:35").do(sprayLower)
schedule.every().day.at("10:50").do(sprayLower)
schedule.every().day.at("11:05").do(sprayLower)
schedule.every().day.at("11:20").do(sprayLower)
schedule.every().day.at("11:35").do(sprayLower)
schedule.every().day.at("11:50").do(sprayLower)
schedule.every().day.at("12:05").do(sprayLower)
schedule.every().day.at("12:20").do(sprayLower)
schedule.every().day.at("12:35").do(sprayLower)
schedule.every().day.at("12:50").do(sprayLower)
schedule.every().day.at("13:05").do(sprayLower)
schedule.every().day.at("13:20").do(sprayLower)
schedule.every().day.at("13:35").do(sprayLower)
schedule.every().day.at("13:50").do(sprayLower)
schedule.every().day.at("14:05").do(sprayLower)
schedule.every().day.at("14:20").do(sprayLower)
schedule.every().day.at("14:35").do(sprayLower)
schedule.every().day.at("14:50").do(sprayLower)
schedule.every().day.at("15:05").do(sprayLower)
schedule.every().day.at("15:20").do(sprayLower)
schedule.every().day.at("15:35").do(sprayLower)
schedule.every().day.at("15:50").do(sprayLower)
schedule.every().day.at("16:05").do(sprayLower)
schedule.every().day.at("16:20").do(sprayLower)
schedule.every().day.at("16:35").do(sprayLower)
schedule.every().day.at("16:50").do(sprayLower)
schedule.every().day.at("17:05").do(sprayLower)
schedule.every().day.at("17:20").do(sprayLower)
schedule.every().day.at("17:35").do(sprayLower)
schedule.every().day.at("17:50").do(sprayLower)
schedule.every().day.at("00:00").do(sprayLower)

schedule.every().day.at("07:00").do(sprayUpper)
schedule.every().day.at("07:15").do(sprayUpper)
schedule.every().day.at("07:30").do(sprayUpper)
schedule.every().day.at("07:45").do(sprayUpper)
schedule.every().day.at("08:00").do(sprayUpper)
schedule.every().day.at("08:15").do(sprayUpper)
schedule.every().day.at("08:30").do(sprayUpper)
schedule.every().day.at("08:45").do(sprayUpper)
schedule.every().day.at("09:00").do(sprayUpper)
schedule.every().day.at("09:15").do(sprayUpper)
schedule.every().day.at("09:30").do(sprayUpper)
schedule.every().day.at("09:45").do(sprayUpper)
schedule.every().day.at("10:00").do(sprayUpper)
schedule.every().day.at("10:15").do(sprayUpper)
schedule.every().day.at("10:30").do(sprayUpper)
schedule.every().day.at("10:45").do(sprayUpper)
schedule.every().day.at("11:00").do(sprayUpper)
schedule.every().day.at("11:15").do(sprayUpper)
schedule.every().day.at("11:30").do(sprayUpper)
schedule.every().day.at("11:45").do(sprayUpper)
schedule.every().day.at("12:03").do(sprayUpper)
schedule.every().day.at("12:15").do(sprayUpper)
schedule.every().day.at("12:30").do(sprayUpper)
schedule.every().day.at("12:45").do(sprayUpper)
schedule.every().day.at("13:00").do(sprayUpper)
schedule.every().day.at("13:15").do(sprayUpper)
schedule.every().day.at("13:30").do(sprayUpper)
schedule.every().day.at("13:45").do(sprayUpper)
schedule.every().day.at("14:00").do(sprayUpper)
schedule.every().day.at("14:15").do(sprayUpper)
schedule.every().day.at("14:30").do(sprayUpper)
schedule.every().day.at("14:45").do(sprayUpper)
schedule.every().day.at("15:00").do(sprayUpper)
schedule.every().day.at("15:15").do(sprayUpper)
schedule.every().day.at("15:30").do(sprayUpper)
schedule.every().day.at("15:45").do(sprayUpper)
schedule.every().day.at("16:00").do(sprayUpper)
schedule.every().day.at("16:15").do(sprayUpper)
schedule.every().day.at("16:30").do(sprayUpper)
schedule.every().day.at("16:45").do(sprayUpper)
schedule.every().day.at("17:00").do(sprayUpper)
schedule.every().day.at("17:15").do(sprayUpper)
schedule.every().day.at("17:30").do(sprayUpper)
schedule.every().day.at("17:45").do(sprayUpper)
schedule.every().day.at("00:05").do(sprayLower)

def takeData():
  temp = json.dumps({
    'command': 'sensor',
    'options': {
      'key': 'genesis-system-pressure',
    }
  })

  pressure = json.dumps({
    'command': 'sensor',
    'options': {
      'key': 'genesis-lowerBed-temperature',
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
