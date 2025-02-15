from database.db import Database
from constants.constants import Tables
from utils.logger import get_logger

logger = get_logger(__name__)


class TableManager:
    def __init__(self):
        self.db = Database.get_instance()
        self.partition_year_range = range(2020, 2026)

    def create_table(
        self,
        table_name,
        schema,
        partition_key=None,
    ):
        try:
            partition_key = (
                f"PARTITION BY RANGE({partition_key})" if partition_key else ""
            )

            query = (
                f"CREATE TABLE IF NOT EXISTS {table_name} ({schema}) {partition_key}"
            )
            self.db.execute(query)
            logger.info(f"Table {table_name} created successfully")
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {e}")
            raise

    def create_partition(self, table_name, partition_key, start_date, end_date):
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name}_{partition_key} PARTITION OF {table_name} FOR VALUES FROM ({start_date}) TO ({end_date});"
            self.db.execute(query)
            logger.info(
                f"Partition {partition_key} created successfully for table {table_name}"
            )
        except Exception as e:
            logger.error(f"Error creating partition {partition_key}: {e}")

    def create_base_tables(self):
        try:
            self.create_table(
                table_name=Tables.vehicles,
                schema=(
                    "vehicle_id VARCHAR(10) PRIMARY KEY,"
                    "name VARCHAR(100) NOT NULL,"
                    "total_mileage FLOAT NOT NULL CHECK (total_mileage >= 0)"
                ),
            )
            self.create_table(
                table_name=Tables.vehicle_logs,
                schema=(
                    "log_id VARCHAR(10) NOT NULL,"
                    "vehicle_id VARCHAR(10) REFERENCES vehicles(vehicle_id),"
                    "trip_date DATE NOT NULL,"
                    "mileage FLOAT NOT NULL CHECK (mileage >= 0),"
                    "fuel_used FLOAT NOT NULL CHECK (fuel_used >= 0),"
                    "PRIMARY KEY (log_id, trip_date)"
                ),
                partition_key="trip_date",
            )

            for year in self.partition_year_range:
                self.create_partition(
                    Tables.vehicle_logs, year, f"'{year}-01-01'", f"'{year+1}-01-01'"
                )

            self.create_table(
                table_name=Tables.shipments,
                schema=(
                    "shipment_id VARCHAR(10) NOT NULL,"
                    "origin VARCHAR(100) NOT NULL,"
                    "destination VARCHAR(100) NOT NULL,"
                    "weight FLOAT NOT NULL CHECK (weight > 0),"
                    "cost FLOAT NOT NULL CHECK (cost > 0),"
                    "delivery_time INTEGER NOT NULL CHECK (delivery_time > 0),"
                    "log_id VARCHAR(10) NOT NULL,"
                    "trip_date DATE NOT NULL,"
                    "PRIMARY KEY (shipment_id, trip_date)"
                ),
                partition_key="trip_date",
            )

            for year in self.partition_year_range:
                self.create_partition(
                    Tables.shipments, year, f"'{year}-01-01'", f"'{year+1}-01-01'"
                )

        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
