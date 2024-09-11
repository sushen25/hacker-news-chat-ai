from flask import Blueprint, make_response, jsonify
from myHackerNews import get_top_news
from app.crud import get_all_posts, create_post

main = Blueprint('main', __name__)

@main.route("/", methods=['GET'])
def hello_from_root():
    return jsonify(message='Hello from root!')

@main.route("/get_top_news")
def get_news():
    top_news = get_top_news()
    return top_news


@main.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)