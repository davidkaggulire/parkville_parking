"""charge_schema.py"""

from marshmallow import Schema, fields, validate
import string


class CarTyreClinicSchema(Schema):
    ALLOWED = string.ascii_letters
    service = fields.String(required=True, error_messages={
        "required": "Service is required."}, validate=[
        validate.Length(min=3)])
    fee = fields.Integer(required=True, error_messages={
        "required": "Fee is required."})


class CarTypeSchema(Schema):
    ALLOWED = string.ascii_letters
    type = fields.String(required=True, error_messages={
        "required": "car type is required."}, validate=[
        validate.Length(min=3), validate.ContainsOnly(ALLOWED, error="only letters allowed")])


class ClinicPaymentSchema(Schema):
    """schema for payment"""
    service_id = fields.String(required=True, error_messages={
        "required": "Service is required."}, validate=[
        validate.Length(equal=36)])
    vehicle_id = fields.String(required=True, error_messages={
        "required": "vehicle_id is required."}, validate=[
        validate.Length(equal=36)])
