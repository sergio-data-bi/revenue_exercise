{% docs stg__reservation_data %}
This staging model processes raw reservation data to calculate net revenues for analysis.


Columns description (from source README.md):
- reservation_id (PK): the unique identifier for a reservation record
- stay_date: date which the reservation has been booked for 
- booking_date: date which the reservation was booked/created 
- property_id: the property identifier for the reservation record
- property_name: the property name for the reservation record
- inventory_id: the identifier for the room type the reservation has been booked for 
- property_group_id: the property group identifier which the property belongs to
- property_group_name: the property group name which the property belongs to
- currency: the currency the reservation has been booked in (corresponding to the local currency of the property)
- net_revenue: the nightly revenue attributed to each stay_date for this reservation 
{% enddocs %}