VEHICLE_LOG_COLUMNS = [
    "log_id",
    "vehicle_id",
    "trip_date",
    "mileage",
    "fuel_used",
]

VEHICLE_COLUMNS = [
    "vehicle_id",
    "name",
    "total_mileage",
]

SHIPPING_COLUMNS = [
    "shipment_id",
    "origin",
    "destination",
    "weight",
    "cost",
    "delivery_time",
    "log_id",
]


class Tables:
    vehicles = "vehicles"
    vehicle_logs = "vehicle_logs"
    shipments = "shipments"


class FilePaths:
    vehicles = "data/raw/vehicles.json"
    vehicle_logs = "data/raw/vehicle_logs.json"
    shipments = "data/raw/shipments.json"
