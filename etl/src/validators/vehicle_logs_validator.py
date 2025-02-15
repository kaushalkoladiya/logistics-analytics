def validate_vehicle_log(data: dict):
    if data.get("mileage") is not None and data.get("fuel_used") is not None:
        return True
    return False
