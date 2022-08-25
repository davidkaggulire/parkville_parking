"""decorators.py"""

from flask import jsonify, request
from marshmallow import ValidationError
from functools import wraps
from flask import jsonify,request, make_response


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