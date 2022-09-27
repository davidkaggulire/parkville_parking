"""carschema.py"""

from marshmallow import Schema, fields, validate
import string


class CreateSchema(Schema):
    ALLOWED = string.ascii_letters
    PLATES = string.ascii_uppercase + string.digits
    NIN = string.ascii_uppercase + string.digits
    message_required = {"required": "Driver_name is required."}
    number_plate_required = {"required": "Number_plate is required."}
    letters_allowed = "only letters allowed"
    upper_case_name = "Name should start with upper case"
    driver_name = fields.String(required=True, error_messages=message_required,
                                validate=[
                                    validate.Length(min=1),
                                    validate.ContainsOnly(
                                        ALLOWED, error=letters_allowed),
                                    validate.Regexp(
                                        "^[A-Z]", error=upper_case_name)
                                ])
    number_plate = fields.String(required=True,
                                 error_messages=number_plate_required,
                                 validate=[
                                    validate.Length(
                                        equal=7,
                                        error="Number plate must \
                                            be of 7 characters"),
                                    validate.Regexp(
                                        "^[U]", error="Number plate should \
                                            start with capital U"),
                                    validate.ContainsOnly(
                                        PLATES,
                                        error="only letters and \
                                            numbers allowed, letters \
                                                should be capital")
                                    ])
    color = fields.String(required=True, error_messages={
                          "required": "Color is required."},
                          validate=validate.Length(min=1))
    model = fields.String(required=True, error_messages={
        "required": "Model is required."})
    phone_number = fields.String(required=True, error_messages={
                                 "required": "phone_number is required."})
    nin_number = fields.String(required=True, error_messages={
        "required": "NIN_number is required."}, validate=[
            validate.Length(equal=14,
                            error="NIN number must be 14 characters"),
            validate.ContainsOnly(NIN, error="Letters should be capital")])
    car_type = fields.String(required=True, error_messages={
        "required": "car_type is required."}, validate=validate.Length(min=1))
    gender = fields.String(required=True, validate=validate.OneOf(
        {"male", "female", "other"}), error_messages={
        "required": "gender is required."})


class SignoutSchema(Schema):
    vehicle_id = fields.String(required=True, error_messages={
        "required": "vehicle_id is required."}, validate=[
        validate.Length(equal=36)])
