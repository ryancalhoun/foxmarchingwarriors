from flask import Response, jsonify
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime

from db import db

header = '''
BEGIN:VCALENDAR
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:FoxMarchingWarriors
X-WR-TIMEZONE:America/Chicago
X-WR-CALDESC:Events for the Fox High School Band Program. 
'''

trailer = 'END:VCALENDAR'

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
    e.to_dict() for e in db.collection('events').order_by('start').where(filter=FieldFilter('start', '>', datetime.now())).get()
  ]
  return jsonify({'events': events})
