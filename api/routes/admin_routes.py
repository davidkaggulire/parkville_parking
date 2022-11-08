"""admin_routes"""

from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required
from api.serializers.vehicle_serializer import response_serializer

from schemas.admin_schema import SignedoutSchema
from decorators.decorators import required_params, token_required

from api import api
from ..models import Vehicle


BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('service', type=str,
                     help=BLANK.format("service"))
_parser.add_argument('fee', type=str,
                     help=BLANK.format("fee"))


class SignedoutVehicles(Resource):
    """signed out vehicles"""

    @jwt_required()
    @token_required
    @required_params(SignedoutSchema())
    def post(self):
        """get signed out vehicles on specific date"""
        data = request.get_json()

        SignedoutSchema().validate(data)

        print(data)
        date = data["date"]

        try:
            vehicles = Vehicle.query.filter_by(signed_out_date=date)
            response = response_serializer(vehicles)
            return response, 200

        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": "No vehicles found"
            }
            return make_response(jsonify(error), 400)


class Home(Resource):
    def get(self):
        return 'Home Page Route'

api.add_resource(SignedoutVehicles, "/api/v1/signedout")
api.add_resource(Home, "/")
