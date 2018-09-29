from flask import g
from flask_httpauth import HTTPTokenAuth

from .errors import error_response
from ..models import User

token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)
