from ..models import Charge

def response_serializer(charges: Charge):
    response = []

    for charge in charges:
        charge_dict= {
            'id': str(charge.id),
            'day_charge': charge.day_charge,
            'night_charge': charge.night_charge,
            'hour_charge': charge.hour_charge,
        }

        response.append(charge_dict)

    return response