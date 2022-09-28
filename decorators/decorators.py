"""decorators.py"""

from marshmallow import ValidationError
from functools import wraps
from flask import jsonify, request, make_response
from api.models import User


def required_params(schema):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "status": "error",
                    "messages": err.messages
                }
                return make_response(jsonify(error), 403)
            return fn(*args, **kwargs)

        return wrapper
    return decorator


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = User.decode_auth_token(token)
            print(data)
            if data == "Signature expired. Please log in again.":
                message = {
                    'message': 'Signature expired. Please log in again.'
                }
                return jsonify(message)
            if data == "Token blacklisted. Please log in again.":
                message = {
                    'message': 'Token blacklisted. Please log in again.'
                }
                return jsonify(message)
            print("hello")
            current_user = User.query.filter_by(id=data).first()
            print(current_user)
        except Exception:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator
