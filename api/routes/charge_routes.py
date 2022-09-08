from api import api, db
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from ..models import Charge, Vehicle
from ..serializers.charge_serializer import response_serializer

from schemas.charge_schema import ChargeSchema
from decorators.decorators import required_params

BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('vehicle_type', type=str,
                     help=BLANK.format("vehicle_type"))
_parser.add_argument('day_charge', type=str,
                     help=BLANK.format("day_charge"))
_parser.add_argument('night_charge', type=str,
                     help=BLANK.format("night_charge"))
_parser.add_argument('hour_charge', type=str,
                     help=BLANK.format("hour_charge"))


class ChargeList(Resource):
    def get(self):
        # return "Hellow world", 200
        charges = Charge.query.all()
        response = response_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(ChargeSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        ChargeSchema().validate(data)

        new_data = Charge(**data)
        db.session.add(new_data)
        db.session.commit()
        print(data)
        return data, 201

        

api.add_resource(ChargeList, "/charges")