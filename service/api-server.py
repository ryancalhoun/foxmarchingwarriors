from flask import Flask, request, jsonify
from google.cloud import firestore
from werkzeug.exceptions import *
import bcrypt
import jwt
import logging
import os
import uuid

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

db = firestore.Client(project=os.getenv('PROJECT'))

@app.route('/api/pages', methods=['GET'])
def get_pages():
  pages = [doc.to_dict() | {'name': doc.id} for doc in db.collection('pages').get()]
  return jsonify({"pages": pages})

@app.route('/api/pages/<page>', methods=['POST'])
def save_page(page):
  db.collection('pages').document(page).set({'contents': request.data.decode('utf-8')}, merge=True)
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

  if 'code' in content and 'code' in user_data:
    if content['code'] != user_data['code']:
      raise Forbidden('user not authenticated')

  if 'new_password' in content:
    password = pw.hash(content['new_password'])
    user.reference.set({'password': password})

  return jsonify({"auth": jwt.encode({'email': content['email']}, os.getenv('JWT_KEY'), algorithm='EdDSA')})

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

