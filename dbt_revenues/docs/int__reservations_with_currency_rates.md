{% docs int__reservations_with_currency_rates %}
This intermediate model enriches reservation data when currency rates are available, enabling revenue analysis of net revenue in both base and group currency for each reservation.

2025-04-07: The model excludes the dates when the currency rates are not available, also when the local currency is equal to the base currency.
This to maintain consistency when consuming and displaying the data.


{% enddocs %}