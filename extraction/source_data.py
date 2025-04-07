def query_one(conn, query):
    return conn.execute(query).fetchone()[0]


def generate_currency_extraction_params_from_db(conn, base_currency, exclude_already_stored_dates=True):
    """
    Generates currency extraction parameters from the database using the provided
    connection and base currency. This function constructs and executes a query
    to calculate the list of local currencies and their associated dates for
    which exchange rates need to be fetched. Optionally, it excludes dates
    that already have stored.

    :param conn: Database connection object used to execute the query.
    :param base_currency: The base currency code (e.g., 'EUR') used to filter
                          the results for local currencies and dates.
    :param exclude_already_stored_dates: A flag indicating whether to exclude
                                         dates for which exchange rates are
                                         already stored. Default is True.
    :return: A tuple containing two elements:
             1. List of local currencies.
             2. List of stay dates.
    :rtype: tuple[list[str], list[str]]
    """
    query = f"""
        WITH
            local_currencies AS (
                SELECT DISTINCT currency
                FROM reservation_data
                WHERE currency != '{base_currency}'
            ),
            relevant_dates AS (
                SELECT DISTINCT stay_date
                FROM reservation_data
                WHERE currency IN (SELECT currency FROM local_currencies)
            ),
            filtered_dates AS (
                SELECT stay_date
                FROM relevant_dates rd
                {f'''WHERE NOT EXISTS (
                    SELECT 1 FROM currency_rates cr
                    WHERE cr.exchange_date = rd.stay_date
                      AND cr.base_currency = '{base_currency}'
                      AND cr.local_currency IN (SELECT local_currency FROM local_currencies)
                )''' if exclude_already_stored_dates else ''}
            )
        SELECT
            (SELECT array_agg(currency) FROM local_currencies) AS local_currencies,
            (SELECT array_agg(stay_date ORDER BY stay_date) FROM filtered_dates) AS stay_dates
    """

    local_currencies, stay_dates = conn.execute(query).fetchone()
    return local_currencies, stay_dates


