from flask import jsonify, request

from . import api
from .errors import abort_json
from ..models import Event


def is_square(json: dict) -> bool:
    required = ("lt_lat", "lt_lng", "rb_lat", "rb_lng")
    return all([k.lower() in required for k in json])


def get_square_from_args(json: dict) -> tuple:
    return json["lt_lat"], json["lt_lng"], json["rb_lat"], json["rb_lng"]


@api.route("/map", methods=["GET"])
def get_events_for_square():
    if not request.args or not is_square(request.args):
        abort_json(400, "Not all required arguments are passed")

    events = Event.get_for_square(
        *get_square_from_args(request.args), request.args.get("type") or "any"
    )
    return jsonify([e.to_json() for e in events])
