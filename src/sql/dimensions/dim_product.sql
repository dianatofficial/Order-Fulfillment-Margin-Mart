-- Dimension: Product
CREATE OR REPLACE TABLE dim_product AS
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id) AS product_key,
    product_id,
    product_name,
    category,
    unit_cost,
    list_price,
    ROUND(list_price - unit_cost, 2) AS standard_margin_amount,
    ROUND(((list_price - unit_cost) / NULLIF(list_price, 0)) * 100.0, 2) AS target_margin_pct,
    CASE 
        WHEN ((list_price - unit_cost) / NULLIF(list_price, 0)) >= 0.60 THEN 'High Margin (>60%)'
        WHEN ((list_price - unit_cost) / NULLIF(list_price, 0)) >= 0.35 THEN 'Medium Margin (35-60%)'
        ELSE 'Low Margin (<35%)'
    END AS margin_tier,
    weight_kg,
    is_hazardous,
    CURRENT_TIMESTAMP AS dwh_updated_at
FROM stg_products;
