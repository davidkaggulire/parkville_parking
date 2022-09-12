# models

from enum import unique
from api import db
from datetime import datetime

import sqlalchemy.dialects.postgresql as postgresql
import uuid


class Cartype(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    type = db.Column(db.String(80), unique=True, nullable=False)
    vehicle = db.relationship('Vehicle', backref='cartype', lazy=True)


class Truckcharge(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Taxicharge(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Coastercharge(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Carcharge(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Bodacharge(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
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
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    gender = db.Column(db.Enum('male', 'female', 'other', name='varchar'))
    flag = db.Column(db.String(80), nullable=False, default="admitted")
    parking = db.Column(db.Boolean, default=False, nullable=False)
    battery = db.Column(db.Boolean, default=False, nullable=False)
    clinic = db.Column(db.Boolean, default=False, nullable=False)
    cartype_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('cartype.id'),
                           nullable=False)
    clinicpayment = db.relationship(
        'ClinicPayment', backref='vehicle', lazy=True)
    batterypayment = db.relationship(
        'BatteryPayment', backref='vehicle', lazy=True)

    def __repr__(self) -> str:
        return self.driver_name

    def serialize(self):
        car_type = Cartype.query.filter_by(id=self.cartype_id).first_or_404(
            description='Record with id={} is not available'.format(self.cartype_id))

        return {
            'id': str(self.id),
            'driver_name': self.driver_name,
            'number_plate': self.number_plate,
            'color': self.color,
            'model': self.model,
            'phone_number': self.phone_number,
            'nin_number': self.nin_number,
            'created_at': str(self.created_at),
            'gender': self.gender,
            'car_type': car_type.type,
            'battery': self.battery,
            'parking': self.parking,
            'clinic': self.clinic
        }


class PaymentCar(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('vehicle.id'),
                           nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('carcharge.id'),
                          nullable=False)


class PaymentTruck(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('vehicle.id'),
                           nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('truckcharge.id'),
                          nullable=False)


class PaymentTaxi(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('vehicle.id'),
                           nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('taxicharge.id'),
                          nullable=False)


class PaymentCoaster(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('vehicle.id'),
                           nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('coastercharge.id'),
                          nullable=False)


class PaymentBodaboda(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('vehicle.id'),
                           nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('bodacharge.id'),
                          nullable=False)


class Cartyreclinic(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    service = db.Column(db.String(120), unique=True, nullable=False)
    fee = db.Column(db.String(80), nullable=False)
    clinicpayment = db.relationship(
        'ClinicPayment', backref='car_tyre_clinic', lazy=True)

    def serialize(self):
        return {
            'id': str(self.id),
            'service': self.service,
            'fee': self.fee,
        }


class ClinicPayment(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    service_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('cartyreclinic.id'),
                           nullable=False)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('vehicle.id'),
                           nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'service_id': str(self.service_id),
            'vehicle_id': str(self.vehicle_id),
        }


class Batterysection(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    battery_size = db.Column(db.String(120), unique=True, nullable=False)
    batterypayment = db.relationship(
        'BatteryPayment', backref='batterysection', lazy=True)

    def serialize(self):
        return {
            'id': str(self.id),
            'battery_size': self.battery_size,
        }


class BatteryPayment(db.Model):
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    battery_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('batterysection.id'),
                           nullable=False)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True), db.ForeignKey('vehicle.id'),
                           nullable=False)
    fee = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'battery_id': str(self.battery_id),
            'vehicle_id': str(self.vehicle_id),
            'fee': self.fee
        }
