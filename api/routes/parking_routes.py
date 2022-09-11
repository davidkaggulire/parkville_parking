from api import api, db
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response

from api.models import Bodacharge, Carcharge, Coastercharge, PaymentBodaboda, PaymentCar, PaymentCoaster, PaymentTaxi, PaymentTruck, Taxicharge, Truckcharge, Vehicle
from api.serializers.parking_serializer import boda_parking_serializer, car_parking_serializer, coaster_parking_serializer, taxi_parking_serializer, truck_parking_serializer
from schemas.payment_schema import PaymentSchema
from ..serializers.charge_serializer import boda_serializer, car_serializer, coaster_serializer, taxi_serializer, truck_serializer

from decorators.decorators import required_params

BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('duration', type=str,
                     help=BLANK.format("duration"))
_parser.add_argument('charge', type=str,
                     help=BLANK.format("charge"))


class CarPaymentList(Resource):
    def get(self):
        # return "Hellow world", 200
        payments = PaymentCar.query.all()
        response = car_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(PaymentSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data['vehicle_id']

        PaymentSchema().validate(data)
        try:
            new_data = PaymentCar(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            # update parking_flag to True - to know element updated.
            vehicle = Vehicle.query.filter_by(id=vehicle_id)\
                .first_or_404(description='Record with id={} is not available'.format(vehicle_id))

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
    def get(self, payment_id):
        return PaymentCar.serialize(
            PaymentCar.query.filter_by(id=payment_id)
            .first_or_404(description='Record with id={} is not available'.format(payment_id))), 200


class CoasterPaymentList(Resource):
    def get(self):
        # return "Hellow world", 200
        payments = PaymentCoaster.query.all()
        response = coaster_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(PaymentSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data['vehicle_id']

        PaymentSchema().validate(data)

        try:
            new_data = PaymentCoaster(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle = Vehicle.query.filter_by(id=vehicle_id)\
                .first_or_404(description='Record with id={} is not available'.format(vehicle_id))

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
    def get(self, payment_id):
        return PaymentCoaster.serialize(
            PaymentCoaster.query.filter_by(id=payment_id)
            .first_or_404(description='Record with id={} is not available'.format(payment_id))), 200


class TruckPaymentList(Resource):
    def get(self):
        # return "Hellow world", 200
        payments = PaymentTruck.query.all()
        response = truck_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(PaymentSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data['vehicle_id']

        PaymentSchema().validate(data)

        try:
            new_data = PaymentTruck(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle = Vehicle.query.filter_by(id=vehicle_id)\
                .first_or_404(description='Record with id={} is not available'.format(vehicle_id))

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
    def get(self, payment_id):
        return PaymentTruck.serialize(
            PaymentTruck.query.filter_by(id=payment_id)
            .first_or_404(description='Record with id={} is not available'.format(payment_id))), 200


class TaxiPaymentList(Resource):
    def get(self):
        # return "Hellow world", 200
        payments = PaymentTaxi.query.all()
        response = taxi_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(PaymentSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data["vehicle_id"]

        PaymentSchema().validate(data)

        try:
            new_data = PaymentTaxi(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle = Vehicle.query.filter_by(id=vehicle_id)\
                .first_or_404(description='Record with id={} is not available'.format(vehicle_id))

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
    def get(self, payment_id):
        return PaymentTaxi.serialize(
            PaymentTaxi.query.filter_by(id=payment_id)
            .first_or_404(description='Record with id={} is not available'.format(payment_id))), 200


class BodaPaymentList(Resource):
    def get(self):
        # return "Hellow world", 200
        payments = PaymentBodaboda.query.all()
        response = boda_parking_serializer(payments)
        return response, 200
        # return [Charge.serialize(charge) for charge in charges], 200

    @required_params(PaymentSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data["vehicle_id"]

        PaymentSchema().validate(data)

        try:
            new_data = Bodacharge(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle = Vehicle.query.filter_by(id=vehicle_id)\
                .first_or_404(description='Record with id={} is not available'.format(vehicle_id))

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
    def get(self, payment_id):
        return Bodacharge.serialize(
            Bodacharge.query.filter_by(id=payment_id)
            .first_or_404(description='Record with id={} is not available'.format(payment_id))), 200


api.add_resource(TruckPaymentList, "/truckpayments")
api.add_resource(TruckPaymentRecord, "/truckpayments/<payment_id>")

api.add_resource(CoasterPaymentList, "/coasterpayments")
api.add_resource(CoasterPaymentRecord, "/coasterpayments/<payment_id>")

api.add_resource(CarPaymentList, "/carpayments")
api.add_resource(CarPaymentRecord, "/carpayments/<payment_id>")

api.add_resource(TaxiPaymentList, "/taxipayments")
api.add_resource(TaxiPaymentRecord, "/taxipayments/<payment_id>")

api.add_resource(BodaPaymentList, "/bodapayments")
api.add_resource(BodaPaymentRecord, "/bodapayments/<payment_id>")
