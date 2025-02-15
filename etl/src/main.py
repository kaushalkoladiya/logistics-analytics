from database.table_manager import TableManager, Tables
from database.db import Database
from processors import ShipmentProcessor, VehicleProcessor, VehicleLogProcessor
from services.notification_service import NotificationService
from utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    Database.init_db()

    table_manager = TableManager()
    table_manager.create_base_tables()

    notification_service = NotificationService()

    # Start new batch
    batch_id = notification_service.start_batch()

    vehicle_processor = VehicleProcessor()
    vehicle_result = vehicle_processor.run()
    if vehicle_result:
        notification_service.mark_table_complete(batch_id, Tables.vehicles)

    vehicle_log_processor = VehicleLogProcessor()
    log_result = vehicle_log_processor.run()
    if log_result:
        notification_service.mark_table_complete(batch_id, Tables.vehicle_logs)

    shipment_processor = ShipmentProcessor()
    if shipment_processor.run():
        notification_service.mark_table_complete(batch_id, Tables.shipments)

    # Optional: Get final status
    final_status = notification_service.get_batch_status(batch_id)
    logger.info(f"Batch processing completed: {final_status}")

    # exit the program
    exit(0)
