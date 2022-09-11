"""paymentschema.py"""

from marshmallow import Schema, fields, validate


class PaymentSchema(Schema):
    vehicle_id = fields.String(required=True, error_messages={"required": "Driver_name is required."}, validate=[
        validate.Length(equal=36)])
    charge_id = fields.String(required=True, error_messages={
        "required": "Color is required."}, validate=validate.Length(equal=36))
