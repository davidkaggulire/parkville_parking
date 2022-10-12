from api import api, db
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required

from api.models import Bodacharge, Carcharge, Coastercharge
from api.models import Truckcharge, Taxicharge
from ..serializers.charge_serializer import boda_serializer, car_serializer
from ..serializers.charge_serializer import taxi_serializer, truck_serializer
from ..serializers.charge_serializer import coaster_serializer
from schemas.charge_schema import ChargeSchema
from decorators.decorators import required_params, token_required

BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('duration', type=str,
                     help=BLANK.format("duration"))
_parser.add_argument('charge', type=str,
                     help=BLANK.format("charge"))


class TruckChargeList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        charges = Truckcharge.query.paginate(page=page, per_page=per_page)
        response = truck_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(ChargeSchema())
    def post(self):
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


class TruckChargeRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, charge_id):
        return Truckcharge.serialize(
            Truckcharge.query.filter_by(id=charge_id).first_or_404(
                description='Record with id={} is not available'.format(
                    charge_id))), 200


class CoasterChargeList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        charges = Coastercharge.query.paginate(page=page, per_page=per_page)
        response = coaster_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(ChargeSchema())
    def post(self):
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


class CoasterChargeRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, charge_id):
        return Coastercharge.serialize(
            Coastercharge.query.filter_by(id=charge_id).first_or_404(
                description='Record with id={} is not available'.format(
                    charge_id))), 200


class CarChargeList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        charges = Carcharge.query.paginate(page=page, per_page=per_page)
        response = car_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(ChargeSchema())
    def post(self):
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


class CarChargeRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, charge_id):
        return Carcharge.serialize(
            Carcharge.query.filter_by(id=charge_id).first_or_404(
                description='Record with id={} is not available'.format(
                    charge_id))), 200


class TaxiChargeList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        charges = Taxicharge.query.paginate(page=page, per_page=per_page)
        response = taxi_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(ChargeSchema())
    def post(self):
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


class TaxiChargeRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, charge_id):
        return Taxicharge.serialize(
            Taxicharge.query.filter_by(id=charge_id).first_or_404(
                description='Record with id={} is not available'.format(
                    charge_id))), 200


class BodaChargeList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        charges = Bodacharge.query.paginate(page=page, per_page=per_page)
        response = boda_serializer(charges)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(ChargeSchema())
    def post(self):
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


class BodaChargeRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, charge_id):
        return Bodacharge.serialize(
            Bodacharge.query.filter_by(id=charge_id).first_or_404(
                description='Record with id={} is not available'.format(
                    charge_id))), 200


api.add_resource(TruckChargeList, "/api/v1/truckcharges")
api.add_resource(TruckChargeRecord, "/api/v1/truckcharges/<charge_id>")

api.add_resource(CoasterChargeList, "/api/v1/coastercharges")
api.add_resource(CoasterChargeRecord, "/api/v1/coastercharges/<charge_id>")

api.add_resource(CarChargeList, "/api/v1/carcharges")
api.add_resource(CarChargeRecord, "/api/v1/carcharges/<charge_id>")

api.add_resource(TaxiChargeList, "/api/v1/taxicharges")
api.add_resource(TaxiChargeRecord, "/api/v1/taxicharges/<charge_id>")

api.add_resource(BodaChargeList, "/api/v1/bodacharges")
api.add_resource(BodaChargeRecord, "/api/v1/bodacharges/<charge_id>")
