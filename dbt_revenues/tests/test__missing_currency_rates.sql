-- Set to warn to proceed with missing data, error otherwise
{{ config(
    severity='error'
) }}

WITH reservation_data AS (
    SELECT * FROM {{ ref('stg__reservation_data') }}
),
property_group AS (
    SELECT * FROM {{ ref('stg__property_group') }}
),
currency_rates AS (
    SELECT * FROM {{ ref('stg__currency_rates') }}
)

SELECT
    r.reservation_id,
    r.local_currency,
    pg.base_currency,
    cr.rate
FROM reservation_data r
JOIN property_group pg
    ON r.property_group_id = pg.property_group_id
LEFT JOIN currency_rates cr
    ON r.stay_date = cr.exchange_date
   AND r.local_currency = cr.local_currency
   AND pg.base_currency = cr.base_currency
WHERE r.local_currency <> pg.base_currency  -- Only reservations needing conversion
  AND cr.rate IS NULL  -- Missing currency rate
