"""charge_schema.py"""

from marshmallow import Schema, fields, validate
import string


class ChargeSchema(Schema):
    ALLOWED = string.ascii_letters
    CHARGE = string.digits
    vehicle_type = fields.String(required=True, error_messages={
                                 "required": "Vehicle_type is required."}, validate=[
        validate.Length(min=1), validate.ContainsOnly(ALLOWED, error="only letters allowed")])

    day_charge = fields.Integer(required=True, error_messages={
        "required": "Day_charge is required."})
    night_charge = fields.Integer(required=True, error_messages={
        "required": "Day_charge is required."})
    hour_charge = fields.Integer(required=True, error_messages={
        "required": "Day_charge is required."})
