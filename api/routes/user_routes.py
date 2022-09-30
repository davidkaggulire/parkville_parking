from api import api
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response

from ..models import BlacklistToken, User

from api import db
from api import bcrypt, jwt


BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('email', type=str,
                     help=BLANK.format("email"))
_parser.add_argument('password', type=str,
                     help=BLANK.format("password"))


class RegisterAPI(Resource):
    """
    User Registration Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()

        print(post_data)
        print(post_data.get('email'))
        print(post_data.get('password'))

        # check if user already exists

        try:
            user = User.query.filter_by(email=post_data.get('email')).first()

            if not user:
                try:
                    user = User(
                        email=post_data.get('email'),
                        password=post_data.get('password')
                    )

                    # insert the user
                    db.session.add(user)
                    db.session.commit()
                    # generate the auth token
                    auth_token = user.encode_auth_token(user.id)

                    # print(auth_token)
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully registered.',
                        'auth_token': auth_token
                    }

                    print(responseObject)
                    return make_response(jsonify(responseObject), 201)
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status': 'fail',
                        'message': 'Some error occurred. Please try again.'
                    }
                    return make_response(jsonify(responseObject), 401)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return make_response(jsonify(responseObject), 202)
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


class LoginAPI(Resource):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
            ):
                # access_token = create_access_token(identity=user.id)
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token,
                        'expiresIn': 3600,
                        'email': user.email
                        # 'jti': access_token
                    }
                    return make_response(jsonify(responseObject), 200)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject), 404)
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject), 500)


class UserAPI(Resource):
    """
    User Resource
    """
    # @token_required
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            print(auth_token)
            resp = User.decode_auth_token(auth_token)
            print(resp)

            if resp == "Token blacklisted. Please log in again.":
                responseObject = {
                    'status': 'error',
                    'message': 'Token blacklisted. Please log in again.',
                }
                return make_response(jsonify(responseObject), 400)

            if resp == "Signature expired. Please log in again.":
                responseObject = {
                    'status': 'error',
                    'message': 'Signature expired. Please log in again.',
                }
                return make_response(jsonify(responseObject), 400)

            if resp == "Invalid token. Please log in again.":
                responseObject = {
                    'status': 'error',
                    'message': 'Invalid token. Please log in again.',
                }
                return make_response(jsonify(responseObject), 400)

            if isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return make_response(jsonify(responseObject), 200)
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject), 401)


class LogoutAPI(Resource):
    """
    Logout Resource
    """
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                # mark the token as blacklisted
                is_blacklisted_token = BlacklistToken.check_blacklist(
                                    auth_token)
                if is_blacklisted_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Token blacklisted already. Please log in again.'
                    }
                    return make_response(jsonify(responseObject), 200)
                else:
                    blacklist_token = BlacklistToken(token=auth_token)
                    try:
                        # insert the token
                        db.session.add(blacklist_token)
                        db.session.commit()
                        responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged out.'
                        }
                        return make_response(jsonify(responseObject), 200)
                    except Exception as e:
                        responseObject = {
                            'status': 'fail',
                            'message': e
                        }
                        return make_response(jsonify(responseObject), 200)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject), 403)


def check_blacklist(token):
    BlacklistToken.check_blacklist(token)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_database = check_blacklist(jti)
    return token_in_database is not None


api.add_resource(RegisterAPI, "/api/v1/auth/signup")
api.add_resource(LoginAPI, "/api/v1/auth/login")
api.add_resource(UserAPI, "/api/v1/auth/status")
api.add_resource(LogoutAPI, "/api/v1/auth/logout")
