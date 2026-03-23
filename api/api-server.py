from flask import Flask, request, jsonify
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client(project='foxmarchingwarriors')

@app.route('/pages')
def sample():
  pages = [doc.to_dict()['name'] for doc in db.collection('pages').get()]
  return jsonify({"hello": pages})

@app.route('/health')
def health():
  return 'ok'
