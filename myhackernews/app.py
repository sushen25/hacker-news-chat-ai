from flask import Flask, jsonify, make_response
from flask_cors import CORS
from myHackerNews import get_top_news

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080'])


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/get_top_news")
def hello():
    top_news = get_top_news()
    return top_news


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
