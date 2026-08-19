-- Staging: Warehouses
CREATE OR REPLACE TABLE stg_warehouses AS
SELECT
    CAST(warehouse_id AS VARCHAR) AS warehouse_id,
    CAST(facility_name AS VARCHAR) AS facility_name,
    CAST(city AS VARCHAR) AS city,
    CAST(state AS VARCHAR) AS state,
    CAST(region AS VARCHAR) AS region,
    CAST(capacity_units_per_day AS INTEGER) AS capacity_units_per_day,
    CAST(automation_level AS VARCHAR) AS automation_level,
    CAST(labor_shifts AS INTEGER) AS labor_shifts
FROM raw_warehouses;
