WITH reservation_data AS (
    SELECT * FROM {{ source('raw', 'reservation_data') }}
)
SELECT
    property_id,
    property_name,
    property_group_id,
    property_group_name,
    inventory_id,
    reservation_id,
    stay_date,
    booking_date,
    currency AS local_currency,
    net_revenue
FROM
    reservation_data