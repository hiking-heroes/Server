from flask import jsonify, request

from . import api
from ..models import Event
from .errors import abort_json
from .. import naviaddress as na


def is_square(json: dict) -> bool:
    required = ("lt_lat", "lt_lng", "rb_lat", "rb_lng")
    return all([json.get(r) for r in required])


def get_square_from_args(json: dict) -> tuple:
    return json["lt_lat"], json["lt_lng"], json["rb_lat"], json["rb_lng"]


@api.route("/events", methods=["GET"])
def get_events_for_square():
    if not request.args or not is_square(request.args):
        return abort_json(400, "Not all required arguments are passed")

    events = Event.get_for_square(
        *get_square_from_args(request.args), request.args.get("type") or "any"
    )
    return jsonify({"events": [e.to_json() for e in events]})


@api.route('/events/<int:id>')
def get_event(id):
    event = Event.query.get(id)
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
    return jsonify({}), 201


@api.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    return jsonify({})


@api.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    return jsonify({'result': True})


@api.route('/events/<int:id>/members', methods=['POST'])
def add_member(id):
    return jsonify()


@api.route('/events/<int:id>/members', methods=['DELETE'])
def delete_member(id):
    return jsonify()

