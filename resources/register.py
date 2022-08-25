from email.policy import default
from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from models.model import PostgreSQLDatabase
import json
import datetime
from json import JSONEncoder

from schemas.carschema import CreateSchema
from decorators.decorators import required_params

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

class DateTimeEncoder(JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class RegisterCar(Resource):
    def get(self):
        return {'hello': 'parking'}

    @required_params(CreateSchema())
    def post(self):
        args = _parser.parse_args()
        data = request.get_json()
        print(data["nin_number"])

        CreateSchema().validate(data)

        driver_name = data["driver_name"]
        number_plate = data["number_plate"]
        color = data["color"]
        model = data["model"]
        phone_number = data["phone_number"]
        nin_number = data["nin_number"]
        duration_type = data["duration_type"]
        charge_value = data["charge_value"]
        vehicle_type = data["vehicle_type"]

        try:
            db = PostgreSQLDatabase()
            status = db.connect()
            created, vehicle_detail = db.create(driver_name,
                                                number_plate,
                                                color,
                                                model,
                                                phone_number,
                                                nin_number,
                                                duration_type,
                                                charge_value,
                                                vehicle_type)
            print(DateTimeEncoder().encode(vehicle_detail))
            vehicle_detail = json.dumps(vehicle_detail, indent=4, cls=DateTimeEncoder)

            if created:
                message = {
                    "status": "success",
                    "message": "Vehicle registered successfully",
                    "vehicle": json.loads(vehicle_detail)
                }
                return make_response(jsonify(message), 200)
            else:
                message = {
                    "status": "error",
                    "message": "failed to create vehicle",
                }
            return jsonify(message), 500
        except Exception as err:
            print(err)
