from interfaces.db import IDatabase

import os
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from api import api, db
from api.models import Cartype
from api.serializers.vehicle_serializer import car_type_serializer

from api.models import Vehicle
from api.serializers.vehicle_serializer import response_serializer


load_dotenv()

class PostgreSQLDatabase(IDatabase):
    """postgresql database"""
    def __init__(self):
        pass
    __instance = None

    def connect(self):
        try:
            db_name = os.environ.get('DB_NAME')
            DB_USER = os.environ.get('DB_USER')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=DB_USER,
                password=DB_PASSWORD,
                host="localhost",
                port="5432"
            )
            print(self.conn)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            self.dict_cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print(f"Connected to {db_name}")
        except Exception:
            print("Connection to PostgreSQL failed")
        return True
    
    # CARS
    def create_car_type(self, data):
        """creates record that are saved into the database"""
        try:
            new_data = Cartype(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            return True, data
        except Exception as e:
            return False, e

    def read_car_type(self):
        """views record in database"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)
            charges = Cartype.query.paginate(page=page, per_page=per_page)
            response = car_type_serializer(charges)
            return True, response
        except Exception as e :
            return False, e
    
    def update_car_type(self):
        """updates record in database"""
        pass

    def delete_car_type(self):
        """deletes record from database"""
        pass

    # BATTERIES
    def create_batteries(self):
        """creates record that are saved into the database"""

    def read_batteries(self):
        """views record in database"""

    def update_batteries(self):
        """updates record in database"""

    def delete_batteries(self):
        """deletes record from database"""

    # VEHICLES
    def create_vehicle(self, data):
        """creates record that are saved into the database"""
        driver_name = data["driver_name"]
        number_plate = data["number_plate"]
        color = data["color"]
        model = data["model"]
        phone_number = data["phone_number"]
        nin_number = data["nin_number"]
        car_type = data["car_type"]
        gender = data["gender"]

        try:
            user = Vehicle.query.filter_by(
                driver_name=driver_name, number_plate=number_plate,
                flag="admitted").first_or_404()

            if user:
                message = {
                    "status": "fail",
                    "message": "Car admitted already"
                }
                return False, message
        except Exception:
            try:
                new_dict = {
                    "driver_name": driver_name,
                    "number_plate": number_plate,
                    "color": color,
                    "model": model,
                    "phone_number": phone_number,
                    "nin_number": nin_number,
                    "cartype_id": car_type,
                    'gender': gender,
                    'flag': "admitted"
                }

                new_data = Vehicle(**new_dict)

                # new_data = Vehicle(**data)
                db.session.add(new_data)
                db.session.commit()
                # print(data)

                return True, new_data
            except Exception as e:
                return False, e


    def read_vehicles(self):
        """views record in database"""
        try:
            print(request.args)
            page = request.args.get('page', 1, type=int)
            print(page)
            per_page = request.args.get('per_page', 5, type=int)

            persons = Vehicle.query.paginate(page=page, per_page=per_page)
            return True, persons
        except Exception as e:
            return False, e
    
    def get_vehicle(self, id):
        print(id)
        try:
            return True, Vehicle.serialize(
                Vehicle.query.filter_by(id=id).first_or_404(
                            description=f'Record with id={id} \
                                is unavailable'))
        except Exception as e:
            return False, e
    
    def read_signed_out_vehicles(self):
        """get all signed out cars"""
        print(request.args)
        page = request.args.get('page', 1, type=int)
        print(page)
        per_page = request.args.get('per_page', 5, type=int)
        vehicles = Vehicle.query.filter_by(flag="signed out").paginate(page=page, per_page=per_page)
        response = response_serializer(vehicles)
        return response, 200

    def sign_out_vehicle(self, vehicle_id):
        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description=f'Vehicle with id={vehicle_id} is not available')

            if vehicle.flag == "admitted":
                vehicle.flag = "signed out"
                vehicle.signed_out_at = datetime.datetime.now()
                vehicle.signed_out_date = datetime.datetime.now()
                db.session.commit()
                message = {"message": "Vehicle signed out successfully"}

                return make_response(jsonify(message), 200)
            else:
                message = {"message": "Vehicle signedout already"}
                return make_response(jsonify(message), 400)

        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)

    def update_vehicle(self):
        """updates record in database"""
        pass

    def delete_vehicle(self):
        """deletes record from database"""
        pass

    # CHARGES
    def create_charges(self, data, chargeType):
        """creates record that are saved into the database"""
        try:
            new_data = chargeType(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            message = {
                "status": "success",
                "message": "Charge saved successfully",
                "vehicle": data
            }
            return make_response(jsonify(message), 201)
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)

    def read_charges(self, chargeType, serializer):
        """views record in database"""
        # return "Hellow world", 200
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        charges = chargeType.query.paginate(page=page, per_page=per_page)
        response = serializer(charges)
        return response, 200

    def get_single_charge(self, charge_id, chargeType):
        return chargeType.serialize(
            chargeType.query.filter_by(id=charge_id).first_or_404(
                description='Record with id={} is not available'.format(
                    charge_id))), 200

    def update_charges(self):
        """updates record in database"""

    def delete_charges(self):
        """deletes record from database"""

    # CLINIC
    def create_clinic(self):
        """creates record that are saved into the database"""

    def read_clinic(self):
        """views record in database"""

    def update_clinic(self):
        """updates record in database"""

    def delete_clinic(self):
        """deletes record from database"""

    # PAYMENT
    def create_payment(self, data, chargeType):
        """creates record that are saved into the database"""
        vehicle_id = data['vehicle_id']
        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first_or_404(
                description='Record with id={} is not available'.format(
                    vehicle_id))

            if vehicle.parking is True:
                return make_response(jsonify({"message": "Paid already"}), 400)

            new_data = chargeType(**data)
            db.session.add(new_data)
            db.session.commit()
            print(data)

            vehicle.parking = True
            db.session.commit()

            message = {
                "status": "success",
                "message": "Payment made successfully",
                "vehicle": data
            }
            return make_response(jsonify(message), 201)
        except Exception as e:
            print(e)
            error = {
                "status": "error",
                "error": str(e)
            }
            return make_response(jsonify(error), 400)

    def read_payment(self, paymentType, serializer):
        """views record in database"""
        payments = paymentType.query.all()
        response = serializer(payments)
        return response, 200

    def get_single_payment(self, chargeType, payment_id):
        return chargeType.serialize(
            chargeType.query.filter_by(id=payment_id).first_or_404(
                description='Record with id={} is not available'.format(
                    payment_id))), 200

    def update_payment(self):
        """updates record in database"""
        pass

    def delete_payment(self):
        """deletes record from database"""
        pass

    def signup(self):
        """signup user"""
        pass

    def login(self):
        """login user"""
        pass
