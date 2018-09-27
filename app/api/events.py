from flask import jsonify, request, g

from . import api
from ..models import Event
from .errors import error_response
from .. import naviaddress as na
from .help_func import is_params_passed, fill_navi_address_data
from .. import db
from .auth import token_auth


@api.route("/events", methods=["GET"])
def get_events_for_square():
    required = ["lt_lat", "lt_lng", "rb_lat", "rb_lng"]
    if not request.args or not is_params_passed(request.args, required):
        return error_response(400, "Not all required arguments are passed")

    events = Event.get_for_square(
        lt_lat=request.args["lt_lat"],
        lt_lng=request.args["lt_lng"],
        rb_lat=request.args["rb_lat"],
        rb_lng=request.args["rb_lng"],
        event_type=request.args.get("type", None),
        start=request.args.get("start", None),
        end=request.args.get("end", None)
    )
    return jsonify({"events": [e.to_json() for e in events]})


@api.route('/events/<eid>')
def get_event(eid):
    event = Event.query.get(eid)
    if not event:
        return error_response(404, "Event not found")

    navi_data = na.get_req(
        "/addresses/{0}/{1}".format(
            event.container, event.naviaddress
        ).replace("#", "%23")
    )
    if navi_data.status_code != 200:
        return error_response(navi_data.status_code, navi_data.text)

    navi_event = navi_data.json()

    return jsonify(event.to_json(navi_event["result"]))


@api.route('/events', methods=['POST'])
@token_auth.login_required
def create_event():
    user = g.current_user

    required = ["lat", "lng"]
    if not request.json or not is_params_passed(request.json, required):
        return error_response(400, "Not all required parameters are passed")

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
        return error_response(navi_data.status_code, navi_data.text)

    navi_event = navi_data.json()["result"]
    c, n = navi_event["container"], navi_event["naviaddress"]
    navi_method = "/addresses/accept/{0}/{1}".format(c, n).replace("#", "%23")

    navi_data = na.post_req(
        navi_method,
        json={"container": c, "naviaddress": n},
        headers={
            "auth-token": user.navi_token,
            "content-type": "application/json"
        }
    )
    if navi_data.status_code != 200:
        return error_response(navi_data.status_code, navi_data.text)

    navi_data = na.put_req(
        navi_method.replace("/accept", ""),
        json=fill_navi_address_data(**request.json, owner_email=user.email),
        headers={
            "auth-token": user.navi_token,
            "content-type": "application/json"
        }
    )
    if navi_data.status_code != 200:
        return error_response(navi_data.status_code, navi_data.text)

    event = Event(
        container=c,
        naviaddress=n,
        latitude=request.json["lat"],
        longitude=request.json["lng"],
        start=request.json["event_start"],
        end=request.json["event_end"],
        type=request.json.get("type", "no type"),
        places=request.json.get("seats", None),
        owner=user
    )
    db.session.add_all([user, event])
    db.session.commit()

    return get_event(event.id), 201


@api.route('/events/<int:eid>', methods=['PUT'])
def update_event(eid):
    return jsonify({})


@api.route('/events/<int:eid>', methods=['DELETE'])
def delete_event(eid):
    return jsonify({'result': True})


@api.route('/events/<int:eid>/join', methods=['PUT'])
@token_auth.login_required
def join_event(eid):
    event = Event.query.get(eid)
    if not event:
        return error_response(404, "Event not found")
    event.add_participant(g.current_user)
    db.session.commit()
    return get_event(eid)


@api.route('/events/<int:eid>/exit', methods=['PUT'])
@token_auth.login_required
def exit_event(eid):
    event = Event.query.get(eid)
    if not event:
        return error_response(404, "Event not found")
    event.delete_participant(g.current_user)
    db.session.commit()
    return get_event(eid)
