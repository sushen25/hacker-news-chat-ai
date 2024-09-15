import datetime

from sqlalchemy import func
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<Post {self.id} - {self.title}>"
