from ..models import PaymentBodaboda, PaymentCar, PaymentCoaster
from ..models import PaymentTaxi, PaymentTruck


def car_parking_serializer(payments: PaymentCar):
    response = []

    for payment in payments:

        payment_dict = {
            "id": str(payment.id),
            "vehicle_id": payment.vehicle_id,
            "charge_id": payment.charge_id,
            "paid_at": str(payment.paid_at),
            "paid_date": str(payment.paid_date)
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "payments": response
    }

    return final_output


def coaster_parking_serializer(payments: PaymentCoaster):
    response = []

    for payment in payments:

        payment_dict = {
            "id": str(payment.id),
            "vehicle_id": payment.vehicle_id,
            "charge_id": payment.charge_id,
            "paid_at": str(payment.paid_at),
            "paid_date": str(payment.paid_date)
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "payments": response
    }

    return final_output


def truck_parking_serializer(payments: PaymentTruck):
    response = []

    for payment in payments:

        payment_dict = {
            "id": str(payment.id),
            "vehicle_id": payment.vehicle_id,
            "charge_id": payment.charge_id,
            "paid_at": str(payment.paid_at),
            "paid_date": str(payment.paid_date)
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "payments": response
    }

    return final_output


def taxi_parking_serializer(payments: PaymentTaxi):
    response = []

    for payment in payments:

        payment_dict = {
            "id": str(payment.id),
            "vehicle_id": payment.vehicle_id,
            "charge_id": payment.charge_id,
            "paid_at": str(payment.paid_at),
            "paid_date": str(payment.paid_date)
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "payments": response
    }

    return final_output


def boda_parking_serializer(payments: PaymentBodaboda):
    response = []

    for payment in payments:

        payment_dict = {
            "id": str(payment.id),
            "vehicle_id": payment.vehicle_id,
            "charge_id": payment.charge_id,
            "paid_at": str(payment.paid_at),
            "paid_date": str(payment.paid_date)
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "payments": response
    }

    return final_output
