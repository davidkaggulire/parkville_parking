from api import api
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from ..models import Charge, Vehicle
from ..serializers.vehicle_serializer import response_serializer

from schemas.carschema import CreateSchema
from decorators.decorators import required_params
from api import db

import json
import phonenumbers

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
    def get(self):
        # return "Hellow world", 200
        persons = Vehicle.query.all()
        response = response_serializer(persons)
        return response, 200
        # return [PersonDetails.serialize(record) for record in records]

    @required_params(CreateSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        CreateSchema().validate(data)

        print(data)

        try:

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
            duration_type = data["duration_type"]

            charge_value = data["charge_value"]
            vehicle_type = data["vehicle_type"]

            vehicle = Charge.query.filter_by(id=vehicle_type).first_or_404(description='Record with id={} is not available'.format(vehicle_type))

            print(vehicle.night_charge)

            if duration_type == "day":
                charge_value = vehicle.day_charge
            elif duration_type == "night":
                charge_value = vehicle.night_charge
            elif duration_type == "less than 3 hours":
                charge_value = vehicle.hour_charge

            print(charge_value)

            new_dict = {
                "driver_name": driver_name,
                "number_plate": number_plate,
                "color": color,
                "model": model,
                "phone_number": phone_number,
                "nin_number": nin_number,
                "duration_type": duration_type,
                "charge_value": charge_value,
                "charge_id": vehicle_type,
            }

            new_data = Vehicle(**new_dict)

            # new_data = Vehicle(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            output = {
                "driver_name": driver_name,
                "number_plate": number_plate,
                "color": color,
                "model": model,
                "phone_number": phone_number,
                "nin_number": nin_number,
                "duration_type": duration_type,
                "charge_value": charge_value,
                "vehicle_type": vehicle.vehicle_type,
            }

            message = {
                "status": "success",
                "message": "Vehicle registered successfully",
                "vehicle": output
            }
            return make_response(jsonify(message), 201)
        except Exception as e:
            print(e)
            return jsonify()




api.add_resource(VehicleList, "/vehicle")
