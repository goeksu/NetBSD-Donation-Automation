feedback_site
==============

The Feedback Site module handles the collection and processing of feedback from donors. It provides interfaces for entering feedback, validating donation information, and submitting responses to the system.

app.py
------

.. code-block:: python

    """app.py is the main entry point for the feedback site."""

    from flask import Flask, render_template, request, session
    from flask_talisman import Talisman

    # Flask application setup and routes...

This file sets up the Flask application and defines routes for handling user interactions. Key functions include:

- **index:** Renders the main page of the feedback site.
- **validate:** Validates donation details submitted by the user.
- **feedback_by_mail:** Handles feedback provided via links in emails.
- **store:** Stores the feedback into the database and handles file uploads if necessary.

Security settings such as Content Security Policy (CSP) are applied using Flask-Talisman.

database.py
-----------

.. code-block:: python

    """database.py is the database layer for the feedback site."""

    import psycopg2
    from config import get_db_connection

    # Database query execution...

This script contains functions for interacting with the database. It utilizes a central function `execute_query` to perform SQL operations, ensuring that database interactions are handled efficiently and securely.

files.py
--------

.. code-block:: python

    """This module handles the file upload and processing."""

    import os
    from PIL import Image
    from werkzeug.utils import secure_filename

    # File validation and processing...

Responsible for processing uploaded files, this file includes functions to validate file extensions and sizes, handle image resizing based on donation amounts, and save files to the server.

queries.py
----------

This file defines classes for structuring SQL queries related to donations and feedback. It includes methods for checking the existence of donations and feedback and for inserting new feedback records into the database.

Key Classes:

- **DonationSQL:** Manages SQL queries related to donation records.
- **FeedbackSQL:** Handles SQL queries for feedback interactions.

Each script is crucial for the operations of the feedback site, ensuring that donor feedback is collected securely and efficiently, maintaining privacy and data integrity.

Files
------
- **Templates:** Contains HTML templates for the feedback site.
- **Static:** Includes CSS and JavaScript files for styling and interactivity.