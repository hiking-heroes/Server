from flask import jsonify, request, g

from . import api
from ..models import Device
from .errors import error_response
from .help_func import is_params_passed
from .. import db
from .auth import token_auth


@api.route("/notifications/devices", methods=["POST"])
@token_auth.login_required
def subscribe_to_notifications():
    required = ["device_token"]
    if not request.json or not is_params_passed(request.json, required):
        return error_response(400, "Not all required parameters are passed")

    d = Device(token=request.json["device_token"], owner=g.current_user)

    db.session.add(d)
    db.session.commit()

    return jsonify(d.to_json()), 201


@api.route("/notifications/devices/<int:did>", methods=["DELETE"])
@token_auth.login_required
def unsubscribe_from_notifications(did):
    d = g.current_user.devices.filter_by(id=did).first()
    if d:
        db.session.delete(d)
    else:
        return error_response(404, "Device not found for user")

    db.session.commit()

    return get_subscribed_devices()


@api.route("/notifications/devices")
@token_auth.login_required
def get_subscribed_devices():
    return jsonify([d.to_json() for d in g.current_user.devices.all()])
