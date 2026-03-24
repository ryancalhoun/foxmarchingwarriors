from flask import Flask, request, jsonify
from google.cloud import firestore
from werkzeug.exceptions import *
import bcrypt

app = Flask(__name__)

db = firestore.Client(project='foxmarchingwarriors')

@app.route('/pages')
def get_pages():
  pages = [doc.to_dict() | {'name': doc.id} for doc in db.collection('pages').get()]
  return jsonify({"pages": pages})

@app.route('/authenticate', methods=['POST'])
def auth():
  content = request.form

  user = db.collection('users').document(content['email']).get()
  if not user.exists or not bcrypt.checkpw(content['password'], user.to_dict()['password']):
    raise Forbidden('user not authenticated')

  return jsonify({"auth": "<token>"})

@app.route('/health')
def health():
  return 'ok'
