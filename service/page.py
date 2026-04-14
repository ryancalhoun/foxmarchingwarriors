from flask import request, jsonify
from google.cloud import storage
from datetime import datetime
from werkzeug.exceptions import *
import os

from db import db
import auth

def get_pages():
  pages = [doc.to_dict() | {'name': doc.id} for doc in db.collection('pages').get()]
  return jsonify({"pages": pages})

def get_layout():
  doc = db.collection('layout').document('current').get()
  return jsonify(doc.to_dict())

def get_current_contents(page):
  doc = db.collection('pages').document(page).get()
  v = doc.update_time.strftime('%Y%m%d-%H%M%S')
  return jsonify(doc.to_dict() | {'v' : v })

def save_page(page, v0):
  user = auth.get_user(request, scope='edit')

  history = db.collection('pages').document(page)

  doc = history.get()
  if v0 != doc.update_time.strftime('%Y%m%d-%H%M%S'):
    raise Conflict(f'version {v0} is out of date')

  contents = request.data.decode('utf-8')

  history.collection('versions').document(v0).set(doc.to_dict())
  v1 = history.set({
    'author': user.id,
    'contents': contents,
  })

  return jsonify({'v': v1.update_time.strftime('%Y%m%d-%H%M%S')})

def upload(page):
  auth.get_user(request, scope='edit')

  file = request.files['file']

  client = storage.Client(project=os.getenv('PROJECT'))
  bucket = client.bucket(os.getenv('BUCKET'))
  obj = bucket.blob(f'uploads/{page}/{file.filename}')
  obj.upload_from_file(file)

  return jsonify({'url': obj.public_url})
