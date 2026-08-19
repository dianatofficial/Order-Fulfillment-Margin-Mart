-- Dimension: Carrier
CREATE OR REPLACE TABLE dim_carrier AS
SELECT
    ROW_NUMBER() OVER (ORDER BY carrier_id) AS carrier_key,
    carrier_id,
    carrier_name,
    service_level,
    sla_contract_days,
    base_tariff,
    cost_per_kg,
    reliability_score,
    CASE 
        WHEN sla_contract_days = 1 THEN 'Next-Day Express'
        WHEN sla_contract_days = 2 THEN '2-Day Priority'
        WHEN sla_contract_days = 3 THEN '3-Day Standard'
        ELSE '5-Day Freight Economy'
    END AS speed_category,
    CURRENT_TIMESTAMP AS dwh_updated_at
FROM stg_carriers;
