from flask import current_app
from flask_login import UserMixin

from . import db
from . import fcm_notifications as fcm


class Participant(db.Model):
    __tablename__ = "participants"
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"),
                         primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)


class EventTag(db.Model):
    __tablename__ = "events_tags"
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"),
                         primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"),
                       primary_key=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    navi_token = db.Column(db.String(36), nullable=False)
    own_events = db.relationship("Event", backref="owner",
                                 lazy="dynamic")
    events = db.relationship('Participant',
                             foreign_keys=[Participant.user_id],
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    devices = db.relationship("Device", backref="owner",
                              lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_all_events(self) -> list:
        events = [e.to_json() for e in self.own_events.all()]
        events.extend([e.to_json() for e in self.get_events()])
        return events

    def get_events(self):
        return Event.query.join(
            Participant, Participant.event_id == Event.id
        ).filter(
            Participant.user_id == self.id
        )

    @staticmethod
    def check_token(token):
        return User.query.filter_by(navi_token=token).first()

    def notify(self, title: str = None, body: str = None):
        if self.devices.count():
            fcm.send_notification(
                server_key=current_app.config["FCM_KEY"],
                registration_ids=[d.token for d in self.devices.all()],
                notification={"title": title, "body": body}
            )


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    container = db.Column(db.String(10), nullable=False)
    naviaddress = db.Column(db.String(20), nullable=False, unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    start = db.Column(db.String(24))
    end = db.Column(db.String(24))
    places = db.Column(db.Integer)
    type = db.Column(db.String(25), index=True, default="no type")
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    participants = db.relationship('Participant',
                                   foreign_keys=[Participant.event_id],
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    tags = db.relationship('EventTag',
                           foreign_keys=[EventTag.event_id],
                           lazy='dynamic',
                           cascade='all, delete-orphan')

    @staticmethod
    def get_for_square(lt_lat, lt_lng, rb_lat, rb_lng, event_type=None,
                       start=None, end=None):
        q = Event.query.filter(
            Event.latitude > lt_lat,
            Event.longitude > lt_lng,
            Event.latitude < rb_lat,
            Event.longitude < rb_lng,
        )
        if event_type:
            q = q.filter(Event.type == event_type)
        if start and end:
            q = q.filter(
                Event.start > start,
                Event.start < end
            )
        return q.all()

    def get_participants(self):
        return User.query.join(
            Participant, Participant.user_id == User.id
        ).filter(
            Participant.event_id == self.id
        )

    def add_participant(self, user):
        if user not in self.participants:
            p = Participant(user_id=user.id, event_id=self.id, confirmed=True)
            db.session.add(p)

    def delete_participant(self, user):
        p = self.participants.filter_by(user_id=user.id).first()
        if p:
            db.session.delete(p)

    def add_tag(self, tag):
        if tag not in self.tags:
            et = EventTag(event_id=self.id, tag_id=tag.id)
            db.session.add(et)

    def delete_tag(self, tag):
        t = self.tags.filter_by(tag_id=tag.id).first()
        if t:
            db.session.delete(t)

    def get_tags(self):
        return Tag.query.join(EventTag, EventTag.tag_id == Tag.id).filter(
            EventTag.event_id == self.id
        )

    def to_json(self, navi: dict = None) -> dict:
        response = {
            "id": self.id,
            "name": self.name,
            "container": self.container,
            "naviaddress": self.naviaddress,
            "owner_id": self.owner_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start": self.start,
            "end": self.end,
            "type": self.type,
            "seats": {
                "total": self.places,
                "free": self.places - self.participants.filter_by(
                    confirmed=True).count()if self.places else None
            },
            "tags": [t.title for t in self.get_tags()]
        }
        if navi:
            response["navi"] = navi

        return response


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), index=True, nullable=False)
    events = db.relationship('EventTag',
                             foreign_keys=[EventTag.tag_id],
                             lazy='dynamic',
                             cascade='all, delete-orphan')

    @staticmethod
    def get_or_create(title):
        t = Tag.query.filter_by(title=title).first()
        if not t:
            t = Tag(title=title)
            db.session.add(t)
        return t

    def get_events(self):
        return Event.query.join(
            EventTag, EventTag.event_id == Event.id
        ).filter(
            EventTag.tag_id == self.id
        )


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(152), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_json(self):
        return {
            "id": self.id,
            "token": self.token
        }
