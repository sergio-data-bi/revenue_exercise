-- Set to warn to proceed with missing data, error otherwise
{{ config(
    severity='error'
) }}

WITH int_row_count AS (
    SELECT COUNT(*) AS row_count
    FROM {{ ref('int__reservations_with_currency_rates') }}
),
stg_row_count AS (
    SELECT COUNT(*) AS row_count
    FROM {{ ref('stg__reservation_data') }}
)
SELECT
    int_row_count.row_count AS int_row_count,
    stg_row_count.row_count AS stg_row_count
FROM int_row_count, stg_row_count
WHERE int_row_count.row_count <> stg_row_count.row_count