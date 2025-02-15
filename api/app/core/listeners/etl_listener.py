import select
import psycopg2

from app.core.config import settings
from app.core.tasks.task_manager import TaskManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ETLListener:
    def __init__(self):
        self.connection_params = {
            "dbname": settings.POSTGRES_DB,
            "user": settings.POSTGRES_USER,
            "password": settings.POSTGRES_PASSWORD,
            "host": settings.POSTGRES_SERVER,
            "port": settings.POSTGRES_PORT,
        }
        # Create dedicated connection for listening
        self.listen_conn = psycopg2.connect(**self.connection_params)
        self.listen_conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        )

        # Initialize task managers
        self.task_manager = TaskManager()

    def process_batch(self, batch_id: str):
        try:
            logger.info(f"Starting post-ETL processing for batch: {batch_id}")
            self.task_manager.process_completed_batch(batch_id)

        except Exception as e:
            logger.error(f"Error processing batch {batch_id}: {e}")

    def start_listening(self):
        """Start listening for ETL completion notifications"""
        try:
            with self.listen_conn.cursor() as cur:
                cur.execute("LISTEN etl_complete")
                logger.info("Started listening for ETL completion")

                while True and not self.listen_conn.closed:
                    if select.select([self.listen_conn], [], [], 60) == ([], [], []):
                        # Timeout - optional keep-alive check
                        continue

                    self.listen_conn.poll()
                    while self.listen_conn.notifies:
                        notify = self.listen_conn.notifies.pop()
                        batch_id = notify.payload
                        logger.info(
                            f"Received ETL completion notification for batch: {batch_id}"
                        )

                        # Process the completed batch
                        self.process_batch(batch_id)
                        # Close the connection to prevent memory leak
                        self.listen_conn.close()

        except Exception as e:
            logger.error(f"Listener error: {e}")
            self.listen_conn.close()
            raise e

    def cleanup(self):
        if self.listen_conn and not self.listen_conn.closed:
            self.listen_conn.close()
