from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from myHackerNews import get_top_news

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080'])

db_uri = "postgresql://admin:admin@localhost:5432/mydb"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri  # Change to your database URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Post


@app.route("/", methods=['GET'])
def hello_from_root():
    return jsonify(message='Hello from root!')

@app.route("/")


@app.route("/get_top_news")
def hello():
    top_news = get_top_news()
    return top_news


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
