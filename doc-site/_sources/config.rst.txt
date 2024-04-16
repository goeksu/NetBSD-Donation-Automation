.. _config:

config
====================

This module is responsible for managing all configurations related to databases and email services, and includes utilities for handling various tasks across the project. Below are detailed descriptions of each file and its functionalities.

__init__.py
-----------

.. code-block:: python

    """Database and email configuration."""

    import logging
    import smtplib
    import ssl
    from configparser import ConfigParser
    import os
    import psycopg2
    from .models import Donation
    from validate_email import validate_email

    # Initialization and configuration setup...

This file handles the initialization of email and database configurations. It reads from the configuration files to set up SMTP for sending emails and establishes database connections.

Key Functions:\n
- `get_db_connection`: Establishes ¬ database connection using psycopg2.\n
- `get_server`: Configures and returns an SMTP server instance for sending emails.\n
- `send_url_mail`: Prepares and sends an email containing the URL to the donation page.\n
- `send_thank_mail`: Sends a thank you email to a recipient.

models.py
---------

.. code-block:: python

    """This file contains the Donation class and Feedback class."""

    from datetime import datetime
    from config import utils

    class Donation:
        """Represents a donation."""
        # Constructor and methods...

    class Feedback:
        """Represents a feedback received from donors."""
        # Constructor and methods...

This file defines the data models for donations and feedbacks. The `Donation` class encapsulates all attributes related to a donation, and the `Feedback` class deals with responses received from donors.

utils.py
--------

.. code-block:: python

    """This module provides utility functions for the application."""

    import uuid
    import logging
    import json
    import xml.etree.ElementTree as ET

    # Utility functions...

This file contains utility functions that are used across various modules. Functions include generating XML files, confirming numbers, access tokens, and handling JSON outputs that used by both *donation_harvester* and *feedback_site*.

set_db.sh
---------

This script automates the database setup process including user creation, database creation, and setting permissions. It provides options to create or drop the database.

Configuration Files
-------------------

- **config.ini**: Contains the main settings for the application, such as database credentials.
- **mail_config.ini**: Specifies the configurations for the email server, including SMTP settings and credentials.



