"""This module contains the Paypal API operations."""
import logging
from datetime import datetime, timedelta, timezone
import requests
from requests.auth import HTTPBasicAuth
from models import Donation


class PaypalAPI:
    """This is a class for Paypal API."""

    def __init__(
        self, client_id: str, client_secret: str, last_donation_time: datetime
    ) -> None:
        # Get access token
        self.access_token = self._get_access_token(client_id, client_secret)
        last_donation_time = (
            last_donation_time[:-2] + "00" + last_donation_time[-2:]
        )
        self.latest_donation_time = int(
            datetime.timestamp(
                datetime.strptime(last_donation_time, "%Y-%m-%d %H:%M:%S%z")
            )
        )

    def _get_access_token(self, client_id: str, client_secret: str) -> str:
        """Gets access token from Paypal API."""
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        payload = "grant_type=client_credentials"
        r = requests.post(
            url,
            auth=HTTPBasicAuth(client_id, client_secret),
            data=payload,
            timeout=10,
        )
        return r.json()["access_token"]

    def _update_latest_donation_time(self, timestamp: int):
        """
        This function compares the timestamp of the latest donation with
        the timestamp of the current donation and updates
        the latest_donation_time if the current donation is newer.
        """
        self.latest_donation_time = max(
            int(self.latest_donation_time), int(timestamp)
        )

    def get_new_donations(self) -> list[Donation]:
        """
        Gets donation later than the latest_donation_time.
        """
        return self.request_donations(
            datetime.fromtimestamp(self.latest_donation_time)
        )

    def get_all_charges(self) -> list[Donation]:
        """
        Gets all charges in 1 month
        """
        return self.request_donations()

    def request_donations(
        self, start_date: datetime = None, end_date: datetime = datetime.now()
    ) -> list[Donation]:
        """
        This function requests donations from Paypal API for the time between
        given args. If args are not given, it requests donations for the last
        30 days.
        """
        if start_date is None:
            start_date = end_date - timedelta(days=29)

        headers = {"Authorization": f"Bearer {self.access_token}"}

        # if difference is more than a month adjust start_date to be exactly
        # a month before end_date
        if (end_date - start_date).days >= 30:
            start_date = end_date - timedelta(days=29)

        # convert datetime object to required format
        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.999Z")
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.999Z")

        params = (
            ("fields", "payer_info"),
            ("start_date", start_date),
            ("end_date", end_date),
        )

        response = requests.get(
            "https://api-m.sandbox.paypal.com/v1/reporting/transactions",
            headers=headers,
            params=params,
            timeout=10,
        )

        response_json = response.json()

        # Check if the request was successful
        if (
            "name" in response_json
            and response_json["name"] == "INVALID_REQUEST"
        ):
            logging.error(f"Invalid request: {response_json['message']}")
            return []

        # Check if the response contains the transaction_details key
        if "transaction_details" not in response_json:
            logging.error("KeyError: 'transaction_details'")
            return []

        # Get the transactions from the response
        transactions = response_json["transaction_details"]

        # Convert the transactions to Donation objects. Store them in a list.
        donations = []
        for transaction in transactions:
            donation = self._transaction_to_donation(transaction)
            donations.append(donation)
        logging.info(f"PayPal - fetched {len(donations)} donations between {start_date} and {end_date}")
        return donations

    def _transaction_to_donation(self, transaction: dict[str, str]) -> Donation:
        """
        Converts a PayPal transaction into a Donation object.
        Also updates the latest_donation_time based on the transaction's
        timestamp.
        Uses UTC.
        """

        # Get the transaction_info and payer_info from the transaction
        transaction_info = transaction["transaction_info"]
        payer_info = transaction["payer_info"]

        # Prepare the variables to return Donation object
        donor_name = payer_info["payer_name"].get(
            "alternate_full_name", "Unknown"
        )
        email = payer_info.get("email_address", "Unknown")
        amount = float(
            transaction_info["transaction_amount"].get("value", 0.0)
        )
        currency = transaction_info["transaction_amount"].get(
            "currency_code", "Unknown"
        )
        date_time = datetime.strptime(
            transaction_info["transaction_initiation_date"],
            "%Y-%m-%dT%H:%M:%S%z",
        )
        date_time = date_time.astimezone(timezone.utc)  # convert to UTC
        vendor = "PayPal"

        # Update the latest_donation_time if this transaction is newer
        self._update_latest_donation_time(int(date_time.timestamp()))
        int(date_time.timestamp())
        return Donation(
            donor_name, amount, currency, email, date_time, vendor
        )
