from flask import jsonify, request

from . import api
from .errors import error_response
from .help_func import is_params_passed
from .. import db
from .. import naviaddress as na
from ..models import User


@api.route('/users/signup', methods=['POST'])
def create_user():
    """SIGN UP"""
    required = ["email", "password", "first_name", "last_name"]
    if not request.json or not is_params_passed(request.json, required):
        return error_response(400, "Not all required parameters are passed")

    navi_data = na.post_req(
        "/profile",
        json=request.json,
        headers={"content-type": "application/json"}
    )
    if navi_data.status_code != 200:
        return error_response(navi_data.status_code, navi_data.text)

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
    required = ["email", "password"]
    if not request.json or not is_params_passed(request.json, required):
        return error_response(400, "Not all required parameters are passed")

    navi_data = na.post_req(
        "/sessions",
        json=request.json,
        headers={"content-type": "application/json"}
    )
    if navi_data.status_code != 200:
        return error_response(navi_data.status_code, navi_data.text)

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

    user.notify("Sign In", "Account was signed in.")

    navi_user["events"] = user.get_all_events()

    return jsonify(navi_user)


@api.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    return jsonify({})


@api.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    return jsonify({'result': True})
