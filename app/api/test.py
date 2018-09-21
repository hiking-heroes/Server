from flask import jsonify
from . import api


@api.route('/users/')
def get_user():
    users = [{"name": "test1", "navi": 1}, {"name": "test2", "navi": 2}]
    return jsonify(users)
