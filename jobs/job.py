from google.cloud import firestore
import resend
import logging
import os

if __name__ == "__main__":
  db = firestore.Client(project=os.getenv('PROJECT'))
  resend.api_key = os.getenv('RESEND_API_KEY')

  params = {
    'from': 'Fox Marching Warriors <no-reply@foxmarchingwarriors.band>',
    'to': ['ryanjamescalhoun@gmail.com'],
    'subject': 'Password Reset test email',
    'html': '<h1> Reset your password </h1> <p> Click the link </p>'
  }

  resend.Emails.send(params)
