from sqlalchemy.orm import Session
from sqlalchemy import text

from app.utils.logger import get_logger

logger = get_logger(__name__)


class MaterializedViewManager:
    """Manages materialized views and indexes using an SQLAlchemy session."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_view(self, view_name: str, query: str):
        """Creates a materialized view if it does not exist."""
        logger.info(f"Creating materialized view {view_name}...")
        sql_query = text(
            f"CREATE MATERIALIZED VIEW IF NOT EXISTS {view_name} AS {query};"
        )
        self._execute_sql(sql_query)

    def refresh_view(self, view_name: str, concurrently: bool = True):
        """Refreshes a materialized view."""
        logger.info(f"Refreshing materialized view {view_name}...")
        concurrent_sql = "CONCURRENTLY" if concurrently else ""
        sql_query = text(f"REFRESH MATERIALIZED VIEW {concurrent_sql} {view_name};")
        self._execute_sql(sql_query)

    def create_index(self, index_name: str, view_name: str, column: str):
        """Creates an index on a materialized view."""
        logger.info(f"Creating index {index_name} on {view_name}...")
        sql_query = text(
            f"CREATE INDEX IF NOT EXISTS {index_name} ON {view_name} ({column});"
        )
        self._execute_sql(sql_query)

    def create_unique_index(self, index_name: str, view_name: str, column: str):
        """Creates a unique index on a materialized view."""
        logger.info(f"Creating unique index {index_name} on {view_name}...")
        sql_query = text(
            f"CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {view_name} ({column});"
        )
        self._execute_sql(sql_query)

    def _execute_sql(self, sql_query):
        """Executes a SQL command using the provided SQLAlchemy session."""
        try:
            logger.debug(f"Executing SQL query for: {sql_query}")
            self.db_session.execute(sql_query)
            self.db_session.commit()
            logger.debug("SQL query executed successfully")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error executing SQL query: {e}")
