import smtplib, ssl
import os

#msg format:
#Subject: <subject>
#\n
#\n
#<body>
def sendDevMail(msg):
  port = 465
  user = os.getenv('GMAIL_USER')
  password = os.getenv('GMAIL_PASS')
  host = "smtp.gmail.com"
  
  context = ssl.create_default_context()

  with smtplib.SMTP_SSL(host, port, context=context) as server:
    server.login(user, password)
    server.sendmail(user, user, msg)
    server.quit()
