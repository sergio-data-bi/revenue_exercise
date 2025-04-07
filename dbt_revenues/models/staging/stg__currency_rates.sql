WITH currency_rates AS (
    SELECT * FROM {{ source('raw', 'currency_rates') }}
)
SELECT
    exchange_date,
    base_currency,
    local_currency,
    rate
FROM
    currency_rates