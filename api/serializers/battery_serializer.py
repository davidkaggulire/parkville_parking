"""battery_serializer"""

from api.models import BatteryPayment, Batterysection, Vehicle


def battery_section_list_serializer(sizes: Batterysection):
    """serializer"""
    response = []

    for size in sizes:
        battery_dict = {
            'id': str(size.id),
            "service": size.battery_size
        }

        response.append(battery_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "battery_list": response
    }

    return final_output


def battery_list_payment_serializer(payments: BatteryPayment):
    """serializer payment"""
    response = []

    for payment in payments:

        battery_section = Batterysection.query.filter_by(
            id=payment.battery_id).first_or_404(
            description='Record with id={} is not available'.format(
                payment.battery_id))

        vehicle = Vehicle.query.filter_by(id=payment.vehicle_id).first_or_404(
            description='Record with id={} is not available'.format(
                payment.vehicle_id))

        payment_dict = {
            'id': str(payment.id),
            "battery_id": str(payment.battery_id),
            'vehicle_id': str(payment.vehicle_id),
            'battery_size': battery_section.battery_size,
            'fee': payment.fee,
            'number_plate': vehicle.number_plate,
            'driver_name': vehicle.driver_name,
            "paid_at": str(payment.paid_at),
            "paid_date": str(payment.paid_date)
        }

        response.append(payment_dict)

    final_output = {
        "status": "success",
        "results": len(response),
        "battery_payments": response
    }

    return final_output


def battery_single_payment_serializer(payment):
    """serializer payment single"""

    battery = Batterysection.query.filter_by(
        id=payment["battery_id"]).first_or_404(
        description='Battery section with id={} is not available'.format(
            payment["battery_id"]))

    vehicle = Vehicle.query.filter_by(id=payment["vehicle_id"]).first_or_404(
        description='Vehicle with id={} is not available'.format(
            payment["vehicle_id"]))

    payment_dict = {
        'id': str(payment["id"]),
        "battery_id": str(payment["battery_id"]),
        'vehicle_id': str(payment["vehicle_id"]),
        'battery_size': battery.battery_size,
        'fee': payment["fee"],
        'number_plate': vehicle.number_plate,
        'driver_name': vehicle.driver_name,
        "paid_at": str(payment['paid_at']),
        "paid_date": str(payment['paid_date'])
    }

    final_output = {
        "status": "success",
        "message": "payment made succesfully",
        "battery_payments": payment_dict
    }

    return final_output
