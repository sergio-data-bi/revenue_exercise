WITH reservation_revenues AS (
    SELECT * FROM {{ ref('int__reservations_with_currency_rates') }}
)

SELECT
    property_group_id,
    property_group_name,
    stay_date,
    base_currency,
    SUM(net_revenue_base_currency) AS total_revenue_base_currency,
    COUNT(DISTINCT reservation_id) AS reservations
FROM reservation_revenues
GROUP BY
    property_group_id,
    property_group_name,
    stay_date,
    base_currency