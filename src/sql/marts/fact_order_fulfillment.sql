-- Fact: Order Fulfillment (Granular line-item / package level)
CREATE OR REPLACE TABLE fact_order_fulfillment AS
WITH raw_joined AS (
    SELECT
        f.fulfillment_id,
        f.order_id,
        i.order_item_id,
        CAST(strftime(f.order_placed_at, '%Y%m%d') AS INTEGER) AS order_date_key,
        CAST(strftime(f.dispatched_at, '%Y%m%d') AS INTEGER) AS dispatch_date_key,
        CAST(strftime(f.delivered_at, '%Y%m%d') AS INTEGER) AS delivery_date_key,
        dp.product_key,
        dw.warehouse_key,
        dc.carrier_key,
        f.order_placed_at,
        f.dispatched_at,
        f.promised_delivery_date,
        f.delivered_at,
        i.quantity,
        i.unit_price,
        i.unit_cost,
        i.gross_line_amount,
        i.discount_amount,
        i.line_total_amount,
        i.total_line_cost,
        -- Allocate shipment cost proportionally based on item net revenue
        ROUND(f.shipping_cost * (i.line_total_amount / NULLIF(o.net_order_amount, 0)), 2) AS item_shipping_allocated_cost,
        dc.sla_contract_days AS sla_target_days
    FROM stg_fulfillments f
    JOIN stg_orders o ON f.order_id = o.order_id
    JOIN stg_order_items i ON f.order_id = i.order_id
    JOIN dim_product dp ON i.product_id = dp.product_id
    JOIN dim_warehouse dw ON f.warehouse_id = dw.warehouse_id
    JOIN dim_carrier dc ON f.carrier_id = dc.carrier_id
)
SELECT
    ROW_NUMBER() OVER (ORDER BY order_placed_at, order_id, order_item_id) AS fulfillment_key,
    order_id,
    order_item_id,
    order_date_key,
    dispatch_date_key,
    delivery_date_key,
    product_key,
    warehouse_key,
    carrier_key,
    order_placed_at,
    dispatched_at,
    promised_delivery_date,
    delivered_at,
    quantity,
    unit_price,
    unit_cost,
    gross_line_amount,
    discount_amount,
    line_total_amount AS net_line_amount,
    total_line_cost,
    item_shipping_allocated_cost,
    -- Financial Margin Calculations
    ROUND(line_total_amount - total_line_cost - item_shipping_allocated_cost, 2) AS gross_margin_amount,
    ROUND(((line_total_amount - total_line_cost - item_shipping_allocated_cost) / NULLIF(line_total_amount, 0)) * 100.0, 2) AS gross_margin_pct,
    -- Timing & Latency Metrics
    ROUND(date_diff('second', order_placed_at, dispatched_at) / 3600.0, 2) AS dispatch_latency_hours,
    ROUND(date_diff('second', dispatched_at, delivered_at) / 86400.0, 2) AS transit_time_days,
    ROUND(date_diff('second', order_placed_at, delivered_at) / 86400.0, 2) AS total_fulfillment_cycle_days,
    sla_target_days,
    ROUND(GREATEST(0.0, (date_diff('second', dispatched_at, delivered_at) / 86400.0) - sla_target_days), 2) AS delivery_delay_days,
    CASE 
        WHEN (date_diff('second', dispatched_at, delivered_at) / 86400.0) > sla_target_days THEN 1 
        ELSE 0 
    END AS is_delayed_delivery,
    CASE 
        WHEN (date_diff('second', order_placed_at, dispatched_at) / 3600.0) > 24.0 THEN 1 
        ELSE 0 
    END AS is_delayed_dispatch,
    CASE 
        WHEN (date_diff('second', dispatched_at, delivered_at) / 86400.0) <= sla_target_days THEN 'On-Time'
        WHEN (date_diff('second', dispatched_at, delivered_at) / 86400.0) <= sla_target_days + 1.0 THEN 'Minor Delay (<24h)'
        ELSE 'Severe Delay (>24h)'
    END AS sla_compliance_status
FROM raw_joined;
