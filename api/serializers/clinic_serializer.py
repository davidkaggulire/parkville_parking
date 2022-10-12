"""clinic_serializer.py"""

from api.models import Cartyreclinic, ClinicPayment, Vehicle


def clinic_serializer(services: Cartyreclinic):
    """clinic serializer"""
    response = []

    for service in services.items:
        service_dict = {
            'id': str(service.id),
            "service": service.service,
            'fee': service.fee
        }

        response.append(service_dict)

    meta = {
        "page": services.page,
        'pages': services.pages,
        'total_count': services.total,
        'prev_page': services.prev_num,
        'next_page': services.next_num,
        'has_next': services.has_next,
        'has_prev': services.has_prev,

    }

    final_output = {
        "status": "success",
        "results": len(response),
        "clinic_services": response,
        "meta": meta
    }

    return final_output


def clinic_pay_serializer(payments: ClinicPayment):
    """clinic payments serializer"""
    response = []

    for payment in payments:

        car_tyre_clinic = Cartyreclinic.query.filter_by(
            id=payment.service_id).first_or_404(
            description=f'Record with id={payment.service_id} is \
                not available')

        vehicle = Vehicle.query.filter_by(id=payment.vehicle_id).first_or_404(
            description=f'Record with id={payment.vehicle_id} is \
                not available')

        payment_dict = {
            'id': str(payment.id),
            "service_id": str(payment.service_id),
            'vehicle_id': str(payment.vehicle_id),
            'service': car_tyre_clinic.service,
            'fee': car_tyre_clinic.fee,
            'number_plate': vehicle.number_plate,
            'driver_name': vehicle.driver_name,
            "paid_at": str(payment.paid_at),
            "paid_date": str(payment.paid_date)
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "clinic_payments": response
    }

    return final_output


def clinic_pay_single_serializer(payment):
    """clinic payments serializer for single car"""
    car_tyre_clinic = Cartyreclinic.query.filter_by(
        id=payment["service_id"]).first_or_404(
        description='Cartyreclinic with id={} is not available'.format(
            payment["service_id"]))

    vehicle = Vehicle.query.filter_by(id=payment["vehicle_id"]).first_or_404(
        description='Vehicle with id={} is not available'.format(
            payment["vehicle_id"]))

    payment_dict = {
        'id': str(payment["id"]),
        "service_id": str(payment["service_id"]),
        'vehicle_id': str(payment["vehicle_id"]),
        'service': car_tyre_clinic.service,
        'fee': car_tyre_clinic.fee,
        'number_plate': vehicle.number_plate,
        'driver_name': vehicle.driver_name,
        "paid_at": str(payment["paid_at"]),
        "paid_date": str(payment["paid_date"])
    }

    final_output = {
        "status": "success",
        "message": "payment made succesfully",
        "clinic_payments": payment_dict
    }

    return final_output
