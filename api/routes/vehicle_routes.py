"""vehicle_routes.py"""

import datetime
import json
import phonenumbers

from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required
from api import api
from api import db

from decorators.decorators import required_params, token_required
from schemas.carschema import CreateSchema, SignoutSchema

from ..models import Vehicle
from ..serializers.vehicle_serializer import response_serializer


BLANK = "'{}' cannot be blank"

_parser = reqparse.RequestParser()
_parser.add_argument('driver_name', type=str, help=BLANK.format("driver_name"))
_parser.add_argument('number_plate', type=str,
                     help=BLANK.format("number_plate"))
_parser.add_argument('color', type=str, help=BLANK.format("color"))
_parser.add_argument('model', type=str, help=BLANK.format("model"))
_parser.add_argument('date', type=str, help=BLANK.format("date"))
_parser.add_argument('phone_number', type=str,
                     help=BLANK.format("phone_number"))


class VehicleList(Resource):
    """
    vehicle list:
    """

    @jwt_required()
    @token_required
    def get(self):
        """return list of all vehicles"""
        print(request.args)
        page = request.args.get('page', 1, type=int)
        print(page)
        per_page = request.args.get('per_page', 5, type=int)

        persons = Vehicle.query.paginate(page=page, per_page=per_page)
        response = response_serializer(persons)
        return response, 200

    @jwt_required()
    @token_required
    @required_params(CreateSchema())
    def post(self):
        """register a new vehicle"""
        data = request.get_json()

        CreateSchema().validate(data)

        print(data)

        driver_name = data["driver_name"]
        number_plate = data["number_plate"]
        color = data["color"]
        model = data["model"]
        phone_number = data["phone_number"]

        # validate phone number
        try:
            my_number = phonenumbers.parse(phone_number)
            phonenumbers.is_valid_number(my_number)
        except phonenumbers.NumberParseException as e:
            hello = json.dumps(e, default=str)
            return make_response(jsonify({"error": hello}), 400)

        nin_number = data["nin_number"]

        car_type = data["car_type"]
        gender = data["gender"]

        try:
            user = Vehicle.query.filter_by(
                driver_name=driver_name, number_plate=number_plate,
                flag="admitted").first_or_404()

            if user:
                message = {
                    "status": "fail",
                    "message": "Car admitted already"
                }
                return make_response(jsonify(message), 400)
        except Exception:
            try:
                new_dict = {
                    "driver_name": driver_name,
                    "number_plate": number_plate,
                    "color": color,
                    "model": model,
                    "phone_number": phone_number,
                    "nin_number": nin_number,
                    "cartype_id": car_type,
                    'gender': gender,
                    'flag': "admitted"
                }

                new_data = Vehicle(**new_dict)

                # new_data = Vehicle(**data)
                db.session.add(new_data)
                db.session.commit()
                print(data)

                return Vehicle.serialize(new_data), 201
            except Exception as e:
                print(e)
                error = {
                    "status": "fail",
                    "error": str(e)
                }
                return make_response(jsonify(error), 400)


class VehicleRetrieve(Resource):
    """single vehicle retrieve handler"""
    @token_required
    @jwt_required()
    def get(self, vehicle_id):
        """retrieve single vehicle"""
        print(vehicle_id)
        return Vehicle.serialize(
            Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                        description=f'Record with id={vehicle_id} \
                            is unavailable')), 200


class SignOutVehicle(Resource):
    """signout vehicle handler"""

    @jwt_required()
    @token_required
    def get(self):
        """get all signed out cars"""
        print(request.args)
        page = request.args.get('page', 1, type=int)
        print(page)
        per_page = request.args.get('per_page', 5, type=int)
        vehicles = Vehicle.query.filter_by(flag="signed out").paginate(page=page, per_page=per_page)
        response = response_serializer(vehicles)
        return response, 200

    @jwt_required()
    @token_required
    @required_params(SignoutSchema())
    def post(self):
        """sign out car"""
        data = request.get_json()

        SignoutSchema().validate(data)

        print(data)

        vehicle_id = data["vehicle_id"]

        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description=f'Vehicle with id={vehicle_id} is not available')

            if vehicle.flag == "admitted":
                vehicle.flag = "signed out"
                vehicle.signed_out_at = datetime.datetime.now()
                vehicle.signed_out_date = datetime.datetime.now()
                db.session.commit()
                message = {"message": "Vehicle signed out successfully"}

                return make_response(jsonify(message), 200)
            else:
                message = {"message": "Vehicle signedout already"}
                return make_response(jsonify(message), 400)

        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)


api.add_resource(VehicleList, "/api/v1/vehicles")
api.add_resource(VehicleRetrieve, '/api/v1/vehicles/<vehicle_id>')

api.add_resource(SignOutVehicle, '/api/v1/vehicle/signout')
