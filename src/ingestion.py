import logging
from pathlib import Path
import duckdb
from config.settings import DATABASE_TABLES
from datetime import datetime

logger = logging.getLogger(__name__)


class Ingestor:
    def __init__(self, db_connection_string: str, raw_data_dir: Path, db_type: str = "postgres" ):
        """
        Initializes the Ingestor with a database connection string and type.
        Args:
            db_connection_string (str): The connection string for the database.
            example(postgres): "dbname=dbname user=myuser password=mypassword host=localhost port=5432"
            db_type (str): The type of the database (default is "postgres").
        """
        self.db_connection_string = db_connection_string
        self.db_type = db_type.lower()
        self.raw_data_dir = raw_data_dir

    def ingest_table(self, table_name: str, extraction_date: datetime):
        """
        Ingests data from the database and saves it as a parquet file in the raw layer.
        Args:
            table_name (str): The name of the table to ingest data from.
            extraction_date (datetime): The date of extraction (used for directory structure).
        """

        self.validate_table(table_name)

        dir_path = self.build_directory_path(extraction_date)
        timestamp = extraction_date.strftime("%Y%m%d_%H%M%S")
        file_path = dir_path / f"{table_name}_{timestamp}.parquet"


        # Create a DuckDB connection
        con = duckdb.connect()
        try:
            dir_path.mkdir(parents=True, exist_ok=True)

            logger.info(f"Starting ingestion for table: {table_name} at {extraction_date}")

            # Install and load the appropriate database extension based on the db_type
            # 'INSTALL' and 'LOAD' are DuckDB commands that allow you to install and load extensions for different database types
            # This is necessary to enable DuckDB to connect to the specified database type (e.g., PostgreSQL)
            con.execute(f"INSTALL '{self.db_type}'; LOAD '{self.db_type}';")

            # Attach the database connection string to the DuckDB connection
            # This allows DuckDB to access the specified database using the provided connection string
            # The 'ATTACH' command is used to attach the database to the DuckDB connection, and the 'AS' clause specifies an alias for the attached database
            # 'TYPE {self.db_type.upper()}' specifies the type of the attached database (e.g., POSTGRES for PostgreSQL)
            con.execute(f"ATTACH '{self.db_connection_string}' AS db (TYPE {self.db_type.upper()});")
            copy_query = f"""
                COPY (SELECT * FROM db.public.{table_name}) 
                TO '{file_path.as_posix()}' 
                (FORMAT PARQUET, COMPRESSION 'ZSTD', ROW_GROUP_SIZE 100000);
            """
            con.execute(copy_query)

            row_count = con.execute(f"SELECT COUNT(*) FROM '{file_path.as_posix()}'").fetchone()[0]
            logger.info(f"Ingestion completed for table: {table_name}. Rows ingested: {row_count}. File saved at: {file_path}")

            return file_path

        except Exception as e:
            logger.exception(f"Failed to ingest table '{table_name}': {e}")
            raise

        finally:
            con.close()

    def validate_table(self, table_name: str):
        """
        Validates if the provided table name is in the list of allowed database tables.
        Args:
            table_name (str): The name of the table to validate.
        Raises:
            ValueError: If the table name is not in the list of allowed database tables.
        """
        if table_name not in DATABASE_TABLES:
            raise ValueError(f"Table '{table_name}' is not a valid table name. Valid table names are: {DATABASE_TABLES}")


    def build_directory_path(self, extraction_date: datetime) -> Path:
        """
        Builds the directory path based on the extraction date.
        Args:
            extraction_date (datetime): The date of extraction.

        Returns:
            Path: The directory path where the ingested files should be stored.
        """
        return (
            self.raw_data_dir
            / str(extraction_date.year) 
            / f"{extraction_date.month:02d}" 
            / f"{extraction_date.day:02d}"
        )