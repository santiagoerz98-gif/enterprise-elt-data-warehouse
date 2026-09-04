import duckdb

# Conectar a la base de datos
con = duckdb.connect('warehouse/northwind_dw.duckdb')

# 2. Probar una consulta sobre un modelo
print("\n--- MUESTRA DE DATOS ---")
tables = con.execute("SHOW TABLES FROM main_silver;").df()
for table in tables['name']:
    print(con.execute(f"SUMMARIZE SELECT * FROM main_silver.{table};").df())

con.close()