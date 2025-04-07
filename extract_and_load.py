import os
from pathlib import Path
import duckdb
import freecurrencyapi

from extraction.currency_rates import extract_and_load_currency_rates
from extraction.source_data import generate_currency_extraction_params_from_db
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

FREE_CURRENCY_API_KEY = os.environ.get("FREE_CURRENCY_API_KEY")

SOURCE_DATA_PATH = Path("source_data")
DUCKDB_FILE = "dev.duckdb"

# 2025-04-07: Hard-coding 'EUR' as the code has only been tested with this base currency.
BASE_CURRENCY = 'EUR'


def source_data_to_db(conn) -> None:
    """ Extract the CSV files in source_data and load them into the db."""
    for name in ['inventory', 'property_group', 'reservation_data']:
        file = SOURCE_DATA_PATH / f"{name}.csv"
        logging.info(f"Loading {file} into {name} db table...")
        conn.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto('{file}')")


def currency_rates_to_db(conn) -> None:
    """ Extract currency rates from the free currency API and load them into the db."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS currency_rates (
            exchange_date DATE,
            base_currency VARCHAR,
            local_currency VARCHAR,
            rate DOUBLE,
            PRIMARY KEY (exchange_date, base_currency, local_currency)
        )
    """)
    foreign_currencies, exchange_dates = generate_currency_extraction_params_from_db(
        conn=conn,
        base_currency=BASE_CURRENCY,
        exclude_already_stored_dates=True
    )

    if not exchange_dates:
        logging.info(f'Data for {foreign_currencies} already stored in {DUCKDB_FILE}')
    else:
        if not FREE_CURRENCY_API_KEY:
            raise ValueError("FREE_CURRENCY_API_KEY environment variable not set")
        client = freecurrencyapi.Client(FREE_CURRENCY_API_KEY)
        extract_and_load_currency_rates(client=client,
                                        conn=conn,
                                        base_currency=BASE_CURRENCY,
                                        foreign_currencies=foreign_currencies,
                                        exchange_dates=exchange_dates,
                                        logging=logging)


def main():
    with duckdb.connect(DUCKDB_FILE) as conn:
        source_data_to_db(conn)
        currency_rates_to_db(conn)


if __name__ == "__main__":
    main()
