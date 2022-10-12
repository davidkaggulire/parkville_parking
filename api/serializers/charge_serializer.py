"""charge_serializer"""

from ..models import Bodacharge, Carcharge, Coastercharge
from ..models import Taxicharge, Truckcharge


def truck_serializer(charges: Truckcharge):
    """truck serializer"""
    response = []

    for charge in charges.items:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    meta = {
        "page": charges.page,
        'pages': charges.pages,
        'total_count': charges.total,
        'prev_page': charges.prev_num,
        'next_page': charges.next_num,
        'has_next': charges.has_next,
        'has_prev': charges.has_prev,

    }

    final_output = {
        "status": "success",
        "results": len(response),
        "charges": response,
        "meta": meta
    }

    return final_output


def taxi_serializer(charges: Taxicharge):
    """taxi_serializer"""
    response = []

    for charge in charges.items:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    meta = {
        "page": charges.page,
        'pages': charges.pages,
        'total_count': charges.total,
        'prev_page': charges.prev_num,
        'next_page': charges.next_num,
        'has_next': charges.has_next,
        'has_prev': charges.has_prev,

    }

    final_output = {
        "status": "success",
        "results": len(response),
        "charges": response,
        "meta": meta
    }

    return final_output


def coaster_serializer(charges: Coastercharge):
    """coaster_serializer"""
    response = []

    for charge in charges.items:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    meta = {
        "page": charges.page,
        'pages': charges.pages,
        'total_count': charges.total,
        'prev_page': charges.prev_num,
        'next_page': charges.next_num,
        'has_next': charges.has_next,
        'has_prev': charges.has_prev,

    }

    final_output = {
        "status": "success",
        "results": len(response),
        "charges": response,
        "meta": meta
    }

    return final_output


def car_serializer(charges: Carcharge):
    """car_serializer"""
    response = []

    for charge in charges.items:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    meta = {
        "page": charges.page,
        'pages': charges.pages,
        'total_count': charges.total,
        'prev_page': charges.prev_num,
        'next_page': charges.next_num,
        'has_next': charges.has_next,
        'has_prev': charges.has_prev,

    }

    final_output = {
        "status": "success",
        "results": len(response),
        "charges": response,
        "meta": meta
    }

    return final_output


def boda_serializer(charges: Bodacharge):
    """boda_serializer"""
    response = []

    for charge in charges.items:
        charge_dict = {
            'id': str(charge.id),
            "duration": charge.duration,
            'charge': charge.charge
        }

        response.append(charge_dict)

    meta = {
        "page": charges.page,
        'pages': charges.pages,
        'total_count': charges.total,
        'prev_page': charges.prev_num,
        'next_page': charges.next_num,
        'has_next': charges.has_next,
        'has_prev': charges.has_prev,

    }

    final_output = {
        "status": "success",
        "results": len(response),
        "charges": response,
        "meta": meta
    }

    return final_output
