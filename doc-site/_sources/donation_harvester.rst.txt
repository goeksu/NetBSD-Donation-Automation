.. _donation_harvester:

donation_harvester
==================

The Donation Harvester module is responsible for interacting with payment platforms like PayPal and Stripe to fetch new donations, manage these donations in a database, and optionally send notifications to donors. It provides a command-line interface for different operations like updating, listing, and exporting donations.

app.py
------

.. code-block:: python

    """This is the entry point of the application."""
    import argparse
    from datetime import datetime

    # Application setup and command-line argument parsing...

This script is the main driver of the module, handling command-line inputs to trigger specific functionalities like fetching new donations, sending deferred emails, and exporting data. It leverages external APIs through `stripeapi.py` and `paypalapi.py`.

database.py
-----------

.. code-block:: python

    """This module contains functions to establish connection with the database
    and insert donation details into the database."""

    # Database connection and query execution functions...

This script contains all database interactions, including fetching the latest donations, inserting new donation records, and managing deferred emails. It uses PostgreSQL for data management, facilitated by the psycopg2 library.

stripeapi.py
------------

.. code-block:: python

    """This module contains the Stripe API operations."""

    import stripe
    from config.models import Donation

    # Stripe API interaction...

This file encapsulates all interactions with the Stripe API. It fetches new donations since the last recorded transaction and converts them into internal `Donation` objects.

paypalapi.py
------------

.. code-block:: python

    """This module contains the Paypal API operations."""

    import requests
    from config.models import Donation

    # PayPal API interaction...

Similar to `stripeapi.py`, this script handles all PayPal interactions. It authenticates with the PayPal API, retrieves new transaction data, and transforms it into `Donation` objects.

Key Functions and Methods
-------------------------

- **main**: Orchestrates the module's operations based on command-line arguments.
- **insert_donation**: Inserts new donation data into the database.
- **get_new_donations**: Fetches new donations from PayPal and Stripe.
- **sendmail**: Sends emails to donors based on newly fetched donations.
- **get_last_donation_time**, **insert_deferred_email**, **delete_deferred_emails**: Manage timing and email notifications for asynchronous communication with donors.
- **generate_xml_file**, **json_output**: Output donation data in XML or JSON format for reporting or integration with other systems.

The module is designed to be run periodically, either manually or via a scheduler, to keep donation records up to date and maintain engagement with donors through timely communications.
