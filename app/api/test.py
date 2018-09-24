from flask import jsonify, request

from . import api


@api.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_api():
    return jsonify({
        'result': True,
        'received_args': request.args or None,
        'received_headers': dict(request.headers) or None,
        'received_json': request.json or None
    })
