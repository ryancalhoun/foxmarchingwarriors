from flask import Flask, request
from werkzeug.exceptions import *
import resend
import logging
import os

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/send', methods=['POST'])
def send_email():
  data = request.get_json()

  app.logger.info(f'Send to={data["to"]} subject={data["subject"]}')

  resend.api_key = os.getenv('RESEND_API_KEY')

  params = {
    'from': 'Fox Marching Warriors <no-reply@foxmarchingwarriors.band>',
    'to': [data['to']],
    'subject': data['subject'],
    'html': data['body'],
  }

  res = resend.Emails.send(params)
  app.logger.info(f'Sent ID={res["id"]}')

  return 'ok'
