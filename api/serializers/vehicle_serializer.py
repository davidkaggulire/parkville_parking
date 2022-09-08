from operator import length_hint
from ..models import Charge, Vehicle


def response_serializer(vehicles: Vehicle):
    response = []

    for vehicle in vehicles:

        charge = Charge.query.filter_by(id=vehicle.charge_id).first_or_404(
            description='Record with id={} is not available'.format(vehicle.charge_id))
        vehicle_dict = {
            "id": str(vehicle.id),
            "driver_name": vehicle.driver_name,
            "color": vehicle.color,
            "model": vehicle.model,
            "phone_number": vehicle.phone_number,
            "nin_number": vehicle.nin_number,
            "duration_type": vehicle.duration_type,
            "charge_value": vehicle.charge_value,
            "vehicle_type": charge.vehicle_type,
            "created_at": str(vehicle.created_at),
            "status": vehicle.status,
        }

        response.append(vehicle_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "vehicles": response
    }

    return final_output
