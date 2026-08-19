import pytest
import duckdb
from src.config import DUCKDB_PATH

@pytest.fixture(scope="module")
def db_conn():
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    yield con
    con.close()

def test_dimensions_have_records(db_conn):
    for table in ["dim_product", "dim_warehouse", "dim_carrier", "dim_date"]:
        cnt = db_conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert cnt > 0, f"Table {table} is empty!"

def test_facts_have_records(db_conn):
    for table in ["fact_order_fulfillment", "fact_daily_product_sales"]:
        cnt = db_conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert cnt > 0, f"Table {table} is empty!"

def test_foreign_key_referential_integrity(db_conn):
    # Check orphaned product_keys
    orphan_prods = db_conn.execute("""
        SELECT COUNT(*) 
        FROM fact_daily_product_sales f
        LEFT JOIN dim_product d ON f.product_key = d.product_key
        WHERE d.product_key IS NULL
    """).fetchone()[0]
    assert orphan_prods == 0, f"Found {orphan_prods} orphaned product keys in fact table."

    # Check orphaned warehouse_keys
    orphan_whs = db_conn.execute("""
        SELECT COUNT(*) 
        FROM fact_daily_product_sales f
        LEFT JOIN dim_warehouse d ON f.warehouse_key = d.warehouse_key
        WHERE d.warehouse_key IS NULL
    """).fetchone()[0]
    assert orphan_whs == 0, f"Found {orphan_whs} orphaned warehouse keys in fact table."

    # Check orphaned carrier_keys
    orphan_crs = db_conn.execute("""
        SELECT COUNT(*) 
        FROM fact_daily_product_sales f
        LEFT JOIN dim_carrier d ON f.carrier_key = d.carrier_key
        WHERE d.carrier_key IS NULL
    """).fetchone()[0]
    assert orphan_crs == 0, f"Found {orphan_crs} orphaned carrier keys in fact table."

    # Check orphaned date_keys
    orphan_dates = db_conn.execute("""
        SELECT COUNT(*) 
        FROM fact_daily_product_sales f
        LEFT JOIN dim_date d ON f.date_key = d.date_key
        WHERE d.date_key IS NULL
    """).fetchone()[0]
    assert orphan_dates == 0, f"Found {orphan_dates} orphaned date keys in fact table."
