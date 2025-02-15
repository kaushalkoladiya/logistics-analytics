from database.db import Database
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    def __init__(self):
        self.db = Database.get_instance().get_connection()
        self.setup_tracking_table()

    def setup_tracking_table(self):
        with self.db.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS batch_processing_status (
                    batch_id VARCHAR(50) PRIMARY KEY,
                    vehicles_processed BOOLEAN DEFAULT FALSE,
                    vehicle_logs_processed BOOLEAN DEFAULT FALSE,
                    shipments_processed BOOLEAN DEFAULT FALSE,
                    batch_started_at TIMESTAMP,
                    batch_completed_at TIMESTAMP
                )
            """
            )
            self.db.commit()

    def start_batch(self):
        batch_id = datetime.now().strftime("BATCH_%Y%m%d_%H%M%S")

        with self.db.cursor() as cur:
            cur.execute(
                """
                INSERT INTO batch_processing_status 
                (batch_id, batch_started_at)
                VALUES (%s, NOW())
            """,
                (batch_id,),
            )
            self.db.commit()

        logger.info(f"Started new batch: {batch_id}")
        return batch_id

    def mark_table_complete(self, batch_id: str, table_name: str):
        column_name = f"{table_name}_processed"

        with self.db.cursor() as cur:
            # Update status
            cur.execute(
                f"""
                UPDATE batch_processing_status 
                SET {column_name} = TRUE
                WHERE batch_id = %s
            """,
                (batch_id,),
            )

            # Check if all tables are processed
            cur.execute(
                """
                SELECT 
                    vehicles_processed AND 
                    vehicle_logs_processed AND 
                    shipments_processed
                FROM batch_processing_status
                WHERE batch_id = %s
            """,
                (batch_id,),
            )

            all_complete = cur.fetchone()[0]

            if all_complete:
                # Update completion timestamp
                cur.execute(
                    """
                    UPDATE batch_processing_status 
                    SET batch_completed_at = NOW()
                    WHERE batch_id = %s
                """,
                    (batch_id,),
                )

                # Simple notification with just batch_id
                cur.execute("NOTIFY etl_complete, %s", (batch_id,))
                logger.info(f"Batch {batch_id} complete, notification sent")

            self.db.commit()

    def get_batch_status(self, batch_id: str) -> dict:
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    batch_id,
                    vehicles_processed,
                    vehicle_logs_processed,
                    shipments_processed,
                    batch_started_at,
                    batch_completed_at
                FROM batch_processing_status
                WHERE batch_id = %s
            """,
                (batch_id,),
            )

            result = cur.fetchone()
            if result:
                return {
                    "batch_id": result[0],
                    "status": {
                        "vehicles": result[1],
                        "vehicle_logs": result[2],
                        "shipments": result[3],
                    },
                    "started_at": result[4],
                    "completed_at": result[5],
                }
            return None
