feedback_site
==============

The Feedback Site module handles the collection and processing of feedback from donors. It provides interfaces for entering feedback, validating donation information, and submitting responses to the system.
Site is running by Flask.

app.py
------

This file sets up the Flask application and defines routes for handling user interactions. Key functions include:

- **index:** Renders the main page of the feedback site.
- **validate:** Validates donation details submitted by the user.
- **feedback_by_mail:** Handles feedback provided via links in emails.
- **store:** Stores the feedback into the database and handles file uploads if necessary.

.. code-block:: python

    csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\'',
    'style-src': '\'self\''
    }

    app = Flask(__name__)
    Talisman(app,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
        force_https=False) # TODO for development only

Security settings such as Content Security Policy (CSP) are applied using Flask-Talisman.



database.py
-----------

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

.. code-block:: python

     SQL_CHECK_EXISTS_BY_EMAIL_AND_CONFIRMATION = f"""
    PREPARE get_donations (text, int) AS
    SELECT *
    FROM {PREFIX}.information d
    WHERE d.email = $1 AND d.confirmation_no = $2;
    EXECUTE get_donations(%s, %s);
    """

    SQL_EXISTS_BY_TOKEN = f"""
    PREPARE get_donations_by_token (text) AS
    SELECT *
    FROM {PREFIX}.information
    WHERE uuid = $1;
    EXECUTE get_donations_by_token(%s);
    """

- **FeedbackSQL:** Handles SQL queries for feedback interactions.

.. code-block:: python

     SQL_CHECK_EXISTS_BY_CONFIRMATION = f"""
    PREPARE check_feedback (int) AS
    SELECT EXISTS(SELECT 1 FROM {PREFIX}.interaction WHERE confirmation_no = $1);
    EXECUTE check_feedback(%s);
    """

    SQL_INSERT_FEEDBACK = f"""
    PREPARE insert_feedback (int, bool, text, bool, text, bool, text, text) AS
    INSERT INTO {PREFIX}.interaction VALUES($1, $2, $3, $4, $5, $6, $7, $8);
    EXECUTE insert_feedback(%s, %s, %s, %s, %s, %s, %s, %s);
    """

    SQL_GET_DONORS_THIS_YEAR = f"""
    SELECT i.name,i.logo_filepath,
        CASE WHEN i.answer2 THEN i.email ELSE NULL END
    FROM {PREFIX}.interaction AS i
    INNER JOIN {PREFIX}.information AS inf
    ON i.confirmation_no = inf.confirmation_no
    WHERE i.answer1 = TRUE
        AND EXTRACT(YEAR FROM TO_TIMESTAMP(inf.datetime)) = %s;
    """


Each script is crucial for the operations of the feedback site, ensuring that donor feedback is collected securely and efficiently, maintaining privacy and data integrity.

Files
------
- **Templates:** Contains HTML templates for the feedback site. Uses Bootstrap 5.2.3.
- **Static:** Includes CSS and JavaScript files for styling and interactivity.