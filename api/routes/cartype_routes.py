from api import api, db
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response

from api.models import Cartype
from api.serializers.vehicle_serializer import car_type_serializer
from schemas.clinic_schema import CarTypeSchema
from flask_jwt_extended import jwt_required

from decorators.decorators import required_params, token_required

BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('duration', type=str,
                     help=BLANK.format("duration"))
_parser.add_argument('charge', type=str,
                     help=BLANK.format("charge"))


class CarTypeList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        charges = Cartype.query.all()
        response = car_type_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(CarTypeSchema())
    def post(self):
        data = request.get_json()

        CarTypeSchema().validate(data)
        try:
            new_data = Cartype(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            message = {
                "status": "success",
                "message": "Car type saved successfully",
                "vehicle": data
            }
            return make_response(jsonify(message), 201)
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


api.add_resource(CarTypeList, "/api/v1/cartypes")
