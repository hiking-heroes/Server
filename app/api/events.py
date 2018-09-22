from flask import jsonify

from . import api
from ..models import Event


@api.route('/events/<int:id>')
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify(event.to_json())


@api.route('/events/', methods=['POST'])
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

