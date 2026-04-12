from flask import jsonify
from db import db

def get_events():
  events = [e.to_dict() for e in db.collection('events').get()]
  return jsonify({'events': events})
