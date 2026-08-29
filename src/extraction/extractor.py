import pandas as pd
from pathlib import Path
import logging
from config.settings import DATABASE_TABLES

logger = logging.getLogger(__name__)


# class for extracting data from the database and storaging in local files as parquet files(raw layer)
class DataExtractor:
    def __init__(self, engine):
        self.engine = engine

    def extract_data(self, table_name: str) -> pd.DataFrame:
        """
        Extracts data from the database and saves it as a parquet file in the raw layer.
        Args:
            table_name (str): The name of the table to extract data from.

        Returns:
            pd.DataFrame: The extracted data as a pandas DataFrame.
        """

        # Generate the SQL query to extract data from the specified table
        query = self.generate_query(table_name)

        # Log the extraction process
        logger.info(f"Extracting data from table: {table_name} using query: {query}")

        # Execute the query and read the data into a pandas DataFrame
        df = pd.read_sql(query, self.engine)

        logger.info(f"Extracted {len(df)} rows from table {table_name}")

        return df


    def generate_query(self, table_name):
        if table_name not in DATABASE_TABLES:
            raise ValueError(f"Table '{table_name}' is not a valid table name. Valid table names are: {DATABASE_TABLES}")
        return f"SELECT * FROM {table_name}"