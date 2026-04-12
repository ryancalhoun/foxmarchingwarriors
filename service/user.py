from flask import request, jsonify
import auth
from db import db

def get_myself():
  user = auth.get_user(request)
  info = user.to_dict()

  del info['code']
  del info['password']

  return jsonify(info)

def get_users():
  auth.get_user(request, scope='users')

  users = [doc.to_dict() | {'email': doc.id} for doc in db.collection('users').get()]
  for user in users:
    user['password'] = bool(user.get('password'))
    user['code'] = bool(user.get('code'))

  return jsonify({"users": users})

def update_user(email):
  user = auth.get_user(request)

  if user.id == email:
    auth.check_scope(user, 'edit')
    user = user.reference
  else:
    auth.check_scope(user, 'users')
    user = db.collection('users').document(email)

  user.set(request.form, merge=True)
  return 'ok'
