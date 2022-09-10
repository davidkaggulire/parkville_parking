from api import api, db
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response

from api.models import Bodacharge, Carcharge, Coastercharge, Taxicharge, Truckcharge
from ..serializers.charge_serializer import boda_serializer, car_serializer, coaster_serializer, taxi_serializer, truck_serializer

from schemas.charge_schema import ChargeSchema
from decorators.decorators import required_params

BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('duration', type=str,
                     help=BLANK.format("duration"))
_parser.add_argument('charge', type=str,
                     help=BLANK.format("charge"))


class TruckChargeList(Resource):
    def get(self):
        # return "Hellow world", 200
        charges = Truckcharge.query.all()
        response = truck_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(ChargeSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        ChargeSchema().validate(data)
        try:
            new_data = Truckcharge(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            message = {
                "status": "success",
                "message": "Charge saved successfully",
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


class CoasterChargeList(Resource):
    def get(self):
        # return "Hellow world", 200
        charges = Coastercharge.query.all()
        response = coaster_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(ChargeSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        ChargeSchema().validate(data)

        try:
            new_data = Coastercharge(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            message = {
                "status": "success",
                "message": "Charge saved successfully",
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


class CarChargeList(Resource):
    def get(self):
        # return "Hellow world", 200
        charges = Carcharge.query.all()
        response = car_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(ChargeSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        ChargeSchema().validate(data)

        try:
            new_data = Carcharge(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            message = {
                "status": "success",
                "message": "Charge saved successfully",
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


class TaxiChargeList(Resource):
    def get(self):
        # return "Hellow world", 200
        charges = Taxicharge.query.all()
        response = taxi_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(ChargeSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        ChargeSchema().validate(data)

        try:
            new_data = Taxicharge(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            message = {
                "status": "success",
                "message": "Charge saved successfully",
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


class BodaChargeList(Resource):
    def get(self):
        # return "Hellow world", 200
        charges = Bodacharge.query.all()
        response = boda_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(ChargeSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        ChargeSchema().validate(data)

        try:
            new_data = Bodacharge(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            message = {
                "status": "success",
                "message": "Charge saved successfully",
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


api.add_resource(TruckChargeList, "/truckcharges")
api.add_resource(CoasterChargeList, "/coastercharges")
api.add_resource(CarChargeList, "/carcharges")
api.add_resource(TaxiChargeList, "/taxicharges")
api.add_resource(BodaChargeList, "/bodacharges")
