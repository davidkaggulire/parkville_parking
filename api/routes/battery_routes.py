from api import api
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from api.serializers.battery_serializer import battery_list_payment_serializer, battery_section_list_serializer, battery_single_payment_serializer
from api.serializers.clinic_serializer import clinic_pay_serializer, clinic_pay_single_serializer, clinic_serializer
from schemas.battery_schema import BatteryPaymentSchema, BatterySectionSchema
from ..models import BatteryPayment, Batterysection, Cartyreclinic, ClinicPayment, Vehicle

from decorators.decorators import required_params
from api import db


BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('service', type=str,
                     help=BLANK.format("service"))
_parser.add_argument('fee', type=str,
                     help=BLANK.format("fee"))


class BatterySectionList(Resource):
    def get(self):
        services = Batterysection.query.all()
        response = battery_section_list_serializer(services)
        return response, 200
        # return [PersonDetails.serialize(record) for record in records]

    @required_params(BatterySectionSchema())
    def post(self):
        args = _parser.parse_args()
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
    def get(self, battery_id):
        return Batterysection.serialize(
            Batterysection.query.filter_by(id=battery_id)
            .first_or_404(description='Record with id={} is not available'.format(battery_id))), 200


class BatteryPaymentList(Resource):
    def get(self):
        services = BatteryPayment.query.all()
        response = battery_list_payment_serializer(services)
        return response, 200

    @required_params(BatteryPaymentSchema())
    def post(self):
        # args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data["vehicle_id"]
        battery_id = data["battery_id"]

        BatteryPaymentSchema().validate(data)

        print(data)

        try:

            vehicle = Vehicle.query.filter_by(id=vehicle_id)\
                .first_or_404(description='Vehicle with id={} is not available'.format(vehicle_id))
            try: 
                payment = BatteryPayment.query.filter_by(vehicle_id=vehicle_id, battery_id=battery_id)\
                    .first_or_404(description='Service with id={} and Vehicle with id={} is not available'.format(battery_id, vehicle_id))
                print(f"{payment} exists")
                # if paid, return paid already otherwise convert vehicle.clinic = true
                if  payment:
                    return make_response(jsonify({"message": "Battery size paid for already"}), 400)
            except Exception as e:
                new_data = BatteryPayment(**data)
                db.session.add(new_data)
                db.session.commit()

                vehicle.battery = True
                db.session.commit()
                print(data)

                payment =  BatteryPayment.serialize(new_data)
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
    def get(self, payment_id):
        return BatteryPayment.serialize(
            BatteryPayment.query.filter_by(id=payment_id)
            .first_or_404(description='Record with id={} is not available'.format(payment_id))), 200


api.add_resource(BatterySectionList, "/batteries")
api.add_resource(BatterySectionRecord, "/batteries/<battery_id>")

api.add_resource(BatteryPaymentList, "/batterypayments")
api.add_resource(BatteryPaymentRecord, "/batterypayments/<payment_id>")
