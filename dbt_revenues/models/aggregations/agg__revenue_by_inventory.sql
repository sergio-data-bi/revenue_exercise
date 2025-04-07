WITH reservation_revenues AS (
    SELECT * FROM {{ ref('int__reservations_with_currency_rates') }}
)

SELECT
    property_group_id,
    property_group_name,
    property_id,
    property_name,
    inventory_id,
    inventory_name,
    stay_date,
    base_currency,
    local_currency,
    SUM(net_revenue_base_currency) AS total_revenue_base_currency,
    SUM(net_revenue) AS total_revenue_local_currency,
    COUNT(DISTINCT reservation_id) AS reservations
FROM reservation_revenues
GROUP BY
    property_group_id,
    property_group_name,
    property_id,
    property_name,
    inventory_id,
    inventory_name,
    stay_date,
    base_currency,
    local_currency