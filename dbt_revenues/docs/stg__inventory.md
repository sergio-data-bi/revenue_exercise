{% docs stg__inventory %}
This staging model loads and cleans inventory data, capturing property and inventory identifiers, inventory names, and availability for further integration with reservation data.

Columns description (from source README.md):
- inventory_id: the identifier for the room type the reservation has been booked for 
- property_id: the property identifier for the reservation record
- inventory_name: the name for the room type
- availability: the number of available rooms in each room type in the property
{% enddocs %}