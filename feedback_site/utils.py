"""This module is for small function stuff."""
import logging
from uuid import UUID
from typing import Dict
from models import Donation
from config import send_thank_mail


def send_async_email(app, receiver_email):
    """This function prevents waiting for mails sent before rendering thank_you page."""
    with app.app_context():
        send_thank_mail(receiver_email)


def valid_uuid(uuid_string):
    """Check if the provided string is a valid UUID."""
    try:
        UUID(uuid_string)
        logging.info(f"Valid Token: {uuid_string}")
        return True
    except ValueError:
        logging.info(f"Invalid Token: {uuid_string}")
        return False


def arr_to_donation(donation_arr) -> Donation:
    """Array to Donation object"""
    return Donation(
        confirmation_number=donation_arr[0],
        donor_name=donation_arr[1],
        currency=donation_arr[2],
        quantity=donation_arr[3],
        email=donation_arr[4],
        vendor=donation_arr[5],
        date_time=donation_arr[6],
        amount=donation_arr[7],
        access_token=donation_arr[8],
    )


def dict_to_donation(data: Dict) -> Donation:
    """Dictionary to Donation object"""
    return Donation(
        donor_name=data.get("donor_name"),
        amount=data.get("amount"),
        currency=data.get("currency"),
        email=data.get("email"),
        date_time=data.get("date_time"),
        vendor=data.get("vendor"),
        confirmation_number=data.get("confirmation_number"),
        access_token=data.get("access_token"),
        quantity=data.get("quantity", 1),
    )