"""charge_serializer"""

from ..models import Bodacharge, Carcharge, Coastercharge
from ..models import Taxicharge, Truckcharge


def truck_serializer(charges: Truckcharge):
    """truck serializer"""
    response = []

    for charge in charges:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "truck_charges": response
    }

    return final_output


def taxi_serializer(charges: Taxicharge):
    """taxi_serializer"""
    response = []

    for charge in charges:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "taxi_charges": response
    }

    return final_output


def coaster_serializer(charges: Coastercharge):
    """coaster_serializer"""
    response = []

    for charge in charges:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "coaster_charges": response
    }

    return final_output


def car_serializer(charges: Carcharge):
    """car_serializer"""
    response = []

    for charge in charges:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "car_charges": response
    }

    return final_output


def boda_serializer(charges: Bodacharge):
    """boda_serializer"""
    response = []

    for charge in charges:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "boda_charges": response
    }

    return final_output
