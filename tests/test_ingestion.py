from src.extraction.extractor import DataExtractor
from src.storage.parquet_storage import ParquetStorage
import pandas as pd
from config.settings import RAW_DATA_DIR
from config.database import engine

extractor = DataExtractor(engine)
parquet_storage = ParquetStorage(RAW_DATA_DIR)

table_name = "orders"

data = extractor.extract_data(table_name)

extraction_date = pd.Timestamp.now()

file_path = parquet_storage.save(data, table_name, extraction_date)

print(f"Data for table '{table_name}' extracted and saved to: {file_path}")
print(f"Data rows: {data.shape[0]}")
print(f"Data columns: {data.columns.tolist()}")
print(f"Data types: {data.dtypes.to_dict()}")
print (f"First 5 rows:\n{data.head()}")
