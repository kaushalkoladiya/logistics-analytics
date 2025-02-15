from app.core.tasks.indexes_manager import IndexManager
from app.core.tasks.views_manager import ViewManager
from app.services.calculation_status import CalculationStatusService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TaskManager:
    def __init__(self):
        self.index_manager = IndexManager()
        self.view_manager = ViewManager()
        self.calculation_status_service = CalculationStatusService()

    def process_completed_batch(self, batch_id: str):
        try:
            logger.info(f"Starting post-ETL processing for batch: {batch_id}")

            # database flag to indicate calculation is in progress
            self.calculation_status_service.mark_calculation_start()

            # Create indexes
            self.index_manager.create_indexes()

            # Create/Refresh materialized views
            self.view_manager.create_materialize_views()

            # database flag to indicate calculation is complete
            self.calculation_status_service.mark_calculation_end()

            logger.info(f"Completed processing batch: {batch_id}")

        except Exception as e:
            logger.error(f"Error processing batch {batch_id}: {e}")
