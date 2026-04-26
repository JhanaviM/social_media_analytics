from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import json


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cases = db.relationship('Case', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    keyword = db.Column(db.String(150), nullable=False)
    platform = db.Column(db.String(30), nullable=False)  # X or Facebook
    description = db.Column(db.Text, nullable=True)
    apify_source = db.Column(db.String(300), nullable=True)
    post_ids = db.Column(db.Text, nullable=True)
    time_range_start = db.Column(db.DateTime, nullable=True)
    time_range_end = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default='created')  # created, running, done
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    results = db.relationship('AnalysisResult', backref='case', lazy=True, cascade='all, delete')
    raw_data = db.relationship('RawPost', backref='case', lazy=True, cascade='all, delete')

    def __repr__(self):
        return f'<Case {self.name}>'


class RawPost(db.Model):
    __tablename__ = 'raw_posts'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    post_id = db.Column(db.String(200), nullable=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(200), nullable=True)
    author_followers = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    retweets = db.Column(db.Integer, default=0)
    replies = db.Column(db.Integer, default=0)
    platform = db.Column(db.String(30), nullable=True)
    posted_at = db.Column(db.DateTime, nullable=True)
    hashtags = db.Column(db.Text, nullable=True)  # JSON list
    url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_hashtags(self):
        try:
            return json.loads(self.hashtags) if self.hashtags else []
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': self.author,
            'author_followers': self.author_followers,
            'likes': self.likes,
            'retweets': self.retweets,
            'replies': self.replies,
            'platform': self.platform,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'hashtags': self.get_hashtags(),
        }


class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    module = db.Column(db.String(50), nullable=False)
    result_data = db.Column(db.Text, nullable=False)  # JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_data(self):
        try:
            return json.loads(self.result_data)
        except Exception:
            return {}

    def set_data(self, data):
        self.result_data = json.dumps(data)

    def __repr__(self):
        return f'<AnalysisResult case={self.case_id} module={self.module}>'
