{% docs stg__currency_rates %}
This staging model extracts and transforms raw currency rate data, formatting exchange dates, base currencies, currencies, and rates for downstream transformations.

Columns description:
- exchange_date: The date for which the exchange rate is applicable.
- base_currency: The base currency used for conversion.
- currency: The foreign currency for which the exchange rate is provided.
- rate: The conversion rate from the base currency to the foreign currency.
{% enddocs %}
