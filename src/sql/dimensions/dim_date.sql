-- Dimension: Date
CREATE OR REPLACE TABLE dim_date AS
WITH date_series AS (
    SELECT 
        CAST('2024-01-01' AS DATE) + INTERVAL (d) DAY AS full_date
    FROM generate_series(0, 1095) AS t(d)
)
SELECT
    CAST(strftime(full_date, '%Y%m%d') AS INTEGER) AS date_key,
    full_date,
    EXTRACT(YEAR FROM full_date) AS calendar_year,
    EXTRACT(QUARTER FROM full_date) AS calendar_quarter,
    'Q' || EXTRACT(QUARTER FROM full_date) AS quarter_name,
    EXTRACT(MONTH FROM full_date) AS month_number,
    strftime(full_date, '%B') AS month_name,
    strftime(full_date, '%b') AS month_short,
    EXTRACT(DAY FROM full_date) AS day_of_month,
    EXTRACT(DOW FROM full_date) AS day_of_week_number,
    strftime(full_date, '%A') AS day_of_week_name,
    strftime(full_date, '%a') AS day_of_week_short,
    CASE WHEN EXTRACT(DOW FROM full_date) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend,
    CASE 
        WHEN EXTRACT(MONTH FROM full_date) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM full_date) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM full_date) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END AS season,
    'FY' || EXTRACT(YEAR FROM full_date) || '-P' || LPAD(CAST(EXTRACT(MONTH FROM full_date) AS VARCHAR), 2, '0') AS fiscal_period
FROM date_series;
