from flask import Flask, request, jsonify
from google.cloud import firestore, storage, tasks_v2
from werkzeug.exceptions import *
from jwt.exceptions import *
import bcrypt
import json
import jwt
import logging
import os
import uuid
import urllib.request

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

db = firestore.Client(project=os.getenv('PROJECT'))

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

@app.route('/api/pages', methods=['GET'])
def get_pages():
  pages = [doc.to_dict() | {'name': doc.id} for doc in db.collection('pages').get()]
  return jsonify({"pages": pages})

@app.route('/api/pages/<page>', methods=['POST'])
def save_page(page):
  get_user(request, scope='edit')

  db.collection('pages').document(page).set({'contents': request.data.decode('utf-8')}, merge=True)
  return 'ok'

@app.route('/api/uploads/<page>', methods=['POST'])
def upload(page):
  get_user(request, scope='edit')

  file = request.files['file']

  client = storage.Client(project=os.getenv('PROJECT'))
  bucket = client.bucket(os.getenv('BUCKET'))
  obj = bucket.blob(f'uploads/{page}/{file.filename}')
  obj.upload_from_file(file)

  return jsonify({'url': obj.public_url})

@app.route('/api/events', methods=['GET'])
def get_events():
  events = [e.to_dict() for e in db.collection('events').get()]
  return jsonify({'events': events})

@app.route('/api/users', methods=['GET'])
def get_users():
  get_user(request, scope='users')

  users = [doc.to_dict() | {'email': doc.id} for doc in db.collection('users').get()]
  for user in users:
    user['password'] = bool(user.get('password'))
    user['code'] = bool(user.get('code'))

  return jsonify({"users": users})

@app.route('/api/users/<email>', methods=['POST'])
def update_user(email):
  user = get_user(request)

  if user.id == email:
    check_scope(user, 'edit')
    user = user.reference
  else:
    check_scope(user, 'users')
    user = db.collection('users').document(email)

  user.set(request.form, merge=True)
  return 'ok'

class Password:
  def check(self, pw, h):
    return bcrypt.checkpw(pw.encode('utf-8'), h.encode('utf-8'))

  def hash(self, pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@app.route('/api/authenticate', methods=['POST'])
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

@app.route('/api/forgot', methods=['POST'])
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

@app.route('/api/started')
def startup_probe():
  return 'yes'

@app.route('/api/alive')
def liveness_probe():
  if len(db.collection('pages').get()) == 0:
    raise InternalServerError('database error')
  return 'yes'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return os.getenv('INDEX')

