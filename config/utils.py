"""This module is for random stuff."""
import uuid
import logging
import json
from datetime import datetime
import xml.etree.ElementTree as ET

# Set up allowed file extensions for logo
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def generate_xml_file(feedbacks: list, filename: str) -> None:
    """Generate an XML file with the provided feedbacks"""
    root = ET.Element("donations")
    i = 0
    for feedback in feedbacks:
        if feedback.answer1:
            i += 1
            feedback_element = ET.SubElement(root, "donor")
            feedback_element.set("name", str(feedback.name))
            if feedback.answer2:
                feedback_element.set("email", str(feedback.email))
            if str(feedback.logo_filepath) != "None":
                feedback_element.set("logo_filepath", str(feedback.logo_filepath))
    logging.info(f"Exported {i} feedbacks to {filename} aligning to response")    
    tree = ET.ElementTree(root)
    tree.write(filename)

def generate_confirmation_number() -> str:
    """Generate a random six-digit number"""
    return str(uuid.uuid4().int)[0:10]

def generate_access_token() -> str:
    """Generate a random UUID"""
    return str(uuid.uuid4())

def json_output(donations: list, filename: str='donations.json') -> None:
    """Output results as a JSON file"""
    with open(filename, 'w') as f:
        json.dump(
            [donation.__dict__ for donation in donations],f
            )
    logging.info(f"Successfully outputted results as {filename}")

def check_length(string:str) -> bool:
    """Check if the length of the string is less than 50"""
    return len(string) < 50

def valid_uuid(uuid_string: str) -> bool:
    """Check if the provided string is a valid UUID."""
    try:
        uuid.UUID(uuid_string)
        logging.info(f"Valid Token: {uuid_string}")
        return True
    except ValueError:
        logging.info(f"Invalid Token: {uuid_string}")
        return False
