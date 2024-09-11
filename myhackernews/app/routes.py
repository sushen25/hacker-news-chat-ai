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

@main.route("/get_posts")
def get_posts():
    posts = get_all_posts()
    return jsonify([{"id": post.id, "title": post.title, "summary": post.summary, "url": post.url} for post in posts])

@main.route("/create_post")
def create_post_temp():
    new_post = create_post(1, "My Post", "This  is my first post", "https://www.example.com")
    return jsonify({"id": new_post.id, "title": new_post.title, "summary": new_post.summary, "url": new_post.url})

@main.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)