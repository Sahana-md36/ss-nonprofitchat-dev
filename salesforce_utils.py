from simple_salesforce import Salesforce
from dotenv import load_dotenv
from fastapi import HTTPException
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

def create_contact(email, first_name, last_name):

    sf = connect_to_salesforce()
    contact = {
        "Email": email,
        "FirstName": first_name,
        "LastName": last_name,
    }
    result = sf.Contact.create(contact)
    return result

def query_database(email, route_name):
    sf = connect_to_salesforce() 
    try: 
        if route_name == "APPLICATION_ROUTE":
            results = sf.query_all("SELECT Summary FROM Knowledge__kav WHERE Title ='Application Process'")
            if results["totalSize"] == 0:
                return {"message": "No data found for Application Process", "route": route_name}
            data = [record["Summary"] for record in results["records"]]  
        
        elif route_name == "DOCUMENTS_ROUTE":
            results = sf.query_all("SELECT Summary FROM Knowledge__kav WHERE Title ='Documentation Requirement'")
            if results["totalSize"] == 0:
                return {"message": "No data found for Documentation Requirement", "route": route_name}
            data = [record["Summary"] for record in results["records"]]        
        
        elif route_name == "STATUS_ROUTE":
            results = sf.query_all(f"SELECT Application_Status__c FROM Contact WHERE Email ='{email}'")
            if results["totalSize"] == 0 or not results['records']:
                return {"message": "No data found for the provided email or application status.", "route": route_name}
            data = results['records'][0].get('Application_Status__c')
        
        else:
            return {"message": "Sorry, I am unable to answer that question. Please ask about Application Process, Documents required, or the status of your application."}

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Salesforce query failed: {str(e)}")
