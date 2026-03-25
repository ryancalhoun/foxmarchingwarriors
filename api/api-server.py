from flask import Flask, request, jsonify
from google.cloud import firestore
from werkzeug.exceptions import *
import bcrypt
import jwt
import uuid
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

db = firestore.Client(project='foxmarchingwarriors')
with open('jwt.key') as f:
  jwt_key = f.read()

def str_bytes(f, *args):
  return f(*(type(arg) == str and arg.encode('utf-8') or arg for arg in args))

@app.route('/pages')
def get_pages():
  pages = [doc.to_dict() | {'name': doc.id} for doc in db.collection('pages').get()]
  return jsonify({"pages": pages})

@app.route('/authenticate', methods=['POST'])
def auth_verify():
  content = request.form
  app.logger.info(content)

  user = db.collection('users').document(content['email']).get()
  if not user.exists:
    raise Forbidden('user not authenticated')

  user_data = user.to_dict()
  app.logger.info(user_data)

  if not 'code' in content:
    if not str_bytes(bcrypt.checkpw, content['password'], user_data['password']):
      raise Forbidden('user not authenticated')

  if 'code' in content and 'code' in user_data:
    if content['code'] != user_data['code']:
      raise Forbidden('user not authenticated')

  if 'new_password' in content:
    password = str_bytes(bcrypt.hashpw, content['new_password'], bcrypt.gensalt())
    user.reference.set({'password': password})

  return jsonify({"auth": jwt.encode({'email': content['email']}, jwt_key, algorithm='EdDSA')})

@app.route('/health')
def health():
  return 'ok'
