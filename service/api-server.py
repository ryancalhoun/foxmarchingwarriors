from flask import Flask
import logging
import os

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


import auth
app.route('/api/authenticate', methods=['POST'])(auth.auth_verify)
app.route('/api/forgot', methods=['POST'])(auth.send_forgot_email)

import page
app.route('/api/layout', methods=['GET'])(page.get_layout)
app.route('/api/pages', methods=['GET'])(page.get_pages)
app.route('/api/pages/<page>', methods=['GET'])(page.get_current_contents)
app.route('/api/pages/<page>/<v0>', methods=['POST'])(page.save_page)
app.route('/api/uploads/<page>', methods=['POST'])(page.upload)

import event
app.route('/api/events', methods=['GET'])(event.get_events)
app.route('/api/events/<from_date>/<to_date>', methods=['GET'])(event.get_events_by_range)
app.route('/calendar.ics', methods=['GET'])(event.get_calendar_ics)

import user
app.route('/api/users', methods=['GET'])(user.get_users)
app.route('/api/users/me', methods=['GET'])(user.get_myself)
app.route('/api/users/<email>', methods=['POST'])(user.update_user)

import probe
app.route('/api/started')(probe.startup_probe)
app.route('/api/alive')(probe.liveness_probe)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return os.getenv('INDEX')

