from api import api
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response

from schemas.duration_schema import DurationSchema
from ..models import Charge, Duration
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


class ClinicList(Resource):
    def get(self):
        # return "Hellow world", 200
        persons = Duration.query.all()
        response = response_serializer(persons)
        return response, 200
        # return [PersonDetails.serialize(record) for record in records]

    @required_params(DurationSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()

        DurationSchema().validate(data)

        print(data)

        try:
            duration = data["duration"]
            number_plate = data["number_plate"]
            color = data["color"]
            model = data["model"]
            phone_number = data["phone_number"]

            nin_number = data["nin_number"]
            duration_type = data["duration_type"]

            charge_value = data["charge_value"]
            vehicle_type = data["vehicle_type"]
            gender = data["gender"]

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
                'gender': gender
            }

            new_data = Vehicle(**new_dict)

            # new_data = Vehicle(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            return Vehicle.serialize(new_data), 201
        except Exception as e:
            print(e)
            return jsonify()


api.add_resource(DurationList, "/duration")
