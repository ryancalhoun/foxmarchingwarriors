from flask import Flask, request
from google.cloud import firestore
from werkzeug.exceptions import *
from urllib.request import build_opener
from icalendar import Calendar
import resend
import logging
import os

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/hourly', methods=['POST'])
def hourly():
  url = os.getenv('CALENDAR')

  try:
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0;FoxMarchingBand/1.0')]
    data = opener.open(url).read()
  except Exception as e:
    app.logger.info(e)
    raise e
  cal = Calendar.from_ical(data)

  db = firestore.Client(project=os.getenv('PROJECT'))
  events = db.collection('events')

  for e in cal.events:
    events.document(e.uid).set({
      'start': e.start,
      'end': e.end,
      'data': e.to_ical().decode('utf-8'),
    })

  return 'ok'

@app.route('/send-email', methods=['POST'])
def send_email():
  data = request.get_json()

  app.logger.info(f'Send to={data["to"]} subject={data["subject"]}')

  resend.api_key = os.getenv('RESEND_API_KEY')

  params = {
    'from': 'Fox Marching Warriors <no-reply@foxmarchingwarriors.band>',
    'to': [data['to']],
    'subject': data['subject'],
    'html': data['body'],
  }

  res = resend.Emails.send(params)
  app.logger.info(f'Sent ID={res["id"]}')

  return 'ok'
