from sqlalchemy import text

from app.utils.logger import get_logger
from app.constants.tables import Tables
from app.db.session import get_context_db

logger = get_logger(__name__)


INDEXES = {
    # "vehicle_logs_date": f"CREATE INDEX IF NOT EXISTS idx_vehicle_logs_date ON {Tables.vehicle_logs}(trip_date);",
    # "vehicle_logs_composite": f"CREATE INDEX IF NOT EXISTS idx_vehicle_logs_composite ON {Tables.vehicle_logs}(trip_date, vehicle_id, log_id);",
    # "shipments_log_cost": f"CREATE INDEX IF NOT EXISTS idx_shipments_log_cost ON {Tables.shipments}(log_id, cost, delivery_time);",
    "shipments_log_id": f"CREATE INDEX IF NOT EXISTS idx_shipments_log_id ON {Tables.shipments}(log_id);",
    "shipment_routes": f"CREATE INDEX IF NOT EXISTS idx_shipment_routes ON {Tables.shipments}(origin, destination);",
    # For cost analysis
    "shipments_cost_weight": f"CREATE INDEX IF NOT EXISTS idx_shipments_cost_weight ON {Tables.shipments}(cost, weight);",
}


def get_partition_indexes(table_name, columns, years=range(2020, 2026)):
    return [
        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{year} ON {table_name}_{year}({', '.join(columns)});"
        for year in years
    ]


PARTITION_INDEXES = {
    "shipments_log_cost": get_partition_indexes(
        Tables.shipments, ["log_id", "cost", "delivery_time"]
    ),
    "vehicle_logs_composite": get_partition_indexes(
        Tables.vehicle_logs, ["trip_date", "vehicle_id", "log_id"]
    ),
    "vehicle_logs_date": get_partition_indexes(Tables.vehicle_logs, ["trip_date"]),
    "shipments_cost_weight": get_partition_indexes(
        Tables.shipments, ["cost", "weight"]
    ),
    "shipment_routes": get_partition_indexes(
        Tables.shipments, ["origin", "destination"]
    ),
}


class IndexManager:
    def create_indexes(self):
        with get_context_db() as db:
            logger.info("Creating indexes...")
            try:
                for index_name, sql in INDEXES.items():
                    db.execute(text(sql))
                    logger.info(f"Index {index_name} created")

                for index_name, sqls in PARTITION_INDEXES.items():
                    for sql in sqls:
                        db.execute(text(sql))
                        logger.info(f"PARTITION Index {index_name} created")

                logger.info("Indexes created successfully")
                db.commit()

            except Exception as e:
                logger.error(f"Error creating indexes: {e}")
                db.rollback()
