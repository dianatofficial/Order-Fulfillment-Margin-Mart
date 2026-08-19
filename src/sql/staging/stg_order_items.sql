-- Staging: Order Items
CREATE OR REPLACE TABLE stg_order_items AS
SELECT
    CAST(order_item_id AS VARCHAR) AS order_item_id,
    CAST(order_id AS VARCHAR) AS order_id,
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(unit_price AS DECIMAL(10, 2)) AS unit_price,
    CAST(unit_cost AS DECIMAL(10, 2)) AS unit_cost,
    CAST(discount_amount AS DECIMAL(10, 2)) AS discount_amount,
    CAST(line_total_amount AS DECIMAL(12, 2)) AS line_total_amount,
    CAST(quantity * unit_cost AS DECIMAL(12, 2)) AS total_line_cost,
    CAST(quantity * unit_price AS DECIMAL(12, 2)) AS gross_line_amount
FROM raw_order_items;
