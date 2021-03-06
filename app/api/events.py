from flask import jsonify, request, g

from . import api
from .auth import token_auth
from .errors import error_response
from .help_func import is_params_passed, fill_navi_address_data
from .. import db
from .. import naviaddress as na
from ..models import Event, Tag


@api.route("/events", methods=["GET"])
def get_events_for_square():
    required = ["lt_lat", "lt_lng", "rb_lat", "rb_lng"]
    if not request.args or not is_params_passed(request.args, required):
        return error_response(400, "Not all required arguments are passed")

    tags = request.args.get("tags")
    tags = Tag.get_tags_list(tags.split(",") if tags else [])

    events = Event.get_for_square(
        lt_lat=request.args["lt_lat"],
        lt_lng=request.args["lt_lng"],
        rb_lat=request.args["rb_lat"],
        rb_lng=request.args["rb_lng"],
        event_type=request.args.get("type", None),
        start=request.args.get("start", None),
        end=request.args.get("end", None),
        tags=tags
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

    seats = int(request.json.get("seats")) if request.json.get("seats") else 0

    event = Event(
        container=c,
        name=request.json["name"],
        naviaddress=n,
        latitude=request.json["lat"],
        longitude=request.json["lng"],
        start=request.json["event_start"],
        end=request.json["event_end"],
        type=request.json.get("type", "no type"),
        places=seats,
        owner=user
    )
    tags = []
    for tag in request.json["tags"]:
        if tag:
            tags.append(Tag.get_or_create(tag.lower()))
    for tag in tags:
        event.add_tag(tag)

    session_values = [user, event]
    session_values.extend(tags)
    db.session.add_all(session_values)
    db.session.commit()

    user.notify(body="Event crated: [{0}]{1}".format(c, n))

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
    g.current_user.notify(
        body="You've been joined to the event [{0}]{1}".format(
            event.container, event.naviaddress
        )
    )
    event.owner.notify(
        title="User joined",
        body="User {0} has been joined to your event [{1}]{2}".format(
            g.current_user.email, event.container, event.naviaddress
        )
    )
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


@api.route('/events/my', methods=['GET'])
@token_auth.login_required
def get_user_events():
    tags = request.args.get("tags")
    tags = Tag.get_tags_list(tags.split(",") if tags else [])

    return jsonify(
        {
            "events": g.current_user.get_all_events(
                event_type=request.args.get("type"),
                start=request.args.get("start"),
                end=request.args.get("end"),
                tags=tags
            )
        }
    )
