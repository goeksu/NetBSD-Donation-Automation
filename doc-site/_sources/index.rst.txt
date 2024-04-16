
Welcome to NetBSD Donation Automation's documentation!
======================================================

This documentation covers the NetBSD Donation Automation system, designed to streamline the process of receiving and managing donations via Stripe and PayPal, and engaging donors through a feedback mechanism.

Overview
--------

The system consists of two main components:

**Donation Harvester CLI app:**
    Fetches new donations from payment platforms, stores them in a PostgreSQL database, and notifies donors with an email containing a feedback link and login credentials.

**Feedback Site:**
    Provides a web interface for donors to submit feedback about their donation experience and consent to being listed on a public contributors' page.

This documentation aims to guide you through the installation and configuration of both components, ensuring smooth operation and maintenance.

Getting Started
---------------

Before diving into the specific modules, ensure you review the installation instructions to set up your environment correctly.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   donation_harvester
   feedback_site
   config

Feel free to explore each section to understand better how each part of the system operates and how to effectively manage and utilize it.