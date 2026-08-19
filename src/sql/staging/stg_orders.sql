-- Staging: Orders
CREATE OR REPLACE TABLE stg_orders AS
SELECT
    CAST(order_id AS VARCHAR) AS order_id,
    CAST(customer_id AS VARCHAR) AS customer_id,
    CAST(order_channel AS VARCHAR) AS order_channel,
    CAST(order_placed_at AS TIMESTAMP) AS order_placed_at,
    CAST(order_placed_at AS DATE) AS order_date,
    CAST(gross_order_amount AS DECIMAL(12, 2)) AS gross_order_amount,
    CAST(total_discount_amount AS DECIMAL(12, 2)) AS total_discount_amount,
    CAST(net_order_amount AS DECIMAL(12, 2)) AS net_order_amount,
    CAST(order_status AS VARCHAR) AS order_status
FROM raw_orders;
