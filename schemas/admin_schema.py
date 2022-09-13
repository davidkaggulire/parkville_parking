"""admin_schema.py"""

from marshmallow import Schema, fields


class SignedoutSchema(Schema):
    date = fields.Date(required=True, error_messages={
        "required": "Date is required."})
