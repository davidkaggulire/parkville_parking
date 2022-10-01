"""vehicle_serializer"""

from ..models import Cartype, Vehicle


def response_serializer(vehicles: Vehicle):
    """serializer for vehicle list"""
    response = []

    for vehicle in vehicles:

        car_type = Cartype.query.filter_by(id=vehicle.cartype_id).first_or_404(
            description=f'Record with id={vehicle.cartype_id} is \
                not available')

        vehicle_dict = {
            "id": str(vehicle.id),
            "driver_name": vehicle.driver_name,
            "color": vehicle.color,
            "model": vehicle.model,
            "phone_number": vehicle.phone_number,
            "nin_number": vehicle.nin_number,
            "number_plate": vehicle.number_plate,
            "created_at": str(vehicle.created_at),
            "signed_out_at": str(vehicle.signed_out_at),
            "signed_out_date": str(vehicle.signed_out_date),
            "gender": vehicle.gender,
            "car_type": car_type.type,
            "battery": vehicle.battery,
            "parking": vehicle.parking,
            "clinic": vehicle.clinic,
            "flag": vehicle.flag
        }

        response.append(vehicle_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "vehicles": response
    }

    return final_output


def car_type_serializer(cartypes: Cartype):
    """serializer for cartypes"""
    response = []

    for cartype in cartypes:

        car_type_dict = {
            "id": str(cartype.id),
            "type": cartype.type,
        }

        response.append(car_type_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "car_types": response
    }

    return final_output
