{% docs test__missing_intermediate_reservations %}
# Test: Missing Intermediate Reservations

This test verifies that every reservation in the intermediate model (`int__reservations_with_currency_rates`) has a matching record in the staging model (`stg__reservation_data`).

**Logic:**

- **Join and Filter:**
  A LEFT JOIN is performed on `reservation_id`. The test filters for rows where the staging reservation is missing (`s.reservation_id IS NULL`).

- **Expected Outcome:**
  The query should return zero rows. Any returned rows indicate that there are reservations in the intermediate model without a corresponding staging record.

{% enddocs %}
