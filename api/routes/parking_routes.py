from api import api, db
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required

from api.models import Bodacharge, PaymentBodaboda, PaymentCar, PaymentCoaster
from api.models import PaymentTaxi, PaymentTruck, Vehicle
from api.serializers.parking_serializer import boda_parking_serializer
from api.serializers.parking_serializer import car_parking_serializer
from api.serializers.parking_serializer import coaster_parking_serializer
from api.serializers.parking_serializer import taxi_parking_serializer
from api.serializers.parking_serializer import truck_parking_serializer
from schemas.payment_schema import PaymentSchema

from decorators.decorators import required_params, token_required

BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('duration', type=str,
                     help=BLANK.format("duration"))
_parser.add_argument('charge', type=str,
                     help=BLANK.format("charge"))


class CarPaymentList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        payments = PaymentCar.query.all()
        response = car_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(PaymentSchema())
    def post(self):
        data = request.get_json()

        vehicle_id = data['vehicle_id']

        PaymentSchema().validate(data)
        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description='Record with id={} is not available'.format(
                    vehicle_id))

            if vehicle.parking is True:
                return make_response(jsonify({"message": "Paid already"}), 400)

            new_data = PaymentCar(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            # update parking_flag to True - to know element updated.
            vehicle.parking = True
            db.session.commit()

            message = {
                "status": "success",
                "message": "Payment made successfully",
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


class CarPaymentRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, payment_id):
        return PaymentCar.serialize(
            PaymentCar.query.filter_by(id=payment_id).first_or_404(
                description='Record with id={} is not available'.format(
                    payment_id))), 200


class CoasterPaymentList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        payments = PaymentCoaster.query.all()
        response = coaster_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(PaymentSchema())
    def post(self):
        data = request.get_json()

        vehicle_id = data['vehicle_id']

        PaymentSchema().validate(data)

        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description='Record with id={} is not available'.format(
                    vehicle_id))

            if vehicle.parking is True:
                return make_response(jsonify({"message": "Paid already"}), 400)

            new_data = PaymentCoaster(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle.parking = True
            db.session.commit()

            message = {
                "status": "success",
                "message": "Payment made successfully",
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


class CoasterPaymentRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, payment_id):
        return PaymentCoaster.serialize(
            PaymentCoaster.query.filter_by(id=payment_id).first_or_404(
                description='Record with id={} is not available'.format(
                    payment_id))), 200


class TruckPaymentList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        payments = PaymentTruck.query.all()
        response = truck_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(PaymentSchema())
    def post(self):
        data = request.get_json()

        vehicle_id = data['vehicle_id']

        PaymentSchema().validate(data)

        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description='Record with id={} is not available'.format(
                    vehicle_id))

            if vehicle.parking is True:
                return make_response(jsonify({"message": "Paid already"}), 400)

            new_data = PaymentTruck(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle.parking = True
            db.session.commit()

            message = {
                "status": "success",
                "message": "Payment made successfully",
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


class TruckPaymentRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, payment_id):
        return PaymentTruck.serialize(
            PaymentTruck.query.filter_by(id=payment_id).first_or_404(
                description='Record with id={} is not available'.format(
                    payment_id))), 200


class TaxiPaymentList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        payments = PaymentTaxi.query.all()
        response = taxi_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(PaymentSchema())
    def post(self):
        data = request.get_json()

        vehicle_id = data["vehicle_id"]

        PaymentSchema().validate(data)

        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description='Record with id={} is not available'.format(
                    vehicle_id))

            if vehicle.parking is True:
                return make_response(jsonify({"message": "Paid already"}), 400)

            new_data = PaymentTaxi(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle.parking = True
            db.session.commit()

            message = {
                "status": "success",
                "message": "Payment made successfully",
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


class TaxiPaymentRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, payment_id):
        return PaymentTaxi.serialize(
            PaymentTaxi.query.filter_by(id=payment_id).first_or_404(
                description='Record with id={} is not available'.format(
                    payment_id))), 200


class BodaPaymentList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        # return "Hellow world", 200
        payments = PaymentBodaboda.query.all()
        response = boda_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @jwt_required()
    @token_required
    @required_params(PaymentSchema())
    def post(self):
        data = request.get_json()

        vehicle_id = data["vehicle_id"]

        PaymentSchema().validate(data)

        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description='Record with id={} is not available'.format(
                    vehicle_id))

            if vehicle.parking is True:
                return make_response(jsonify({"message": "Paid already"}), 400)

            new_data = Bodacharge(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle.parking = True
            db.session.commit()

            message = {
                "status": "success",
                "message": "Payment made successfully",
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


class BodaPaymentRecord(Resource):
    @jwt_required()
    @token_required
    def get(self, payment_id):
        return Bodacharge.serialize(
            Bodacharge.query.filter_by(id=payment_id).first_or_404(
                description='Record with id={} is not available'.format(
                    payment_id))), 200


api.add_resource(TruckPaymentList, "/api/v1/truckpayments")
api.add_resource(TruckPaymentRecord, "/api/v1/truckpayments/<payment_id>")

api.add_resource(CoasterPaymentList, "/api/v1/coasterpayments")
api.add_resource(CoasterPaymentRecord, "/api/v1/coasterpayments/<payment_id>")

api.add_resource(CarPaymentList, "/api/v1/carpayments")
api.add_resource(CarPaymentRecord, "/api/v1/carpayments/<payment_id>")

api.add_resource(TaxiPaymentList, "/api/v1/taxipayments")
api.add_resource(TaxiPaymentRecord, "/api/v1/taxipayments/<payment_id>")

api.add_resource(BodaPaymentList, "/api/v1/bodapayments")
api.add_resource(BodaPaymentRecord, "/api/v1/bodapayments/<payment_id>")
