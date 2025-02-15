import ijson
import os
import json
from datetime import datetime
from io import StringIO
from dotenv import load_dotenv

from utils.logger import get_logger
from database.db import Database

load_dotenv()

logger = get_logger(__name__)

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10000))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))


class StreamProcessor:
    """
    Base processor class for handling streaming data ingestion.
    Provides common functionality for file processing, data validation, and database ingestion.
    """

    def __init__(
        self, file_path: str, table_name: str, columns: list, validation_callback=None
    ):
        """
        Initialize the stream processor.
        
        Args:
            file_path (str): Path to the input file
            table_name (str): Target database table name
            columns (list): List of column names for the table
            validation_callback (callable, optional): Function to validate each record
        """
        self.file_path = file_path
        self.table_name = table_name
        self.columns = columns
        self.validation_callback = validation_callback
        self.db = Database.get_instance()

    def process_file(self) -> bool:
        """
        Process the input file in streaming fashion.
        Validates records, batches them, and sends to database.
        
        Returns:
            bool: True if processing successful, False otherwise
        """
        # check if file exists
        if not os.path.exists(self.file_path):
            logger.error(f"File not found: {self.file_path}")
            return False

        logger.info(f"Processing file: {self.file_path}")

        with open(self.file_path, "r") as file:
            count = 0
            invalid_items = []
            buffer = StringIO()

            for item in ijson.items(file, "item"):
                # logger.info(f"Processing item: {item}")
                if self.validation_callback and not self.validation_callback(item):
                    invalid_items.append(item)
                    # logger.warning(f"Invalid item: {item}")
                    continue

                # values = [str(item.get(col, 'NULL')) for col in self.columns]
                values = [
                    str(item[col]) if item[col] is not None else "\\N"
                    for col in self.columns
                ]
                buffer.write("\t".join(values) + "\n")
                count += 1

                if (count % BATCH_SIZE) == 0 and count > 0:
                    logger.info(f"Processed {count} items")
                    self.ingest_data(buffer=buffer)
                    buffer = StringIO()  # Reset the buffer

            self.ingest_data(buffer=buffer)
            logger.info(f"Processed {count} items")

            if invalid_items:
                logger.warning(f"Invalid items: {len(invalid_items)}")
                # store invalid items in a file
                self.save_invalid_items(invalid_items)

            # Move file to processed directory
            self.move_processed_file()
        return True

    def ingest_data(self, buffer: StringIO, retry_count: int = 0) -> bool:
        """
        Ingest data from buffer into database with retry mechanism.
        
        Args:
            buffer (StringIO): Buffer containing the data to ingest
            retry_count (int): Current retry attempt number
            
        Returns:
            bool: True if ingestion successful, False otherwise
        """
        try:
            logger.info(f"Ingesting data into table: {self.table_name}")
            buffer.seek(0)

            result = self.db.copy_from(buffer, self.table_name, self.columns, sep="\t")

            if result:
                logger.info(f"Successfully ingested data for file {self.file_path}")
                buffer.flush()
                return True
            else:
                logger.error(f"Error ingesting data for file {self.file_path}")
                buffer.seek(0)
                self.save_failed_data(buffer.getvalue())
                return False
        except Exception as e:
            retry_count += 1
            if retry_count < MAX_RETRIES:
                logger.warning(
                    f"Error ingesting data for file {self.file_path}. Retrying..."
                )
                return self.ingest_data(buffer=buffer, retry_count=retry_count)
            else:
                logger.error(f"Error ingesting data for file {self.file_path}: {e}")
                buffer.seek(0)
                self.save_failed_data(buffer.getvalue())
                return False

    def save_failed_data(self, buffer_str: str) -> bool:
        """
        Save failed records to a file for later processing.
        
        Args:
            buffer_str (str): String containing failed records
            
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            failed_dir = os.path.join("data", "failed")
            os.makedirs(failed_dir, exist_ok=True)

            filed_file = os.path.join(failed_dir, f"{self.table_name}_{timestamp}.txt")
            logger.info(f"Saving failed data to file: {filed_file}")

            with open(filed_file, "w") as file:
                file.write(buffer_str)
            return True
        except Exception as e:
            logger.error(f"Error saving failed data: {e}")
            logger.error(f"Data: \n{buffer_str}")
            return False

    def move_processed_file(self) -> bool:
        try:
            processed_dir = os.path.join("data", "processed")
            os.makedirs(processed_dir, exist_ok=True)
            processed_file = os.path.join(
                processed_dir, os.path.basename(self.file_path)
            )
            logger.info(f"Moving file to processed directory: {processed_file}")
            os.rename(self.file_path, processed_file)
            return True
        except Exception as e:
            logger.error(f"Error moving file to processed directory: {e}")
            return False

    def save_invalid_items(self, invalid_items: list) -> bool:
        try:
            invalid_dir = os.path.join("data", "invalid")
            os.makedirs(invalid_dir, exist_ok=True)
            invalid_file = os.path.join(invalid_dir, f"{self.table_name}_invalid.json")
            logger.info(f"Saving invalid items to file: {invalid_file}")

            with open(invalid_file, "w") as file:
                json.dump(invalid_items, file, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving invalid items: {e}")
            return False

    def run(self) -> bool:
        self.process_file()
        return True
