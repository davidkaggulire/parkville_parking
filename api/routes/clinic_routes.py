from api import api
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from api.serializers.clinic_serializer import clinic_pay_serializer
from api.serializers.clinic_serializer import clinic_serializer
from api.serializers.clinic_serializer import clinic_pay_single_serializer
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

        print(request.args)
        page = request.args.get('page', 1, type=int)
        print(page)
        per_page = request.args.get('per_page', 5, type=int)

        services = Cartyreclinic.query.paginate(page=page, per_page=per_page)
        response = clinic_serializer(services)
        return response, 200
        # return [PersonDetails.serialize(record) for record in records]

    @jwt_required()
    @token_required
    @required_params(CarTyreClinicSchema())
    def post(self):
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
    @jwt_required()
    @token_required
    def get(self, service_id):
        return Cartyreclinic.serialize(
            Cartyreclinic.query.filter_by(id=service_id).first_or_404(
                description='Record with id={} is not available'.format(
                    service_id))), 200


class ClinicPaymentList(Resource):
    @jwt_required()
    @token_required
    def get(self):
        services = ClinicPayment.query.all()
        response = clinic_pay_serializer(services)
        return response, 200

    @jwt_required()
    @token_required
    @required_params(ClinicPaymentSchema())
    def post(self):
        # args = _parser.parse_args()
        data = request.get_json()

        vehicle_id = data["vehicle_id"]
        service_id = data["service_id"]

        ClinicPaymentSchema().validate(data)

        print(data)

        try:

            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description='Vehicle with id={} is not available'.format(
                    vehicle_id))
            try:
                payment = ClinicPayment.query.filter_by(
                    vehicle_id=vehicle_id, service_id=service_id).first_or_404(
                    description='Service with id={} and Vehicle with id={} is \
                        not available'.format(service_id, vehicle_id))
                print(f"{payment} exists")
                if payment:
                    message = {"message": "Clinic service paid for already"}
                    return make_response(jsonify(message), 400)
            except Exception:
                new_data = ClinicPayment(**data)
                db.session.add(new_data)
                db.session.commit()

                vehicle.clinic = True
                db.session.commit()
                print(data)

                payment = ClinicPayment.serialize(new_data)
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
    @jwt_required()
    @token_required
    def get(self, payment_id):
        return ClinicPayment.serialize(
            ClinicPayment.query.filter_by(id=payment_id).first_or_404(
                description='Record with id={} is not available'.format(
                    payment_id))), 200


api.add_resource(ClinicServiceList, "/api/v1/cartyreservices")
api.add_resource(ClinicServiceRecord, "/api/v1/cartyreservices/<service_id>")

api.add_resource(ClinicPaymentList, "/api/v1/clinicpayment")
api.add_resource(ClinicPaymentRecord, "/api/v1/clinicpayment/<payment_id>")
