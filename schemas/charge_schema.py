"""charge_schema.py"""

from marshmallow import Schema, fields, validate
import string


class ChargeSchema(Schema):
    ALLOWED = string.ascii_letters
    duration = fields.String(required=True, error_messages={
                                 "required": "Duration is required."}, validate=[
        validate.Length(min=1)])

    charge = fields.Integer(required=True, error_messages={
        "required": "Charge is required."})
