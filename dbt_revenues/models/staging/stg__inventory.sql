WITH inventory AS (
    SELECT * FROM {{ source('raw', 'inventory') }}
)
SELECT
    property_id,
    inventory_id,
    inventory_name,
    availability
FROM
    inventory