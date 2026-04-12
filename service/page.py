from flask import request, jsonify
from google.cloud import storage
from werkzeug.exceptions import *
import os

from db import db
import auth

def get_pages():
  pages = [doc.to_dict() | {'name': doc.id} for doc in db.collection('pages').get()]
  return jsonify({"pages": pages})

def save_page(page):
  auth.get_user(request, scope='edit')

  db.collection('pages').document(page).set({'contents': request.data.decode('utf-8')}, merge=True)
  return 'ok'

def upload(page):
  auth.get_user(request, scope='edit')

  file = request.files['file']

  client = storage.Client(project=os.getenv('PROJECT'))
  bucket = client.bucket(os.getenv('BUCKET'))
  obj = bucket.blob(f'uploads/{page}/{file.filename}')
  obj.upload_from_file(file)

  return jsonify({'url': obj.public_url})
