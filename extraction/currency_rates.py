from datetime import time
import time

REQUESTS_PER_MINUTE_THRESHOLD = 10


def extract_and_load_currency_rates(client,
                                    conn,
                                    base_currency,
                                    foreign_currencies,
                                    exchange_dates,
                                    logging) -> None:
    """
    Handles the extraction and loading of historical currency exchange rates from a client API
    to a database adhering to the API's request rate limits.

    This function retrieves historical exchange rates for a specified base currency against
    multiple foreign currencies on given exchange dates. For each exchange date, the function
    fetches the rate data, and inserts or updates the rate in the database. The function ensures that
    request thresholds are respected, introducing delays as necessary to conform to API rate limits.

    :param client: API client instance to fetch historical exchange rate data from freecurrencyapi.com
    :param conn: DuckDB database connection object.
    :param base_currency: The currency code (e.g., 'EUR') representing the base currency for which
        exchange rates are being retrieved.
    :param foreign_currencies: A list of currency codes representing the foreign currencies to retrieve rates for.
    :param exchange_dates: A list of datetime.date objects representing the dates for which to fetch
        historical currency rates.
    :param logging: Logging instance.
    :return: None
    """

    requests_made = 0
    start_time = time.time()

    for exchange_date in exchange_dates:
        if requests_made >= REQUESTS_PER_MINUTE_THRESHOLD:
            elapsed_time = time.time() - start_time
            if elapsed_time < 60:
                wait_time = 60 - elapsed_time
                logging.info(f"Reached {REQUESTS_PER_MINUTE_THRESHOLD} requests, waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            requests_made = 0
            start_time = time.time()

        logging.info(f"Fetching data for {exchange_date}...")
        response = client.historical(exchange_date, base_currency, foreign_currencies)

        exchange_date_str = exchange_date.strftime('%Y-%m-%d')
        if 'data' in response:
            record = response['data'].get(exchange_date_str)
            for local_currency, rate in record.items():
                conn.execute(
                    """
                    INSERT INTO currency_rates (exchange_date, base_currency, local_currency, rate)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT (exchange_date, base_currency, local_currency)
                    DO UPDATE SET rate = EXCLUDED.rate
                    """,
                    (exchange_date_str, base_currency, local_currency, rate)
                )
            logging.info(f"Stored {exchange_date_str}: {record}\n")
        else:
            error_message = response.get('message', 'Unknown error')
            logging.error(f"API error: {error_message}")
            break
        requests_made += 1
