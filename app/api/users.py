from flask import jsonify, request, abort

from . import api
from ..models import User
from .. import naviaddress as na
from .. import db
from .errors import bad_request, conflict


def is_ready_for_reg(json: dict) -> bool:
    required = ("email", "password", "first_name", "last_name")
    return all([k in required for k in json.keys()])


@api.route('/users/', methods=['POST'])
def create_user():
    if not request.json or not is_ready_for_reg(request.json):
        return bad_request("Not all required parameters are passed")

    navi_data = na.create_user_profile(request.json)
    if navi_data.status_code != 200:
        if navi_data.status_code == 409:
            return conflict(str(navi_data.content))
        else:
            abort(navi_data.status_code)

    navi_user = navi_data.json()

    user = User(id=navi_user["id"], navi_token=navi_user["token"])
    db.session.add(user)
    db.session.commit()

    return jsonify(navi_user), 201


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    return jsonify({})


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return jsonify({'result': True})
