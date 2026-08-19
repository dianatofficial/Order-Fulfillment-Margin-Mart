-- Staging: Carriers
CREATE OR REPLACE TABLE stg_carriers AS
SELECT
    CAST(carrier_id AS VARCHAR) AS carrier_id,
    CAST(carrier_name AS VARCHAR) AS carrier_name,
    CAST(service_level AS VARCHAR) AS service_level,
    CAST(sla_contract_days AS INTEGER) AS sla_contract_days,
    CAST(base_tariff AS DECIMAL(10, 2)) AS base_tariff,
    CAST(cost_per_kg AS DECIMAL(10, 2)) AS cost_per_kg,
    CAST(reliability_score AS DECIMAL(5, 2)) AS reliability_score
FROM raw_carriers;
