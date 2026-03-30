from flask import Flask, request, jsonify
from google.cloud import firestore, storage
from werkzeug.exceptions import *
from jwt.exceptions import *
import bcrypt
import jwt
import logging
import os
import uuid

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
    if kwargs['scope'] not in (user.to_dict().get('scopes') or []):
      raise Forbidden('user not allowed')

  return user

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

