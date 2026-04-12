from werkzeug.exceptions import *
from db import db

def startup_probe():
  return 'yes'

def liveness_probe():
  if len(db.collection('pages').get()) == 0:
    raise InternalServerError('database error')
  return 'yes'

