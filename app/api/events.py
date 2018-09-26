from flask import jsonify, request

from . import api
from ..models import Event, User
from .errors import abort_json
from .. import naviaddress as na
from .help_func import is_params_passed
from .. import db


@api.route("/events", methods=["GET"])
def get_events_for_square():
    required = ["lt_lat", "lt_lng", "rb_lat", "rb_lng"]
    if not request.args or not is_params_passed(request.args, required):
        return abort_json(400, "Not all required arguments are passed")

    events = Event.get_for_square(
        lt_lat=request.args["lt_lat"],
        lt_lng=request.args["lt_lng"],
        rb_lat=request.args["rb_lat"],
        rb_lng=request.args["rb_lng"],
        event_type=request.args.get("type", "any")
    )
    return jsonify({"events": [e.to_json() for e in events]})


@api.route('/events/<eid>')
def get_event(eid):
    event = Event.query.get(eid)
    if not event:
        return abort_json(404, "Event not found")

    navi_data = na.get_req(
        "/addresses/{0}/{1}".format(event.container, event.naviaddress)
    )
    if navi_data.status_code != 200:
        return abort_json(navi_data.status_code, navi_data.text)

    navi_event = navi_data.json()

    return jsonify(event.to_json(navi_event["result"]))


@api.route('/events', methods=['POST'])
def create_event():
    user = User.query.filter_by(navi_token=request.headers.get("token", ""))
    if not user:
        abort_json(401, "Token check failed")

    required = ["lat", "lng"]
    if not request.json or not is_params_passed(request.json, required):
        return abort_json(400, "Not all required parameters are passed")

    navi_data = na.post_req(
        "/addresses",
        json={
            "lat": request.json["lat"],
            "lng": request.json["lng"],
            "address_type": "event",
            "default_lang": request.json.get("default_lang", "ru")
        },
        headers={
            "auth-token": user.navi_token,
            "content-type": "application/json"
        }
    )
    if navi_data.status_code != 200:
        return abort_json(navi_data.status_code, navi_data.text)

    c, n = navi_data.json()["container"], navi_data.json()["naviaddress"]

    navi_data = na.post_req(
        "/addresses/accept/{0}/{1}".format(c, n).replace("#", "%23"),
        json={"container": c, "naviaddress": n},
        headers={
            "auth-token": user.navi_token,
            "content-type": "application/json"
        }
    )
    if navi_data.status_code != 200:
        return abort_json(navi_data.status_code, navi_data.text)

    # 3. TODO: Обновить его информацию в нави

    event = Event(
        container=c,
        naviaddress=n,
        latitude=request.json["lat"],
        longitude=request.json["lng"],
        type=request.json.get("type", "no type"),
        owner=user
    )
    db.session.add_all([user, event])
    db.session.commit()

    return jsonify(navi_data.json()), 201


@api.route('/events/<int:eid>', methods=['PUT'])
def update_event(eid):
    return jsonify({})


@api.route('/events/<int:eid>', methods=['DELETE'])
def delete_event(eid):
    return jsonify({'result': True})


@api.route('/events/<int:eid>/members', methods=['POST'])
def add_member(eid):
    return jsonify()


@api.route('/events/<int:eid>/members', methods=['DELETE'])
def delete_member(eid):
    return jsonify({'result': True})
