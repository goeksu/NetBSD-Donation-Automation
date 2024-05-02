.. _config:

config
====================

This module is responsible for managing all configurations related to databases and email services, and includes utilities for handling various tasks across the project. Below are detailed descriptions of each file and its functionalities.

__init__.py
-----------

This file handles the initialization of email and database configurations. It reads from the configuration files to set up SMTP for sending emails and establishes database connections.

Key Functions:

- `get_db_connection`: Establishes database connection using psycopg2.

- `get_server`: Configures and returns an SMTP server instance for sending emails.

- `send_url_mail`: Prepares and sends an email containing the URL to the donation page.

- `send_thank_mail`: Sends a thank you email to a recipient.

models.py
---------

.. code-block:: python

    class Donation:
        """Represents a donation."""
        def __init__(
        self,
        donor_name: str,
        amount: float,
        currency: str,
        email: str,
        date_time: int,
        vendor: str,
        confirmation_number=None,
        access_token=None,
        quantity: int = 1,
    ) -> None:
        # Constructor and methods...
        def print_donation(self) -> None:
        def list_to_donation(donation_arr: list[str]) -> Donation:
        def dict_to_donation(data: dict[str, str]) -> Donation:



    class Feedback:
        """Represents a feedback received from donors."""
        def __init__(
        self,
        confirmation_number: int,
        answer1: bool,
        name: str,
        answer2: bool,
        email: str,
        answer3: bool,
        notification_email=str,
        logo_filepath=str,
    ) -> None:
        # Constructor and methods...
        def print_feedback(self) -> None:

This file defines the data models for donations and feedbacks. The `Donation` class encapsulates all attributes related to a donation, and the `Feedback` class deals with responses received from donors.

utils.py
--------

.. code-block:: python

    def generate_xml_file(feedbacks: list, filename: str) -> None:
    def generate_confirmation_number() -> str:
    def generate_access_token() -> str:
    def json_output(donations: list, filename: str='donations.json') -> None:
    def check_length(string:str) -> bool:
    def valid_uuid(uuid_string: str) -> bool:

This file contains utility functions that are used across various modules. Functions include generating XML files, confirming numbers, access tokens, and handling JSON outputs that used by both *donation_harvester* and *feedback_site*.

set_db.sh
---------

This script automates the database setup process including user creation, database creation, and setting permissions. It provides options to create or drop the database.

Configuration Files
-------------------

- **config.ini**: Contains the main settings for the application, such as database credentials.
- **mail_config.ini**: Specifies the configurations for the email server, including SMTP settings and credentials.



