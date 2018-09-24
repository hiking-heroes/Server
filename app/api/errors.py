from flask import jsonify
from app.exceptions import ValidationError
from . import api


errors = {
    400: 'bad request',
    401: 'unauthorized',
    403: 'forbidden',
    404: 'not found',
    409: 'conflict',
    500: 'internal server error'
}


def abort_json(code: int, message: str):
    response = jsonify({
        'error': errors.get(code, 'unexpected error'),
        'message': message
    })
    response.status_code = code
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return abort_json(400, e.args[0])
