{% docs __overview__ %}
# dbt Revenues Project Overview

This project transforms and aggregates hotel reservation data, currency exchange rates, and property details to calculate revenue metrics in both local and group currencies.  
The output is structured for analysis and easy visualization in BI tools.

## Staging Models
- [stg__reservation_data](#!/model/model.dbt_revenues.stg__reservation_data): Raw reservation data.
- [stg__inventory](#!/model/model.dbt_revenues.stg__inventory): Property inventory details.
- [stg__property_group](#!/model/model.dbt_revenues.stg__property_group): Property group information and base currencies.
- [stg__currency_rates](#!/model/model.dbt_revenues.stg__currency_rates): External currency exchange rate data.

## Intermediate Models
- [int__reservations_with_currency_rates](#!/model/model.dbt_revenues.int__reservations_with_currency_rates): Enriches reservations with currency exchange rates for revenue aggregations and analytics.

## Aggregation Models
- [agg__revenue_by_property_group](#!/model/model.dbt_revenues.agg__revenue_by_property_group): Computes summarized revenue figures per hotel group.
- [agg__revenue_by_property](#!/model/model.dbt_revenues.agg__revenue_by_property): Calculates revenue totals for individual properties in local and group currency.
- [agg__revenue_by_inventory](#!/model/model.dbt_revenues.agg__revenue_by_inventory): Aggregates total revenue by room inventory type for each property.

## Tests

- [test__missing_currency_rates](#!/test/test.dbt_revenues.test__missing_currency_rates): Ensures all reservations requiring currency conversion have corresponding currency exchange rates.

- [test__missing_intermediate_reservations](#!/test/test.dbt_revenues.test__missing_intermediate_reservations): Verifies that the intermediate reservations model accurately incorporates all staged reservation records, ensuring data integrity.

{% enddocs %}
