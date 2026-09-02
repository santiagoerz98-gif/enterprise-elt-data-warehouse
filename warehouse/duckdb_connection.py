import duckdb
from config.settings import DUCKDB_DIR

def get_duckdb_connection():
    DUCKDB_DIR.parent.mkdir(parents=True, exist_ok=True)

    # Connect to the DuckDB database located at DUCKDB_DIR
    # DUCKDB_DIR specifies the location of the DuckDB database file
    # This will create the database file if it does not already exist
    return duckdb.connect(str(DUCKDB_DIR)) 

if __name__ == "__main__":

    conn = get_duckdb_connection()
    conn.execute("SELECT 1")
    print(conn.fetchall())
    conn.close()