from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080'])


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
