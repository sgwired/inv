from datetime import datetime
from flask import current_app
from inventor import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# comments = db.Table('comments',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'))
# )


# notes = db.Table('notes',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
# )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    address1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120))
    city = db.Column(db.String(60))
    state = db.Column(db.String(60))
    postal_code = db.Column(db.String(15))
    country = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    role = db.Column(db.Integer, nullable=False, default=0)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    nda = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ideas = db.relationship('Idea', backref='inventor', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.id}')"


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    featured_image = db.Column(db.String(20), nullable=False, default='default_image.jpg')
    secondary_image = db.Column(db.String(20), nullable=False, default='default_image.jpg')
    primary_document = db.Column(db.String(20))
    secondary_document = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # comments = db.relationship('Comment', secondary=comments,
    #     backref=db.backref('idea_comments', lazy='dynamic'))
    # notes = db.relationship('Note', secondary=notes,
    #     backref=db.backref('idea_notes', lazy='dynamic'))

    def __repr__(self):
        return f"Idea('{self.title}', '{self.id}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.comment}', '{self.id}')"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Note('{self.note}', '{self.id}')"
