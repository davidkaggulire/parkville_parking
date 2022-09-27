"""charge_schema.py"""

from marshmallow import Schema, fields, validate


class BatterySectionSchema(Schema):
    battery_size = fields.String(required=True, error_messages={
        "required": "Battery_size is required."}, validate=[
        validate.Length(min=3)])


class BatteryPaymentSchema(Schema):
    """schema for payment"""
    battery_id = fields.String(required=True, error_messages={
        "required": "battery_id is required."}, validate=[
        validate.Length(equal=36)])
    vehicle_id = fields.String(required=True, error_messages={
        "required": "Vehicle_id is required."}, validate=[
        validate.Length(equal=36)])
    fee = fields.Integer(required=True, error_messages={
        "required": "Fee is required."})
