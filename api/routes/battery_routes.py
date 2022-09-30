"""battery routes"""
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required

from decorators.decorators import required_params, token_required
from api.serializers.battery_serializer import battery_list_payment_serializer
from api.serializers.battery_serializer import battery_section_list_serializer
from api.serializers.battery_serializer import battery_single_payment_serializer
from schemas.battery_schema import BatteryPaymentSchema, BatterySectionSchema
from api import api
from api import db
from ..models import BatteryPayment, Batterysection, Vehicle


BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('service', type=str,
                     help=BLANK.format("service"))
_parser.add_argument('fee', type=str,
                     help=BLANK.format("fee"))


class BatterySectionList(Resource):
    """battery section list"""
    @jwt_required()
    @token_required
    def get(self):
        """get battery services"""
        services = Batterysection.query.all()
        response = battery_section_list_serializer(services)
        return response, 200
        # return [PersonDetails.serialize(record) for record in records]

    @jwt_required()
    @token_required
    @required_params(BatterySectionSchema())
    def post(self):
        """post battery service"""
        data = request.get_json()

        BatterySectionSchema().validate(data)

        print(data)

        try:
            new_data = Batterysection(**data)

            db.session.add(new_data)
            db.session.commit()
            print(data)

            return Batterysection.serialize(new_data), 201
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


class BatterySectionRecord(Resource):
    """battery section"""

    @jwt_required()
    @token_required
    def get(self, battery_id):
        """serialize"""
        return Batterysection.serialize(
            Batterysection.query.filter_by(id=battery_id).first_or_404(
                description=f'Record with id={battery_id} is \
                    not available')), 200


class BatteryPaymentList(Resource):
    """list payments battery"""

    @jwt_required()
    @token_required
    def get(self):
        """get all payments"""
        services = BatteryPayment.query.all()
        response = battery_list_payment_serializer(services)
        return response, 200

    @jwt_required()
    @token_required
    @required_params(BatteryPaymentSchema())
    def post(self):
        """post battery payment"""
        data = request.get_json()

        vehicle_id = data["vehicle_id"]
        battery_id = data["battery_id"]

        BatteryPaymentSchema().validate(data)

        print(data)

        try:

            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description=f'Vehicle with id={vehicle_id} is not available')
            try:
                payment = BatteryPayment.query.filter_by(
                    vehicle_id=vehicle_id, battery_id=battery_id).first_or_404(
                    description=f'Service with id={battery_id} \
                        and Vehicle with id={vehicle_id} \
                        is not available')
                print(f"{payment} exists")

                if payment:
                    message = {"message": "Battery size paid for already"}
                    return make_response(jsonify(message), 400)
            except Exception:
                new_data = BatteryPayment(**data)
                db.session.add(new_data)
                db.session.commit()

                vehicle.battery = True
                db.session.commit()
                print(data)

                payment = BatteryPayment.serialize(new_data)
                print(payment)
                response = battery_single_payment_serializer(payment)

                return response, 201
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


class BatteryPaymentRecord(Resource):
    """battery payment record"""

    @jwt_required()
    @token_required
    def get(self, payment_id):
        """return single battery payment"""
        return BatteryPayment.serialize(
            BatteryPayment.query.filter_by(id=payment_id).first_or_404(
                description=f'Record with id={payment_id} is \
                    not available')), 200


api.add_resource(BatterySectionList, "/api/v1/batteries")
api.add_resource(BatterySectionRecord, "/api/v1/batteries/<battery_id>")

api.add_resource(BatteryPaymentList, "/api/v1/batterypayments")
api.add_resource(BatteryPaymentRecord, "/api/v1/batterypayments/<payment_id>")
