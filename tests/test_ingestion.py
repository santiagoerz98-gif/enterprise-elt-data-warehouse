from src.ingestion import Ingestor
from config.settings import DB_CONNECTION_STRING, RAW_DATA_DIR
import pandas as pd

ingestor = Ingestor(DB_CONNECTION_STRING, RAW_DATA_DIR)

table_name = "orders"

extraction_date = pd.Timestamp.now()

file_path = ingestor.ingest_table(table_name, extraction_date)


print(f"Data from table '{table_name}' has been ingested and saved to: {file_path}")

