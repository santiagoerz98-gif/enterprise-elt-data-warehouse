import duckdb
import logging
from config.settings import GOLD_LAYER_TABLES, GOLD_OUTPUT_DIR

logger = logging.getLogger(__name__)

try:
    logger.info("Connecting to DuckDB...")
    con = duckdb.connect('warehouse/northwind_dw.duckdb')
    logger.info("Successfully connected to DuckDB.")
except Exception as e:
    logger.error("Failed to connect to DuckDB: %s", e)
    raise

for table in GOLD_LAYER_TABLES:
    output_file = GOLD_OUTPUT_DIR / f"{table}.parquet"
    try:
        logger.info("Exporting table %s to %s", table, output_file)
        con.execute(f"COPY main_gold.{table} TO '{output_file}' (FORMAT PARQUET, COMPRESSION ZSTD)")
        logger.info("Successfully exported table %s", table)
    except Exception as e:
        logger.error("Failed to export table %s: %s", table, e)

con.close()
