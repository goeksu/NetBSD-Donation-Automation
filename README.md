
![NetBSD.](http://netbsd.org/images/NetBSD-smaller-tb.png)
**Welcome to NetBSD Donation Automation's documentation!**

# Overview

This documentation covers the NetBSD Donation Automation system, designed to streamline the process of receiving and managing donations via Stripe and PayPal, and engaging donors through a feedback mechanism.

The system consists of two main components:

**Donation Harvester CLI app:**

Fetches new donations from payment platforms, stores them in a PostgreSQL database, and notifies donors with an email containing a feedback link and login credentials.

**Feedback Site:**

Provides a web interface for donors to submit feedback about their donation experience and consent to being listed on a public contributors' page.

# Installation

This section guides you through the installation process for the NetBSD Donation Automation system, specifically focusing on setting up the Feedback Site, which is a Flask-based web application. Ensure you have administrative access and the necessary permissions to install the software components described below.

## Prerequisites

Before you begin, you will need:

- **Python 3.6 or higher**: The application is written in Python and requires Python 3.6 or newer.
- **pip**: The Python package installer.
- **PostgreSQL**: A relational database system which is used to store all the application data.
- **Git**: To clone the repository.
- **Virtual Environment (optional but recommended)**: For creating isolated Python environments.

Ensure that Python, pip, and PostgreSQL are installed and properly configured on your system.

## Cloning the Repository

Clone the repository to get the source code on your machine:
```bash
    git clone https://github.com/goeksu/NetBSD-Donation-Automation.git
```
Navigate to the project directory:
```bash
    cd NetBSD-Donation-Automation
```
## Setting Up the Database

Set up the PostgreSQL database using the provided script:
```bash
    cd config
    ./set_db.sh -c
```
This script initializes the database schema and sets the required permissions.

## Setting Up the Virtual Environment

It is recommended to use a virtual environment to isolate package dependencies. To set up and activate a virtual environment:
```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
## Installing Python Dependencies

Install the necessary Python packages using pip:
```bash
    pip3 install -r requirements.txt
```
## Setting the API keys and secrets

Change your API keys and secrets in the `config/config.py` file. You can find the keys and secrets in your PayPal and Stripe accounts.

```bash
secret_key = ANY_RANDOM_STRING

paypal_client_id = YOUR_PAYPAL_CLIENT_ID
paypal_client_secret = YOUR_PAYPAL_CLIENT_SECRET

stripe_api_key = YOUR_STRIPE_API_KEY
```

## Starting the Feedback Site

Ensure you are in the root directory of the `feedback_site` module, then run:
```python
    export FLASK_APP=feedback_site
    export FLASK_ENV=development  # Use 'production' as appropriate
    flask run
```
This command will start the Flask application on the default port (5000). Open a web browser and navigate to `http://127.0.0.1:5000/` to view the application.

## Next Steps

After installation, you may want to configure the system settings or customize the application to better fit your needs. Refer to the `config_module` and `feedback_site` documentation for detailed information on configurations and customizations.
