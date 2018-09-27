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
    email = db.Column(db.String(50), nullable=False, unique=True)
    navi_token = db.Column(db.String(36), nullable=False)
    own_events = db.relationship("Event", backref="owner",
                                 lazy="dynamic")
    events = db.relationship('Participant',
                             foreign_keys=[Participant.user_id],
                             lazy='dynamic',
                             cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_events(self) -> list:
        return [e.to_json() for e in self.events.all()]

    def create_event(self, json: dict):
        pass

    @staticmethod
    def check_token(token):
        return User.query.filter_by(navi_token=token).first()


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    @staticmethod
    def get_for_square(lt_lat, lt_lng, rb_lat, rb_lng, event_type):
        return Event.query.filter(
            Event.latitude > lt_lat,
            Event.longitude > lt_lng,
            Event.latitude < rb_lat,
            Event.longitude < rb_lng,
            event_type == "any" or Event.type == event_type
        ).all()

    def add_participant(self, user):
        if user not in self.participants:
            p = Participant(user_id=user.id, event_id=self.id, confirmed=True)
            db.session.add(p)

    def to_json(self, navi: dict = None) -> dict:
        response = {
            "id": self.id,
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
            }
        }
        if navi:
            response["navi"] = navi

        return response
