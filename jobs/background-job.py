from flask import Flask, request
from google.cloud import firestore
from werkzeug.exceptions import *
from urllib.request import build_opener
from icalendar import Calendar
from icalendar.prop.uri import vUri
from datetime import datetime, date, time
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
    event_props = {
      'start': type(e.start) == datetime and e.start or datetime.combine(e.start, time(0, 0)),
      'end': type(e.end) == datetime and e.end or datetime.combine(e.end, time(23, 59)),
      'data': e.to_ical().decode('utf-8'),
    }

    events.document(e.uid).set(event_props)

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
