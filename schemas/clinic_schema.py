"""charge_schema.py"""

from marshmallow import Schema, fields, validate
import string


class DurationSchema(Schema):
    ALLOWED = string.ascii_letters
    vehicle_type = fields.String(required=True, error_messages={
                                 "required": "Duration is required."}, validate=[
        validate.Length(min=3), validate.ContainsOnly(ALLOWED, error="only letters allowed")])


class CarTypeSchema(Schema):
    ALLOWED = string.ascii_letters
    type = fields.String(required=True, error_messages={
                                 "required": "car type is required."}, validate=[
        validate.Length(min=3), validate.ContainsOnly(ALLOWED, error="only letters allowed")])