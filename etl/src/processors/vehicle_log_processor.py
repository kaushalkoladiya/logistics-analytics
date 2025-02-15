from processors.stream_processor import StreamProcessor
from constants.constants import VEHICLE_LOG_COLUMNS, Tables, FilePaths
from utils.file import get_data_file_path
from validators.vehicle_logs_validator import validate_vehicle_log


class VehicleLogProcessor(StreamProcessor):
    """
    Processor for vehicle log data.
    Handles ingestion of vehicle trip logs with validation for mileage and fuel data.
    """

    def __init__(self):
        """
        Initialize the vehicle log processor.
        Sets up file path, table name, columns, and validation for log data processing.
        """
        self.file_path = get_data_file_path(FilePaths.vehicle_logs)
        self.table_name = Tables.vehicle_logs
        self.columns = VEHICLE_LOG_COLUMNS
        # self.validation_callback = None
        self.validation_callback = validate_vehicle_log
        super().__init__(
            self.file_path, self.table_name, self.columns, self.validation_callback
        )

    def run(self) -> bool:
        """
        Execute the vehicle log processing pipeline.
        
        Returns:
            bool: True if processing successful, False otherwise
        """
        return self.process_file()
