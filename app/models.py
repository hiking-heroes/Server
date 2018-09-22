from flask_login import UserMixin
from . import db


class Participant(db.Model):
    __tablename__ = "participants"
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"),
                         primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    navi_token = db.Column(db.String(36), nullable=False, unique=True)
    own_events = db.relationship("Event", backref="owner",
                                     lazy="dynamic")
    events = db.relationship('Participant',
                             foreign_keys=[Participant.user_id],
                             backref=db.backref('members', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    container = db.Column(db.String(10), nullable=False)
    naviaddress = db.Column(db.String(20), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    members = db.relationship('Participant',
                              foreign_keys=[Participant.user_id],
                              backref=db.backref('events', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
