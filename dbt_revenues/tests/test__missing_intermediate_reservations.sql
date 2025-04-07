-- Set to warn to proceed with missing data, error otherwise
{{ config(
    severity='error'
) }}

WITH reservation_data AS (
    SELECT reservation_id FROM {{ ref('stg__reservation_data') }}
),

intermediate_reservations AS (
    SELECT reservation_id FROM {{ ref('int__reservations_with_currency_rates') }})

SELECT
    i.reservation_id,
    s.reservation_id AS stg_reservation_id
FROM reservation_data s
LEFT JOIN intermediate_reservations i
  ON i.reservation_id = s.reservation_id
WHERE i.reservation_id IS NULL