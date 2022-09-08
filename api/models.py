# models

from email.policy import default
from enum import unique
from api import db
from datetime import datetime

import sqlalchemy.dialects.postgresql as postgresql
import uuid


class Charge(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_type = db.Column(db.String(80), nullable=False)
    day_charge = db.Column(db.String(80), nullable=False)
    night_charge = db.Column(db.String(80), nullable=False)
    hour_charge = db.Column(db.String(80), nullable=False)
    vehicle = db.relationship('Vehicle', backref='charge', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'day_charge': self.day_charge,
            'night_charge': self.night_charge,
            'hour_charge': self.hour_charge,
        }


class Vehicle(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4,
                   unique=True)
    driver_name = db.Column(db.String(80), nullable=False)
    number_plate = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    nin_number = db.Column(db.String(80), nullable=False)
    duration_type = db.Column(db.String(80),  nullable=False)
    charge_value = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(100), nullable=False, default="parked")
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    charge_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('charge.id'),
                          nullable=False)

    def __repr__(self) -> str:
        return self.driver_name

    def serialize(self):
        return {
            'id': self.id,
            'driver_name': self.driver_name,
            'number_plate': self.number_plate,
            'color': self.color,
            'model': self.model,
            'phone_number': self.phone_number,
            'nin_number': self.nin_number,
            'duration_type': self.duration_type,
            'charge_value': self.charge_value,
            'status': self.status,
            'created_at': self.created_at,
        }
