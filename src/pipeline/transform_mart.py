import os
import time
import duckdb
from pathlib import Path
from src.config import DUCKDB_PATH, RAW_DATA_DIR, SQL_DIR, PROCESSED_DATA_DIR
from src.utils.logger import logger

def execute_sql_file(con: duckdb.DuckDBPyConnection, sql_path: Path):
    logger.info(f"Executing model: {sql_path.name}")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
    for stmt in statements:
        con.execute(stmt)

def run_transformations():
    start_time = time.time()
    logger.info(f"Connecting to DuckDB target warehouse: {DUCKDB_PATH}")
    
    raw_orders = str(RAW_DATA_DIR / "orders.csv").replace("\\", "/")
    raw_items = str(RAW_DATA_DIR / "order_items.csv").replace("\\", "/")
    raw_fuls = str(RAW_DATA_DIR / "fulfillments.csv").replace("\\", "/")
    raw_prods = str(RAW_DATA_DIR / "products.csv").replace("\\", "/")
    raw_whs = str(RAW_DATA_DIR / "warehouses.csv").replace("\\", "/")
    raw_crs = str(RAW_DATA_DIR / "carriers.csv").replace("\\", "/")
    raw_custs = str(RAW_DATA_DIR / "customers.csv").replace("\\", "/")
    
    con = duckdb.connect(str(DUCKDB_PATH))
    
    try:
        logger.info("Ingesting raw CSV files into DuckDB source tables...")
        con.execute(f"CREATE OR REPLACE TABLE raw_orders AS SELECT * FROM read_csv_auto('{raw_orders}');")
        con.execute(f"CREATE OR REPLACE TABLE raw_order_items AS SELECT * FROM read_csv_auto('{raw_items}');")
        con.execute(f"CREATE OR REPLACE TABLE raw_fulfillments AS SELECT * FROM read_csv_auto('{raw_fuls}');")
        con.execute(f"CREATE OR REPLACE TABLE raw_products AS SELECT * FROM read_csv_auto('{raw_prods}');")
        con.execute(f"CREATE OR REPLACE TABLE raw_warehouses AS SELECT * FROM read_csv_auto('{raw_whs}');")
        con.execute(f"CREATE OR REPLACE TABLE raw_carriers AS SELECT * FROM read_csv_auto('{raw_crs}');")
        con.execute(f"CREATE OR REPLACE TABLE raw_customers AS SELECT * FROM read_csv_auto('{raw_custs}');")

        logger.info("--- Building Staging Layer ---")
        staging_models = [
            "stg_orders.sql",
            "stg_order_items.sql",
            "stg_fulfillments.sql",
            "stg_products.sql",
            "stg_warehouses.sql",
            "stg_carriers.sql"
        ]
        for m in staging_models:
            execute_sql_file(con, SQL_DIR / "staging" / m)

        logger.info("--- Building Dimension Layer ---")
        dim_models = [
            "dim_date.sql",
            "dim_product.sql",
            "dim_warehouse.sql",
            "dim_carrier.sql"
        ]
        for m in dim_models:
            execute_sql_file(con, SQL_DIR / "dimensions" / m)

        logger.info("--- Building Fact & Data Mart Layer ---")
        mart_models = [
            "fact_order_fulfillment.sql",
            "fact_daily_product_sales.sql",
            "analytics_views.sql"
        ]
        for m in mart_models:
            execute_sql_file(con, SQL_DIR / "marts" / m)

        logger.info("--- Data Mart Transformation Verification ---")
        tables = [
            "dim_date", "dim_product", "dim_warehouse", "dim_carrier",
            "fact_order_fulfillment", "fact_daily_product_sales"
        ]
        for tbl in tables:
            cnt = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            logger.info(f"Table [{tbl}]: {cnt:,} records created.")

        logger.info("Exporting analytical Parquet artifacts to data/processed/ ...")
        p_daily = str(PROCESSED_DATA_DIR / "fact_daily_product_sales.parquet").replace("\\", "/")
        p_ful = str(PROCESSED_DATA_DIR / "fact_order_fulfillment.parquet").replace("\\", "/")
        p_prod = str(PROCESSED_DATA_DIR / "dim_product.parquet").replace("\\", "/")
        p_wh = str(PROCESSED_DATA_DIR / "dim_warehouse.parquet").replace("\\", "/")
        p_cr = str(PROCESSED_DATA_DIR / "dim_carrier.parquet").replace("\\", "/")
        p_dt = str(PROCESSED_DATA_DIR / "dim_date.parquet").replace("\\", "/")

        con.execute(f"COPY fact_daily_product_sales TO '{p_daily}' (FORMAT PARQUET, COMPRESSION ZSTD);")
        con.execute(f"COPY fact_order_fulfillment TO '{p_ful}' (FORMAT PARQUET, COMPRESSION ZSTD);")
        con.execute(f"COPY dim_product TO '{p_prod}' (FORMAT PARQUET, COMPRESSION ZSTD);")
        con.execute(f"COPY dim_warehouse TO '{p_wh}' (FORMAT PARQUET, COMPRESSION ZSTD);")
        con.execute(f"COPY dim_carrier TO '{p_cr}' (FORMAT PARQUET, COMPRESSION ZSTD);")
        con.execute(f"COPY dim_date TO '{p_dt}' (FORMAT PARQUET, COMPRESSION ZSTD);")

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"Data Mart build pipeline completed successfully in {elapsed} seconds.")

    finally:
        con.close()

if __name__ == "__main__":
    run_transformations()
