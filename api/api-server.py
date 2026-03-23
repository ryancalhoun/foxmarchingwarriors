from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/', defaults={'my_path': ''})
@app.route('/<path:my_path>')
def sample(my_path):
  return jsonify({"hello": my_path})
