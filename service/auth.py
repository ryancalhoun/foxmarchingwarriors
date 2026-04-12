from flask import request, jsonify
from google.cloud import tasks_v2
from werkzeug.exceptions import *
from jwt.exceptions import *
import bcrypt
import jwt
import json
import os
import uuid
from db import db

def get_user(req, **kwargs):
  auth = req.headers.get('Authorization')
  if not auth or not auth.startswith('Bearer '):
    raise Unauthorized('action requires login')

  token = auth.split()[1]
  try:
    user_info = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['EdDSA'])
  except DecodeError:
    raise Unauthorized('invalid user token')

  user = db.collection('users').document(user_info['email']).get()

  if not user.exists:
    raise Forbidden('user not allowed')

  if 'scope' in kwargs:
    check_scope(user, kwargs['scope'])

  return user

def check_scope(user, scope):
  if scope not in (user.to_dict().get('scopes') or []):
      raise Forbidden('user not allowed')

class Password:
  def check(self, pw, h):
    return bcrypt.checkpw(pw.encode('utf-8'), h.encode('utf-8'))

  def hash(self, pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def auth_verify():
  content = request.form

  user = db.collection('users').document(content['email']).get()
  if not user.exists:
    raise Forbidden('user not registered')

  user_data = user.to_dict()
  pw = Password()

  if not 'code' in content:
    if not pw.check(content['password'], user_data['password']):
      raise Forbidden('user not authenticated')

  if 'code' in content and user_data.get('code'):
    if content['code'] != user_data['code']:
      raise Forbidden('user not authenticated')

  if 'new_password' in content:
    password = pw.hash(content['new_password'])
    user.reference.set({'password': password, 'code': None}, merge=True)

  jwt_id = {
    'email': content['email'],
    'scopes': user_data.get('scopes') or [],
  }

  return jsonify({"auth": jwt.encode(jwt_id, os.getenv('JWT_KEY'), algorithm='EdDSA')})

def send_forgot_email():
  content = request.form

  user = db.collection('users').document(content['email']).get()
  if not user.exists:
    raise Forbidden('user not registered')

  code = str(uuid.uuid4())
  user.reference.set({'code': code}, merge=True)

  params = urllib.parse.urlencode({
    'email': content['email'],
    'code': code,
  })

  button_style = " ".join([f'{k}: {v};' for k,v in {
    'padding':         '8px 32px',
    'color':           'white',
    'background':      'black',
    'border-radius':   '8px',
    'text-decoration': 'none',
    'font-size':       'x-large',
  }.items()])

  reset_info = {
    'to': content['email'],
    'subject': 'Password Reset',
    'body': f'''
      <p> Hello! </p>
      <p> You requested a link to reset your FoxMarchingWarriors password. <p>
      <p> Click the link below to create a new password. </p>
      <p>
        <a href="https://foxmarchingwarriors.band/reset-password?{params}" style="{button_style}">
          Log in
        </a>
      </p>
      <p> If you did not make this request, please disregard this email. </p>
    '''
  }

  tasks = tasks_v2.CloudTasksClient()
  path = tasks.queue_path(os.getenv('PROJECT'), os.getenv('REGION'), os.getenv('QUEUE'))

  task = {
    'http_request': {
      'http_method': 'POST',
      'url': os.getenv('SEND_URL'),
      'headers': {'Content-Type': 'application/json'},
      'body': json.dumps(reset_info).encode(),
    }
  }

  tasks.create_task(parent=path, task=task)
  return 'ok'
