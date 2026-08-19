import pytest
import duckdb
from src.config import DUCKDB_PATH

@pytest.fixture(scope="module")
def db_conn():
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    yield con
    con.close()

def test_primary_key_uniqueness(db_conn):
    tables_pk = [
        ("dim_product", "product_key"),
        ("dim_warehouse", "warehouse_key"),
        ("dim_carrier", "carrier_key"),
        ("dim_date", "date_key"),
        ("fact_order_fulfillment", "fulfillment_key")
    ]
    for table, pk in tables_pk:
        dup_count = db_conn.execute(f"""
            SELECT COUNT(*) - COUNT(DISTINCT {pk}) 
            FROM {table}
        """).fetchone()[0]
        assert dup_count == 0, f"Found duplicate primary keys in {table}.{pk}!"

def test_not_null_critical_columns(db_conn):
    null_checks = [
        ("fact_order_fulfillment", "order_id"),
        ("fact_order_fulfillment", "product_key"),
        ("fact_order_fulfillment", "warehouse_key"),
        ("fact_order_fulfillment", "carrier_key"),
        ("fact_daily_product_sales", "date_key"),
        ("fact_daily_product_sales", "gross_revenue"),
        ("fact_daily_product_sales", "gross_margin_amount")
    ]
    for table, col in null_checks:
        null_count = db_conn.execute(f"""
            SELECT COUNT(*) 
            FROM {table} 
            WHERE {col} IS NULL
        """).fetchone()[0]
        assert null_count == 0, f"Found NULL values in critical column {table}.{col}!"
