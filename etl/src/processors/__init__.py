"""
Data processing module for the ETL pipeline.
Contains processors for different types of logistics data:
- Shipment records
- Vehicle information
- Vehicle trip logs

Each processor implements specific validation and processing logic
for its respective data type.
"""

from processors.shipment_processor import ShipmentProcessor
from processors.vehicle_processor import VehicleProcessor
from processors.vehicle_log_processor import VehicleLogProcessor