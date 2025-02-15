from app.utils.logger import get_logger
from app.core.tasks.database_views.view_executor import ViewExecutor

logger = get_logger(__name__)


class ViewManager:
    def __init__(self):
        self.view_executors = ViewExecutor()

    def create_materialize_views(self):
        logger.info("Creating materialized views...")

        # run executor
        self.view_executors.execute()

        logger.info("Materialized views created")

    # Future implementation
    def refresh_views(self):
        pass
