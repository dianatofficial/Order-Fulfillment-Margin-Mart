-- Staging: Fulfillments
CREATE OR REPLACE TABLE stg_fulfillments AS
SELECT
    CAST(fulfillment_id AS VARCHAR) AS fulfillment_id,
    CAST(order_id AS VARCHAR) AS order_id,
    CAST(warehouse_id AS VARCHAR) AS warehouse_id,
    CAST(carrier_id AS VARCHAR) AS carrier_id,
    CAST(order_placed_at AS TIMESTAMP) AS order_placed_at,
    CAST(dispatched_at AS TIMESTAMP) AS dispatched_at,
    CAST(promised_delivery_date AS TIMESTAMP) AS promised_delivery_date,
    CAST(delivered_at AS TIMESTAMP) AS delivered_at,
    CAST(shipping_cost AS DECIMAL(10, 2)) AS shipping_cost,
    CAST(package_weight_kg AS DECIMAL(8, 2)) AS package_weight_kg,
    CAST(fulfillment_status AS VARCHAR) AS fulfillment_status
FROM raw_fulfillments;
