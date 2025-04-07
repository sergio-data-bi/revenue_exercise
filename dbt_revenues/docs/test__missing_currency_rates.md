{% docs test__missing_currency_rates %}
# Test: Missing Currency Rates

This custom test ensures that every reservation requiring currency conversion has an associated exchange rate available.

- **Logic:**
  - Join reservation data with property group data so we know when a conversion is needed (i.e. when the reservation’s local currency differs from the base currency).
  - Perform a left join with currency rates on `stay_date`, `local_currency`, and `base_currency`.
  - Identify records where the reservation requires a conversion but there is no corresponding currency rate

**Expected Outcome:**  
The test should return zero rows. If any rows are returned, it indicates that there are reservations missing the necessary currency exchange rates, which would cause the transformation process to be incomplete.

{% enddocs %}
