from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from src.ingestion import Ingestor
from config.settings import RAW_DATA_DIR, DATABASE_TABLES,DB_CONNECTION_STRING

def worker_task(table_name:str):
    """
    Worker task to ingest data for a specific table.

    Args:
        table_name (str): The name of the table to ingest.

    Returns:
        str: The path to the saved file after ingestion.
    """
    ingestor = Ingestor(DB_CONNECTION_STRING,RAW_DATA_DIR)

    file_saved = ingestor.ingest_table(table_name,extraction_date=pd.Timestamp.now())

    return file_saved
    
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(worker_task, DATABASE_TABLES))
        for result in results:
            print(f"File saved: {result}")