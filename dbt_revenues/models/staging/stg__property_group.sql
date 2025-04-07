WITH property_group AS (
    SELECT * FROM {{ source('raw', 'property_group') }}
)
SELECT
    property_group_id,
    property_group_name,
    base_currency,
    created_at
FROM
    property_group