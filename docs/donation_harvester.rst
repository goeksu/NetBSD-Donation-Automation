.. _donation_harvester:

donation_harvester
==================

The Donation Harvester module is responsible for interacting with payment platforms like PayPal and Stripe to fetch new donations, manage these donations in a database, and optionally send notifications to donors. It provides a command-line interface for different operations like updating, listing, and exporting donations.

The module is designed to be run periodically, either manually or via a scheduler, to keep donation records up to date and maintain engagement with donors through timely communications.


app.py
------

This script is the main driver of the module, handling command-line inputs to trigger specific functionalities like fetching new donations, sending deferred emails, and exporting data. It leverages external APIs through `stripeapi.py` and `paypalapi.py`.

Parsing arguments to take action regarding to the given argument.

.. code-block:: python

    parser = argparse.ArgumentParser(description="Donation Update System.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    update_parser = subparsers.add_parser('update', help="Enables database insertion.")
    update_parser.add_argument("--paypal-only", action="store_true", \
        help="Fetches data only from Paypal.")
    update_parser.add_argument("--stripe-only", action="store_true", \
        help="Fetches data only from Stripe.")
    ...

Sending emails and storing them in deferred-email table in case of an issue.


.. code-block:: python

    def sendmail(donations: list) -> None:
    """
    This function send mails to the donors, and insert the failed ones into the database.
    """
    deferred = send_url_mail(donations)
    if deferred:
        logging.info("Inserting deferred emails into the database...")
        insert_deferred_email(deferred)
    ...

database.py
-----------

This script contains all database interactions, including fetching the latest donations, inserting new donation records, and managing deferred emails. It uses PostgreSQL for data management, facilitated by the psycopg2 library.

All the SQL queries defined as f-strings.

.. code-block:: python

    # SQL Query to insert donation_details into the database
    INSERT_DATABASE = f"""
    INSERT INTO {PREFIX}.information VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """

This function gets the last donation time for PayPal and Stripe seperately. If there is no prior donation, returns 1600000000 (Sun Sep 13 2020 12:26:40).

.. code-block:: python

    def get_last_donation_time() -> list[Donation]:
    """Get last donation for both Stripe and Paypal from the database."""
    conn = get_db_connection()
    ...

This function inserts the donation objects into database.

.. code-block:: python

    def insert_donation(donations: list[Donation]) -> None:
    ...
            for donation in donations:
                    cur.execute(
                        INSERT_DATABASE,
                        (
                            donation.confirmation_number,
                            donation.donor_name,
                            donation.currency,
                            donation.quantity,
                            donation.email,
                            donation.vendor,
                            donation.date_time,
                            donation.amount,
                            donation.access_token,
                        ),
                    )

This function gets the donations between specific dates in unix date-time format.

.. code-block:: python

    def get_donations_in_range(begin_date: int, end_date: int, vendor: str) -> list[Donation]:
    ...
            for row in rows:
                    donation = Donation(
                        confirmation_number=row[0],
                        donor_name=row[1],
                        currency=row[2],
                        quantity=row[3],
                        email=row[4],
                        vendor=row[5],
                        date_time=row[6],
                        amount=row[7],
                        access_token=row[8],
                    )

This functions are responsible for inserting, getting and deleting the deferred mails.

.. code-block:: python

    def insert_deferred_email(donations: list[Donation]) -> None:
    ...
    def get_deferred_emails() -> list[Donation]:
    ...
    def delete_deferred_emails() -> None:
    ...


stripeapi.py
------------

This file encapsulates all interactions with the Stripe API. It fetches new donations since the last recorded transaction and converts them into internal `Donation` objects.

This module uses Stripe's official library.

.. code-block:: python

    """This module contains the Stripe API operations."""

    import stripe

Queries handled in Stripe api.

.. code-block:: python

    charges = stripe.Charge.search(
                    query=f"created>{self.latest_donation_time}"
                )

    ...

    customer = stripe.Customer.retrieve(cus_id)

While stripe library returns the donations as charge object, this method converts the objects into Donation object which is defined in the config/models.py

.. code-block:: python

     def _charge_to_donation(self, charge: stripe.Charge, customer: stripe.Customer) -> Donation:


paypalapi.py
------------

Similar to `stripeapi.py`, this script handles all PayPal interactions. While there is no official PayPal library, all the processes completed by http requests. It authenticates, retrieves new transaction data, and transforms it into `Donation` objects.

It is needed to authenticate by the secret and get token.

.. code-block:: python

   def _get_access_token(self, client_id: str, client_secret: str) -> str:

PayPal queries the donation data in maximum of 31 days interval.

.. code-block:: python

    def request_donations(
            self, start_date: int = 0, end_date: int = int(datetime.now().timestamp())
        ) -> list[Donation]:

The response from API is converted to Donation object.

.. code-block:: python

    def _transaction_to_donation(self, transaction: dict[str, str]) -> Donation:

utils.py
-------------------------

This file is in use by Donation Harvester and Feedback Site.

.. code-block:: python

    def generate_xml_file(feedbacks: list, filename: str) -> None:
    ...
    def json_output(donations: list, filename: str='donations.json') -> None:

