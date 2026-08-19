-- Staging: Products
CREATE OR REPLACE TABLE stg_products AS
SELECT
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(product_name AS VARCHAR) AS product_name,
    CAST(category AS VARCHAR) AS category,
    CAST(unit_cost AS DECIMAL(10, 2)) AS unit_cost,
    CAST(list_price AS DECIMAL(10, 2)) AS list_price,
    CAST(weight_kg AS DECIMAL(8, 2)) AS weight_kg,
    CAST(is_hazardous AS BOOLEAN) AS is_hazardous
FROM raw_products;
