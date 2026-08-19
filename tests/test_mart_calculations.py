import pytest
import duckdb
from src.config import DUCKDB_PATH

@pytest.fixture(scope="module")
def db_conn():
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    yield con
    con.close()

def test_gross_margin_mathematical_identity(db_conn):
    # Verify gross_margin_amount = net_revenue - total_cogs - total_allocated_shipping_cost
    mismatches = db_conn.execute("""
        SELECT COUNT(*)
        FROM fact_daily_product_sales
        WHERE ABS(gross_margin_amount - (net_revenue - total_cogs - total_allocated_shipping_cost)) > 0.05
    """).fetchone()[0]
    assert mismatches == 0, f"Found {mismatches} margin calculation discrepancies!"

def test_net_revenue_identity(db_conn):
    mismatches = db_conn.execute("""
        SELECT COUNT(*)
        FROM fact_daily_product_sales
        WHERE ABS(net_revenue - (gross_revenue - total_discounts_amount)) > 0.05
    """).fetchone()[0]
    assert mismatches == 0, f"Found {mismatches} net revenue calculation discrepancies!"

def test_on_time_delivery_rate_bounds(db_conn):
    invalid_rates = db_conn.execute("""
        SELECT COUNT(*)
        FROM fact_daily_product_sales
        WHERE on_time_delivery_rate_pct < 0.0 OR on_time_delivery_rate_pct > 100.0
    """).fetchone()[0]
    assert invalid_rates == 0, f"Found {invalid_rates} invalid SLA delivery percentages!"

def test_fulfillment_latency_non_negative(db_conn):
    neg_latencies = db_conn.execute("""
        SELECT COUNT(*)
        FROM fact_order_fulfillment
        WHERE dispatch_latency_hours < 0 OR transit_time_days < 0
    """).fetchone()[0]
    assert neg_latencies == 0, f"Found {neg_latencies} negative latency records!"
