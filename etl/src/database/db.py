import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from dotenv import load_dotenv

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class Database:
    _instance = None

    def __init__(self):
        if self._instance is not None:
            raise RuntimeError("Call get_instance() instead")
        self.db_name = os.getenv("DB_NAME", "logistics_db")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "postgres")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.connection = None
        self.cursor = None
        self.connect()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def get_connection(self):
        return self.connection

    @classmethod
    def init_db(cls):
        # if database does not exist, create it
        try:
            print("Creating database...")
            conn = psycopg2.connect(
                dbname="postgres",
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres"),
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "5432")),
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            DB_NAME = os.getenv("DB_NAME", "logistics_db")

            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [DB_NAME]
            )
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
                )

            conn.close()
            logger.info("Database created successfully")

        except Exception as e:
            logger.error(f"Error creating database: {e}")

    def connect(self):
        if (
            self.connection is None or self.connection.closed
        ):  # Check if connection exists and is closed.
            try:
                self.connection = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                )
                self.cursor = self.connection.cursor()
                logger.info(
                    "Database connection established."
                )  # Log successful connection
            except Exception as e:
                logger.error(f"Error connecting to database: {e}")
                raise  # Re-raise the exception after logging (important!)

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Database connection closed.")  # Log successful closure
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

    def execute(self, query) -> bool:
        self.connect()  # Ensure connection before executing
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()  # Rollback on error
            raise  # Re-raise exception for handling further up

    def fetch(self, query):
        self.connect()  # Ensure connection before fetching
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return []  # Return empty list, don't re-raise.

    def copy_from(self, buffer, table, columns, sep="\t") -> bool:
        self.connect()  # Ensure connection before copying
        try:
            self.cursor.copy_from(buffer, table=table, columns=columns, sep=sep)
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error copying data: {e}")
            self.connection.rollback()
            return False
