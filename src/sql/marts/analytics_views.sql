-- Analytics Views for Supply Chain & Margin Reporting
CREATE OR REPLACE VIEW vw_executive_monthly_margin_summary AS
SELECT
    d.calendar_year,
    d.month_number,
    d.month_name,
    SUM(f.total_orders_count) AS total_orders,
    SUM(f.total_units_sold) AS total_units,
    ROUND(SUM(f.gross_revenue), 2) AS total_gross_revenue,
    ROUND(SUM(f.net_revenue), 2) AS total_net_revenue,
    ROUND(SUM(f.total_cogs), 2) AS total_cogs,
    ROUND(SUM(f.total_allocated_shipping_cost), 2) AS total_shipping_cost,
    ROUND(SUM(f.gross_margin_amount), 2) AS total_gross_margin,
    ROUND((SUM(f.gross_margin_amount) / NULLIF(SUM(f.net_revenue), 0)) * 100.0, 2) AS overall_margin_pct,
    ROUND(AVG(f.on_time_delivery_rate_pct), 2) AS avg_on_time_rate_pct,
    ROUND(AVG(f.avg_dispatch_latency_hours), 2) AS avg_dispatch_latency_hours
FROM fact_daily_product_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.calendar_year, d.month_number, d.month_name
ORDER BY d.calendar_year, d.month_number;

CREATE OR REPLACE VIEW vw_carrier_performance_scorecard AS
SELECT
    c.carrier_id,
    c.carrier_name,
    c.service_level,
    c.sla_contract_days,
    SUM(f.total_orders_count) AS total_shipments,
    SUM(f.total_delayed_shipments) AS delayed_shipments,
    ROUND(((SUM(f.total_line_items_count) - SUM(f.total_delayed_shipments)) * 100.0) / NULLIF(SUM(f.total_line_items_count), 0), 2) AS sla_compliance_rate_pct,
    ROUND(AVG(f.avg_transit_time_days), 2) AS actual_avg_transit_days,
    ROUND(AVG(f.avg_delivery_delay_days), 2) AS avg_delay_days_beyond_sla,
    ROUND(SUM(f.total_allocated_shipping_cost), 2) AS total_freight_spend,
    ROUND(SUM(f.total_allocated_shipping_cost) / NULLIF(SUM(f.total_units_sold), 0), 2) AS freight_cost_per_unit
FROM fact_daily_product_sales f
JOIN dim_carrier c ON f.carrier_key = c.carrier_key
GROUP BY c.carrier_id, c.carrier_name, c.service_level, c.sla_contract_days
ORDER BY sla_compliance_rate_pct DESC;

CREATE OR REPLACE VIEW vw_warehouse_dispatch_efficiency AS
SELECT
    w.warehouse_id,
    w.facility_name,
    w.region,
    w.capacity_tier,
    w.automation_level,
    SUM(f.total_orders_count) AS total_orders_fulfilled,
    SUM(f.total_units_sold) AS total_units_shipped,
    SUM(f.total_delayed_dispatches) AS delayed_dispatches_count,
    ROUND(AVG(f.avg_dispatch_latency_hours), 2) AS avg_dispatch_latency_hours,
    ROUND(((SUM(f.total_line_items_count) - SUM(f.total_delayed_dispatches)) * 100.0) / NULLIF(SUM(f.total_line_items_count), 0), 2) AS same_day_dispatch_rate_pct
FROM fact_daily_product_sales f
JOIN dim_warehouse w ON f.warehouse_key = w.warehouse_key
GROUP BY w.warehouse_id, w.facility_name, w.region, w.capacity_tier, w.automation_level
ORDER BY avg_dispatch_latency_hours ASC;

CREATE OR REPLACE VIEW vw_product_category_profitability AS
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS sku_count,
    SUM(f.total_units_sold) AS units_sold,
    ROUND(SUM(f.net_revenue), 2) AS net_revenue,
    ROUND(SUM(f.total_cogs), 2) AS total_cogs,
    ROUND(SUM(f.total_allocated_shipping_cost), 2) AS total_shipping_cost,
    ROUND(SUM(f.gross_margin_amount), 2) AS gross_profit_amount,
    ROUND((SUM(f.gross_margin_amount) / NULLIF(SUM(f.net_revenue), 0)) * 100.0, 2) AS category_margin_pct
FROM fact_daily_product_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY gross_profit_amount DESC;
