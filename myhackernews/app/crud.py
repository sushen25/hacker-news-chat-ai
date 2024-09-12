from app import db
from app.models import Post

def create_post(id, title, summary, url):
    new_post = Post(id=id, title=title, summary=summary, url=url)
    db.session.add(new_post)
    db.session.commit()
    return new_post

def get_all_posts():
    return Post.query.all()

def get_post_by_id(id):
    return Post.query.get(id)

def does_post_exist(id) -> bool:
    return Post.query.get(id) is not None

def delete_post(id):
    user = Post.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user