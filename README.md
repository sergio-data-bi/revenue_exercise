# Currency Revenue Data Pipeline

## Project description
Implementation of a data pipeline to extract, load and transform hotel reservation data, foreign currency exchange rates and property information to compute figures and metrics in both local and group currencies.
Ultimately to be easily consumed and displayed in a BI tool.

Source documentation: [source_data/README.md](source_data/README.md)

## Problem Statement
Hotel management groups operate across multiple regions and currencies, creating complexity in financial reporting and analysis.
Reservations are booked in various local currencies, but revenue reporting must often be consolidated into a single, consistent group currency for accurate financial insights and strategic decision-making.
Without a reliable and automated solution, accurately converting currencies, aggregating revenues, and maintaining timely analytics becomes error-prone and inefficient, impacting business agility and clarity.

## Solution
This project provides an automated data pipeline solution leveraging Python, DuckDB, and dbt, extracting currency data from [freecurrencyapi.com](https://freecurrencyapi.com/), enriching the source data and visualise the result in a Streamlit dashboard:
[Published Streamlit dashboard link](https://sergio-data-bi-revenue-exercise-streamlit-app-eqiffi.streamlit.app/)
[Open dbt Generated Documentation](https://sergio-data-bi.github.io/revenue_exercise)

### Workflow
- Extracts and loads raw reservation, property group, and inventory data from source CSV files into DuckDB.
- Retrieves and stores historical currency exchange rates from external APIs, taking into account throttling and extraction frequency limits.
- Utilizes dbt for structured data transformation:
  - Staging models standardize incoming data.
  - Intermediate models enrich reservations with currency rates to compute revenues in both local and group currencies.
  - Aggregation models summarize revenue metrics by inventory, property, and property group dimensions.
- Presents the final data in an accessible and intuitive format through BI visualization tools, such as Streamlit, supporting actionable business intelligence and streamlined financial reporting.


## Project structure
- `dbt_revenues/`: Main dbt project directory
  - `docs/`: Markdown documentation for dbt models
  - `models/`: Core dbt models (staging, intermediate, aggregations)
- `extraction/`: Python modules for retrieving currency rates based on source data
- `source_data/`: Contains source data and `README.md` with source data descriptions
- `scripts/`: Utility scripts
- `streamlit_app.py`: For generating the Revenue Dashboard web app
- `extract_and_load.py`: Extract and load the source CSV data and the API currency rates into DuckDB

# dbt local user profiles.yml configuration
```
dbt_revenues:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: dev.duckdb
      schema: main
```

## Run instructions
```
pip install -r requirements.txt

python extract_and_load.py

dbt build --project-dir dbt_revenues

streamlit run streamlit_app.py

# dbt documentation
dbt docs generate --project-dir dbt_revenues
dbt docs serve --project-dir dbt_revenues
```

## Get Started
Use as initial template or in a Jupyter notebook
```
import duckdb

conn = duckdb.connect("dev.duckdb")
df = conn.query("SELECT * FROM agg__revenue_by_property").to_df()
conn.close()
df
```

## Requirements
* duckdb
* dbt
* pandas
* streamlit
* altair (custom plotting)