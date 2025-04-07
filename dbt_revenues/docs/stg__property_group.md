{% docs stg__property_group %}
This staging model processes property group data, standardizing group identifiers, names, base currencies, and creation dates to support revenue calculations.

Columns description (from source README.md):
- property_group_id: the property group identifier which the property belongs to
- property_group_name: the property group name which the property belongs to
- base_currency: the property groups’ base currency, used for reporting on revenue figures on a group level
- created_at: when the property group was first created
{% enddocs %}