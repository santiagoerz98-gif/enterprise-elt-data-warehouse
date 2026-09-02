import duckdb

# Conectar a la base de datos
con = duckdb.connect('warehouse/northwind_dw.duckdb')

# 2. Probar una consulta sobre un modelo
print("\n--- MUESTRA DE DATOS ---")
print(con.execute("SELECT * FROM main_silver.silver_orders WHERE shipping_status = 'Delayed' LIMIT 10;").df())

con.close()