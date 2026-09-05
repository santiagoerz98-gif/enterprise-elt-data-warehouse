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

GOLD_LAYER_TABLES = [
    "fact_sales",
    "dim_customers",
    "dim_products",
    "dim_employees",
    "dim_time"
]

GOLD_OUTPUT_DIR = Path("data") / "exports" / "gold"