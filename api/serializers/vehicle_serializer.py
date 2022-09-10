from ..models import Cartype, Vehicle


def response_serializer(vehicles: Vehicle):
    response = []

    for vehicle in vehicles:

        vehicle_dict = {
            "id": str(vehicle.id),
            "driver_name": vehicle.driver_name,
            "color": vehicle.color,
            "model": vehicle.model,
            "phone_number": vehicle.phone_number,
            "nin_number": vehicle.nin_number,
            "created_at": str(vehicle.created_at),
            "gender": vehicle.gender,
        }

        response.append(vehicle_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "vehicles": response
    }

    return final_output


def car_type_serializer(cartypes: Cartype):
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