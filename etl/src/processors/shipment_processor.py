from io import StringIO
import os
import ijson
from dotenv import load_dotenv

from validators.batch_shipment_validator import BatchValidator
from processors.stream_processor import StreamProcessor
from database.db import Database
from utils.logger import get_logger
from constants.constants import SHIPPING_COLUMNS, Tables, FilePaths
from utils.file import get_data_file_path


load_dotenv()

logger = get_logger(__name__)

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10000))


class ShipmentProcessor(StreamProcessor):
    """
    Processor for shipment data.
    Handles ingestion of shipment records with complex validation against vehicle logs.
    Uses temporary tables for batch validation and processing.
    """

    def __init__(self):
        """
        Initialize the shipment processor.
        Sets up database connection, batch processing, and validation components.
        """
        self.file_path = get_data_file_path(FilePaths.shipments)
        self.table_name = Tables.shipments
        self.columns = SHIPPING_COLUMNS

        super().__init__(self.file_path, self.table_name, self.columns, None)
        # Keep Database connection same to use TEMP tables
        self.db = Database.get_instance().get_connection()
        self.validator = BatchValidator(self.db, BATCH_SIZE)
        self.current_batch = []
        self.batch_buffer = StringIO()

    def process_batch(self) -> bool:
        """
        Process a batch of shipment records.
        Validates records against vehicle logs and handles invalid records.
        
        Returns:
            bool: True if batch processing successful, False otherwise
        """
        try:
            self.validator.setup_temp_tables()

            # Use existing copy_from method for initial batch load
            with self.db.cursor() as cur:
                cur.execute("TRUNCATE temp_shipments")
                self.batch_buffer.seek(0)
                cur.copy_from(
                    self.batch_buffer,
                    table="temp_shipments",
                    columns=self.columns,
                    sep="\t",
                )

                # Identify and handle invalid records
                cur.execute(
                    """
                    WITH invalid_records AS (
                        SELECT t.*
                        FROM temp_shipments t
                        LEFT JOIN vehicle_logs v ON t.log_id = v.log_id
                        WHERE v.log_id IS NULL
                        AND t.log_id NOT IN (
                            SELECT log_id 
                            FROM vehicle_logs 
                            WHERE trip_date > CURRENT_DATE
                        )
                    )
                    SELECT array_to_json(array_agg(row_to_json(r)))
                    FROM invalid_records r;
                """
                )

                invalid_records = cur.fetchone()[0] or []

                if invalid_records:
                    # Use existing save_invalid_items method
                    self.save_invalid_items(invalid_records)

                # Insert valid records
                cur.execute(
                    """
                    INSERT INTO shipments
                        SELECT t.*, v.trip_date
                    FROM temp_shipments t
                    JOIN vehicle_logs v ON t.log_id = v.log_id;
                """
                )

                # check result of insert
                cur.execute("SELECT COUNT(*) FROM shipments")
                count = cur.fetchone()[0]
                logger.info(f"Inserted {count} valid records into shipments")

                # commit the transaction
                self.db.commit()
                return True

        except Exception as e:
            self.db.rollback()
            # Use existing save_failed_data method
            self.batch_buffer.seek(0)
            self.save_failed_data(self.batch_buffer.getvalue())
            logger.error(f"Batch processing failed: ", e)
            return False

    def process_file(self) -> bool:
        """
        Process the shipment file with batch processing.
        Overrides the base class method to implement batch validation.
        
        Returns:
            bool: True if file processing successful, False otherwise
        """
        if not os.path.exists(self.file_path):
            logger.error(f"File not found: {self.file_path}")
            return False

        logger.info(f"Processing file: {self.file_path}")

        try:
            with open(self.file_path, "r") as file:
                count = 0
                self.current_batch = []
                self.batch_buffer = StringIO()

                for item in ijson.items(file, "item"):
                    values = [
                        str(item[col]) if item[col] is not None else "\\N"
                        for col in self.columns
                    ]
                    self.batch_buffer.write("\t".join(values) + "\n")
                    count += 1

                    if count % BATCH_SIZE == 0:
                        success = self.process_batch()

                        if not success:
                            return False
                        self.batch_buffer = StringIO()

                # Process remaining records
                if self.batch_buffer.tell() > 0:
                    success = self.process_batch()
                    if not success:
                        return False

                logger.info(f"Processed {count} items")

                # Use existing move_processed_file method
                self.move_processed_file()
                return True

        except Exception as e:
            logger.error(f"File processing failed: ", e)
            return False

    def run(self) -> bool:
        return self.process_file()
