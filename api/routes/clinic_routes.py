from lib2to3.pgen2.tokenize import TokenError
from api import api
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from api.serializers.clinic_serializer import clinic_pay_serializer, clinic_pay_single_serializer, clinic_serializer
from schemas.clinic_schema import CarTyreClinicSchema, ClinicPaymentSchema
from ..models import Cartyreclinic, ClinicPayment, Vehicle

from decorators.decorators import required_params, token_required
from api import db
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required



BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('service', type=str,
                     help=BLANK.format("service"))
_parser.add_argument('fee', type=str,
                     help=BLANK.format("fee"))


class ClinicServiceList(Resource):
    # method_decorators = {'get': [token_required]}
    
    @jwt_required()
    @token_required
    def get(self):
        current_identity = get_jwt_identity()
        print("this is the current identity")
        print(current_identity)
        services = Cartyreclinic.query.all()
        response = clinic_serializer(services)
        return response, 200
        # return [PersonDetails.serialize(record) for record in records]

    @required_params(CarTyreClinicSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        CarTyreClinicSchema().validate(data)

        print(data)

        try:
            new_data = Cartyreclinic(**data)

            db.session.add(new_data)
            db.session.commit()
            print(data)

            return Cartyreclinic.serialize(new_data), 201
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


class ClinicServiceRecord(Resource):
    def get(self, service_id):
        return Cartyreclinic.serialize(
            Cartyreclinic.query.filter_by(id=service_id)
            .first_or_404(description='Record with id={} is not available'.format(service_id))), 200


class ClinicPaymentList(Resource):
    def get(self):
        services = ClinicPayment.query.all()
        response = clinic_pay_serializer(services)
        return response, 200

    @required_params(ClinicPaymentSchema())
    def post(self):
        # args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data["vehicle_id"]
        service_id = data["service_id"]

        ClinicPaymentSchema().validate(data)

        print(data)

        try:

            vehicle = Vehicle.query.filter_by(id=vehicle_id)\
                .first_or_404(description='Vehicle with id={} is not available'.format(vehicle_id))
            try: 
                payment = ClinicPayment.query.filter_by(vehicle_id=vehicle_id, service_id=service_id)\
                    .first_or_404(description='Service with id={} and Vehicle with id={} is not available'.format(service_id, vehicle_id))
                print(f"{payment} exists")
                # if paid, return paid already otherwise convert vehicle.clinic = true
                if  payment:
                    return make_response(jsonify({"message": "Clinic service paid for already"}), 400)
            except Exception as e:
                new_data = ClinicPayment(**data)
                db.session.add(new_data)
                db.session.commit()

                vehicle.clinic = True
                db.session.commit()
                print(data)

                payment =  ClinicPayment.serialize(new_data)
                print(payment)
                response = clinic_pay_single_serializer(payment)
                return response, 201
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


class ClinicPaymentRecord(Resource):
    def get(self, payment_id):
        return ClinicPayment.serialize(
            ClinicPayment.query.filter_by(id=payment_id)
            .first_or_404(description='Record with id={} is not available'.format(payment_id))), 200


api.add_resource(ClinicServiceList, "/cartyreservices")
api.add_resource(ClinicServiceRecord, "/cartyreservices/<service_id>")

api.add_resource(ClinicPaymentList, "/clinicpayment")
api.add_resource(ClinicPaymentRecord, "/clinicpayment/<payment_id>")
