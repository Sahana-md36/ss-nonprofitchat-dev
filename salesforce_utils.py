from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Salesforce credentials
SF_USERNAME = os.getenv("SF_USERNAME")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")

def connect_to_salesforce():
    """Connect to Salesforce using credentials from .env"""
    try:
        sf = Salesforce(
            username=SF_USERNAME,
            password=SF_PASSWORD,
            security_token=SF_SECURITY_TOKEN
        )
        return sf
    except Exception as e:
        raise Exception(f"Failed to connect to Salesforce: {e}")

def get_contact_by_email(email):
    """Check the Contact with the email id."""
    sf = connect_to_salesforce()
    query = f"SELECT Id, Name FROM Contact WHERE Email = '{email}'"
    result = sf.query(query)
    if result['records']:
        return result['records'][0]  # Return the first matching contact
    return None

# def create_contact(email):
#     """Insert a new Contact record"""
#     sf = connect_to_salesforce()
#     contact = {"Email": email}
#     result = sf.Contact.create(contact)
#     return result

# def create_contact(email, last_name):
#     """Insert a new Contact record."""
#     sf = connect_to_salesforce()
#     contact = {"Email": email, "LastName": last_name}
#     result = sf.Contact.create(contact)
#     return result
def create_contact(email, first_name, last_name):

    sf = connect_to_salesforce()
    contact = {
        "Email": email,
        "FirstName": first_name,
        "LastName": last_name,
    }
    result = sf.Contact.create(contact)
    return result
