WITH reservations AS (
    SELECT * FROM {{ ref('stg__reservation_data') }}
),

property_groups AS (
    SELECT * FROM {{ ref('stg__property_group') }}
),

inventory AS (
    SELECT * FROM {{ ref('stg__inventory') }}
),

currency_rates AS (
    SELECT * FROM {{ ref('stg__currency_rates') }}
)

SELECT
    r.*,
    i.inventory_name,
    pg.base_currency,
    CASE
        WHEN r.local_currency = pg.base_currency THEN 1.0
        ELSE cr.rate
    END AS currency_rate,
    r.net_revenue * CASE
        WHEN r.local_currency = pg.base_currency THEN 1.0
        ELSE cr.rate
    END AS net_revenue_base_currency
FROM reservations r
LEFT JOIN property_groups pg
    ON r.property_group_id = pg.property_group_id
LEFT JOIN inventory i
    ON r.inventory_id = i.inventory_id
LEFT JOIN currency_rates cr
    ON r.stay_date = cr.exchange_date
    AND r.local_currency = cr.local_currency
    AND pg.base_currency = cr.base_currency
WHERE r.stay_date in (SELECT DISTINCT exchange_date FROM currency_rates WHERE rate IS NOT NULL)