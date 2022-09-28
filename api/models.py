"""models.py"""
import uuid

from datetime import datetime, timedelta
import sqlalchemy.dialects.postgresql as postgresql
import jwt

from api import db
from api import bcrypt
from api import app


class Cartype(db.Model):
    """car types"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    type = db.Column(db.String(80), unique=True, nullable=False)
    vehicle = db.relationship('Vehicle', backref='cartype', lazy=True)


class Truckcharge(db.Model):
    """charges for trucks"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        """serialize method"""
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Taxicharge(db.Model):
    """charges for taxis"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        """serialize method"""
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Coastercharge(db.Model):
    """charges for coasters"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        """serialize method"""
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Carcharge(db.Model):
    """charges for cars"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        """serialize method"""
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Bodacharge(db.Model):
    """charges for boda"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    charge = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(80), unique=True, nullable=False)

    def serialize(self):
        """serialize method"""
        return {
            'id': str(self.id),
            'charge': self.charge,
            'duration': self.duration,
        }


class Vehicle(db.Model):
    """vehicle class"""
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
    signed_out_at = db.Column(db.DateTime, nullable=True)
    signed_out_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.Enum('male', 'female', 'other', name='varchar'))
    flag = db.Column(db.String(80), nullable=False, default="admitted")
    parking = db.Column(db.Boolean, default=False, nullable=False)
    battery = db.Column(db.Boolean, default=False, nullable=False)
    clinic = db.Column(db.Boolean, default=False, nullable=False)
    cartype_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('cartype.id'), nullable=False)
    clinicpayment = db.relationship(
        'ClinicPayment', backref='vehicle', lazy=True)
    batterypayment = db.relationship(
        'BatteryPayment', backref='vehicle', lazy=True)

    def __repr__(self) -> str:
        return self.driver_name

    def serialize(self):
        """serialize method"""
        car_type = Cartype.query.filter_by(id=self.cartype_id).first_or_404(
            description=f'Record with id={self.cartype_id} is not available')

        return {
            'id': str(self.id),
            'driver_name': self.driver_name,
            'number_plate': self.number_plate,
            'color': self.color,
            'model': self.model,
            'phone_number': self.phone_number,
            'nin_number': self.nin_number,
            'created_at': str(self.created_at),
            'signed_out_at': str(self.signed_out_at),
            'signed_out_date': str(self.signed_out_date),
            'gender': self.gender,
            'car_type': car_type.type,
            'battery': self.battery,
            'parking': self.parking,
            'clinic': self.clinic
        }


class PaymentCar(db.Model):
    """payment for cars"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('vehicle.id'), nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True),
                          db.ForeignKey('carcharge.id'), nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    paid_date = db.Column(db.Date, nullable=False,
                          default=datetime.now)


class PaymentTruck(db.Model):
    """payment for trucks"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('vehicle.id'), nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True),
                          db.ForeignKey('truckcharge.id'), nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    paid_date = db.Column(db.Date, nullable=False,
                          default=datetime.now)


class PaymentTaxi(db.Model):
    """payment for taxis"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('vehicle.id'), nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True),
                          db.ForeignKey('taxicharge.id'), nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    paid_date = db.Column(db.Date, nullable=False,
                          default=datetime.now)


class PaymentCoaster(db.Model):
    """payment for coasters"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('vehicle.id'), nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True),
                          db.ForeignKey('coastercharge.id'), nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    paid_date = db.Column(db.Date, nullable=False,
                          default=datetime.now)


class PaymentBodaboda(db.Model):
    """payment for bodas"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('vehicle.id'), nullable=False)
    charge_id = db.Column(postgresql.UUID(as_uuid=True),
                          db.ForeignKey('bodacharge.id'), nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    paid_date = db.Column(db.Date, nullable=False,
                          default=datetime.now)


class Cartyreclinic(db.Model):
    """services in car clinic"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    service = db.Column(db.String(120), unique=True, nullable=False)
    fee = db.Column(db.String(80), nullable=False)
    clinicpayment = db.relationship(
        'ClinicPayment', backref='car_tyre_clinic', lazy=True)

    def serialize(self):
        """serialize method"""
        return {
            'id': str(self.id),
            'service': self.service,
            'fee': self.fee,
        }


class ClinicPayment(db.Model):
    """payment for services in car clinic"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    service_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('cartyreclinic.id'), nullable=False)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('vehicle.id'), nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    paid_date = db.Column(db.Date, nullable=False,
                          default=datetime.now)

    def serialize(self):
        """serialize methods"""
        return {
            'id': str(self.id),
            'service_id': str(self.service_id),
            'vehicle_id': str(self.vehicle_id),
            'paid_at': str(self.paid_at),
            'paid_date': str(self.paid_date)
        }


class Batterysection(db.Model):
    """battery sizes"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    battery_size = db.Column(db.String(120), unique=True, nullable=False)
    batterypayment = db.relationship(
        'BatteryPayment', backref='batterysection', lazy=True)

    def serialize(self):
        """serialize"""
        return {
            'id': str(self.id),
            'battery_size': self.battery_size,
        }


class BatteryPayment(db.Model):
    """payment for batteries"""
    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    battery_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('batterysection.id'), nullable=False)
    vehicle_id = db.Column(postgresql.UUID(as_uuid=True),
                           db.ForeignKey('vehicle.id'), nullable=False)
    fee = db.Column(db.String(80), nullable=False)

    paid_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    paid_date = db.Column(db.Date, nullable=False,
                          default=datetime.now)

    def serialize(self):
        """serialize method"""
        return {
            'id': str(self.id),
            'battery_id': str(self.battery_id),
            'vehicle_id': str(self.vehicle_id),
            'fee': self.fee,
            'paid_at': str(self.paid_at),
            'paid_date': str(self.paid_date)
        }


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(postgresql.UUID(as_uuid=True),
                   primary_key=True, default=uuid.uuid4, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

        self.registered_on = datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=0, seconds=5),
                'iat': datetime.now(),
                'sub': str(user_id)
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config["SECRET_KEY"],
                                 algorithms=["HS256"])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return f'<id: token: {self.token}'

    @staticmethod
    def check_blacklist(auth_token):
        """check token if in blacklist"""
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        return False
