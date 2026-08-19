-- Fact: Daily Product Sales Aggregated Mart
CREATE OR REPLACE TABLE fact_daily_product_sales AS
SELECT
    order_date_key AS date_key,
    product_key,
    warehouse_key,
    carrier_key,
    -- Volume & Transactional Counts
    COUNT(DISTINCT order_id) AS total_orders_count,
    COUNT(order_item_id) AS total_line_items_count,
    SUM(quantity) AS total_units_sold,
    -- Financial Measures
    ROUND(SUM(gross_line_amount), 2) AS gross_revenue,
    ROUND(SUM(discount_amount), 2) AS total_discounts_amount,
    ROUND(SUM(net_line_amount), 2) AS net_revenue,
    ROUND(SUM(total_line_cost), 2) AS total_cogs,
    ROUND(SUM(item_shipping_allocated_cost), 2) AS total_allocated_shipping_cost,
    ROUND(SUM(gross_margin_amount), 2) AS gross_margin_amount,
    ROUND((SUM(gross_margin_amount) / NULLIF(SUM(net_line_amount), 0)) * 100.0, 2) AS gross_margin_pct,
    -- Supply Chain & SLA Measures
    SUM(is_delayed_delivery) AS total_delayed_shipments,
    SUM(is_delayed_dispatch) AS total_delayed_dispatches,
    ROUND(((COUNT(order_item_id) - SUM(is_delayed_delivery)) * 100.0) / NULLIF(COUNT(order_item_id), 0), 2) AS on_time_delivery_rate_pct,
    ROUND(AVG(dispatch_latency_hours), 2) AS avg_dispatch_latency_hours,
    ROUND(AVG(transit_time_days), 2) AS avg_transit_time_days,
    ROUND(AVG(delivery_delay_days), 2) AS avg_delivery_delay_days,
    ROUND(AVG(total_fulfillment_cycle_days), 2) AS avg_total_cycle_days
FROM fact_order_fulfillment
GROUP BY 
    order_date_key,
    product_key,
    warehouse_key,
    carrier_key;
