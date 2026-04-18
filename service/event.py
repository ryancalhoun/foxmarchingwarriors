from flask import Response, jsonify
from google.cloud import firestore
from datetime import datetime

from db import db

header = '''BEGIN:VCALENDAR\r
CALSCALE:GREGORIAN\r
METHOD:PUBLISH\r
X-WR-CALNAME:FoxMarchingWarriors\r
X-WR-TIMEZONE:America/Chicago\r
X-WR-CALDESC:Events for the Fox High School Band Program.\r
'''

trailer = 'END:VCALENDAR\r\n'

def get_calendar_ics():
  def stream():
    yield header
    events = db.collection('events').list_documents()
    for e in events:
      yield e.get().to_dict()['data']
    yield trailer

  return Response(stream(), mimetype='text/calendar')

def get_events():
  events = [
    e.to_dict() for e in db.collection('events').order_by('start').where(filter=firestore.FieldFilter('start', '>', datetime.now())).get()
  ]
  return jsonify({'events': events})

def get_events_by_range(from_date, to_date):
  q = firestore.And([
    firestore.FieldFilter('start', '>', datetime.strptime(from_date, '%Y-%m-%d')),
    firestore.FieldFilter('start', '<', datetime.strptime(to_date, '%Y-%m-%d')),
  ])

  events = [
    e.to_dict() for e in db.collection('events').order_by('start').where(filter=q).get()
  ]
  return jsonify({'events': events})
