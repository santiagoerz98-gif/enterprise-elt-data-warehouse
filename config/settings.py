from pathlib import Path

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