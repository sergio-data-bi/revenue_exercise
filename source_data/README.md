## Summary
At Bookboost, you will be responsible for data models that cover use cases spanning across multiple teams, from product, to analytics, to machine learning. In this take-home exercise, we wanted to give you a small taste of what a day in the life of a Data Engineer at Bookboost looks like whilst getting to know your skills and ways of working better.

None of your work will be used by Bookboost, the goal of this exercise is to showcase the way that you approach your work, and to build your understanding of our expectations in the role.

For this take home exercise, you will be working on a critical problem for our customer-facing analytics capability - **currency conversion**. The data pipeline you build should reliably calculate the net revenue figures for each reservation in the property's local currency as well as the property group's base currency. The property group's base currency reflects the currency in which the head office of a hotel group reports on their revenue data.

For the sake of clarity, a property represents an individual hotel and a property group represents a hotel group which owns one or more individual hotels.

## Data
In this repository, you will find an excerpt of example data from our Customer Data Platform. 

This data includes the following tables:

**reservation_data**:
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

**property_group**: 
- property_group_id: the property group identifier which the property belongs to
- property_group_name: the property group name which the property belongs to
- base_currency: the property groups’ base currency, used for reporting on revenue figures on a group level
- created_at: when the property group was first created

**inventory**:
- inventory_id: the identifier for the room type the reservation has been booked for 
- property_id: the property identifier for the reservation record
- inventory_name: the name for the room type
- availability: the number of available rooms in each room type in the property

## Expected Output
For this exercise, we would like you to build us a data pipeline which:

- Retrieves foreign currency exchange rates from a REST API endpoint.
   - Feel free to use a free foreign exchange rates API of your choosing (or use one of the APIs mentioned in the Guidance section below). 
- Stores the retrieved currency exchange rates in a storage format of your choice.
- Computes the net revenue figures in local and group currencies for each reservation record using the retrieved exchange rates.
- Calculates a net revenue metric in both currencies aggregated by inventory, property and property group dimensions using stay dates as the time axis.

Finally, we’d like this data visualised in a way that is easy to consume and present back during the technical interview. Feel free to display this data in any visualisation format you’d like - this is an opportunity for us to understand what your best practices are for displaying quantitative data.

## Guidance
We have no strict requirements on what tools you use to achieve this output, other than the fact that the data modeling should be done in SQL or Python and the results presented in a Business Intelligence tool of your choice.

Below is a list of free APIs, database and BI tools which you may find useful to complete this exercise (these are just suggestions, we don’t mind what tools you use):

- Preset (BI) - https://preset.io/ 
- Tableau Public (BI) - https://www.tableau.com/products/public 
- Streamlit (BI) - https://streamlit.io/ 
- PostgreSQL (SQL database) - https://www.postgresql.org/ 
- DuckDB (SQL database) - https://duckdb.org/
- Motherduck (Data Warehouse) - https://motherduck.com/ 
- Fixer API (Forex API) - https://fixer.io/ 
- Exchange Rates API (Forex API) - https://exchangeratesapi.io/ 
- CurrencyLayer (Forex API) - https://currencylayer.com/ 


We’d like you to submit this exercise at least 2 working days before the technical interview to allow for our team to review and formulate their questions. Please submit the pipeline you have built and any documentation you feel may be relevant to a public repository on GitHub and share this link with us via email (jesse.stanley@bookboost.io and daan@bookboost.io) when you are ready.

During the panel interview, we’d like you to walk through your work with our team. We’ll be asking questions to understand:

- The approach to consuming data from your chosen Forex Rest API
- The assumptions you have made of the source data
- The transformations you have written
- The presentation of the data to a technical and non-technical audience

Our expectation is that this exercise should take approximately 2 hours to complete thoroughly. Most importantly, we’d like to understand how you would tackle the data problem and present the results to a key business stakeholder. Thus, the final model and visualisations do not have to be perfect. 

Finally, have fun and we look forward to talking through your solutions!
