import os
import time

from utility.mail import sendDevMail

# Send email if rpi not connectable
def handleConnectionCheck():
  rpi_ip = os.getenv('RPI_IP')

  disconnectMsg = 'Subject: Unable To Connect To RPI\n\nHEEEEEEEEEEEEEEEEEEEEELP'
  reconnectMsg = 'Subject: Connection reestablished to RPI\n\n\nnvm'

  while True:
    try:
      response = os.system(f"ping -c 1 -t 2 {rpi_ip}")
      if response != 0:
        # two prevent duds, must be two missed packets in a row
        time.sleep(1)
        response = os.system(f"ping -c 1 -t 2 {rpi_ip}")
        if response != 0:
          sendDevMail(disconnectMsg)
          while response != 0:
            time.sleep(10)
            response = os.system(f"ping -c 1 -t 2 {rpi_ip}")
          sendDevMail(reconnectMsg)
      else:
        time.sleep(10)
    except:
      print('Something went wrong checking connection')