from api import api
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from api.serializers.vehicle_serializer import response_serializer

from schemas.admin_schema import SignedoutSchema
from ..models import Vehicle

from decorators.decorators import required_params


BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('service', type=str,
                     help=BLANK.format("service"))
_parser.add_argument('fee', type=str,
                     help=BLANK.format("fee"))


class SignedoutVehicles(Resource):

    @required_params(SignedoutSchema())
    def post(self):
        args = _parser.parse_args()
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
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


api.add_resource(SignedoutVehicles, "/signedout")
