-- Dimension: Warehouse
CREATE OR REPLACE TABLE dim_warehouse AS
SELECT
    ROW_NUMBER() OVER (ORDER BY warehouse_id) AS warehouse_key,
    warehouse_id,
    facility_name,
    city,
    state,
    region,
    capacity_units_per_day,
    CASE 
        WHEN capacity_units_per_day >= 18000 THEN 'Tier 1 Mega Hub'
        WHEN capacity_units_per_day >= 12000 THEN 'Tier 2 Regional Center'
        ELSE 'Tier 3 Spoke Node'
    END AS capacity_tier,
    automation_level,
    labor_shifts,
    CURRENT_TIMESTAMP AS dwh_updated_at
FROM stg_warehouses;
