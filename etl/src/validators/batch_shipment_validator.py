from database.db import Database


class BatchValidator:
    def __init__(self, connection, batch_size: int = 50000):
        self.batch_size = batch_size
        self.conn = connection

    def setup_temp_tables(self):
        """Creates necessary temporary tables for batch processing"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TEMP TABLE IF NOT EXISTS temp_shipments (
                    shipment_id VARCHAR(20),
                    origin VARCHAR(100),
                    destination VARCHAR(100),
                    weight DECIMAL(10,2),
                    cost DECIMAL(10,2),
                    delivery_time INTEGER,
                    log_id VARCHAR(20)
                ) ON COMMIT DELETE ROWS;
                
                CREATE INDEX IF NOT EXISTS idx_temp_shipments_log_id 
                ON temp_shipments(log_id);
            """
            )
