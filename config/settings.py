import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_STRING = os.getenv("DATABASE_URL")

DATABASE_TABLES = [
    "customers",
    "orders",
    "order_details",
    "products",
    "categories",
    "suppliers",
    "employees",
]

RAW_DATA_DIR = Path("data") / "raw" / "northwind"

DUCKDB_DIR = Path("warehouse") / "northwind_dw.duckdb"