from api.models import Carcharge, Cartyreclinic, ClinicPayment, Vehicle


def clinic_serializer(services: Cartyreclinic):
    response = []

    for service in services:
        service_dict = {
            'id': str(service.id),
            "service": service.service,
            'fee': service.fee
        }

        response.append(service_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "clinic_services": response
    }

    return final_output


def clinic_pay_serializer(payments: ClinicPayment):
    response = []

    for payment in payments:

        car_tyre_clinic = Cartyreclinic.query.filter_by(id=payment.service_id).first_or_404(
            description='Record with id={} is not available'.format(payment.service_id))

        vehicle = Vehicle.query.filter_by(id=payment.vehicle_id).first_or_404(
            description='Record with id={} is not available'.format(payment.vehicle_id))
        
        payment_dict = {
            'id': str(payment.id),
            "service_id": str(payment.service_id),
            'vehicle_id': str(payment.vehicle_id),
            'service': car_tyre_clinic.service,
            'fee': car_tyre_clinic.fee,
            'number_plate': vehicle.number_plate,
            'driver_name': vehicle.driver_name
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "clinic_payments": response
    }

    return final_output

def clinic_pay_single_serializer(payment):

    car_tyre_clinic = Cartyreclinic.query.filter_by(id=payment["service_id"]).first_or_404(
        description='Cartyreclinic with id={} is not available'.format(payment["service_id"]))

    vehicle = Vehicle.query.filter_by(id=payment["vehicle_id"]).first_or_404(
        description='Vehicle with id={} is not available'.format(payment["vehicle_id"]))
    
    payment_dict = {
        'id': str(payment["id"]),
        "service_id": str(payment["service_id"]),
        'vehicle_id': str(payment["vehicle_id"]),
        'service': car_tyre_clinic.service,
        'fee': car_tyre_clinic.fee,
        'number_plate': vehicle.number_plate,
        'driver_name': vehicle.driver_name
    }


    final_output = {
        "status": "success",
        "message": "payment made succesfully",
        "clinic_payments": payment_dict
    }

    return final_output