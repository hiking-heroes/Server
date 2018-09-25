from flask import jsonify, request

from . import api
from ..models import User
from .. import naviaddress as na
from .. import db
from .errors import abort_json


def is_ready_for(json: dict, is_reg=False) -> bool:
    required = ["email", "password"]
    if is_reg:
        required.extend(["first_name", "last_name"])
    return all([json.get(r) for r in required])


@api.route('/users/signup', methods=['POST'])
def create_user():
    """SIGN UP"""
    if not request.json or not is_ready_for(request.json, is_reg=True):
        return abort_json(400, "Not all required parameters are passed")

    navi_data = na.post_req(
        "/profile",
        json=request.json,
        headers={"content-type": "application/json"}
    )
    if navi_data.status_code != 200:
        return abort_json(navi_data.status_code, navi_data.text)

    navi_user = navi_data.json()

    user = User(
        id=navi_user["id"],
        email=navi_user["email"],
        navi_token=navi_user["token"]
    )
    db.session.add(user)
    db.session.commit()

    navi_user["events"] = []

    return jsonify(navi_user), 201


@api.route('/users/signin', methods=['POST'])
def check_user():
    """SIGN IN"""
    if not request.json or not is_ready_for(request.json):
        return abort_json(400, "Not all required parameters are passed")

    navi_data = na.post_req(
        "/sessions",
        json=request.json,
        headers={"content-type": "application/json"}
    )
    if navi_data.status_code != 200:
        return abort_json(navi_data.status_code, navi_data.text)

    navi_user = navi_data.json()

    user = User.query.get(navi_user["id"])
    if user:
        user.navi_token = navi_user["token"]
    else:
        user = User(
            id=navi_user["id"],
            email=navi_user["email"],
            navi_token=navi_user["token"]
        )
    db.session.add(user)
    db.session.commit()

    navi_user["events"] = user.get_events()

    return jsonify(navi_user)


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    return jsonify({})


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return jsonify({'result': True})
