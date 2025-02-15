from pathlib import Path

from processors.stream_processor import StreamProcessor
from constants.constants import VEHICLE_COLUMNS, Tables, FilePaths
from validators.vehicle_logs_validator import validate_vehicle_log
from utils.file import get_data_file_path


class VehicleProcessor(StreamProcessor):
    """
    Processor for vehicle data.
    Handles ingestion of vehicle information into the vehicles table.
    No validation required for vehicle records.
    """

    def __init__(self):
        """
        Initialize the vehicle processor.
        Sets up file path, table name, and columns for vehicle data processing.
        """
        self.file_path = get_data_file_path(FilePaths.vehicles)
        self.table_name = Tables.vehicles
        self.columns = VEHICLE_COLUMNS
        self.validation_callback = None
        super().__init__(
            self.file_path, self.table_name, self.columns, self.validation_callback
        )

    def run(self) -> bool:
        """
        Execute the vehicle data processing pipeline.
        
        Returns:
            bool: True if processing successful, False otherwise
        """
        return self.process_file()
