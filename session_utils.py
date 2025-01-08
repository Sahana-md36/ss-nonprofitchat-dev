import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
import os
import re
from fastapi import Request
from typing import Union

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
ALGORITHM = os.getenv("JWT_ALGORITHM") 
EXPIRE_DELTA = timedelta(minutes=30)  # Token expiry time

def encode_jwt(session_data: dict) -> str:
    """Generate JWT token with session data."""
    expiration = datetime.now(timezone.utc) + EXPIRE_DELTA
    payload = {
        "data": session_data,
        "exp": expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict:
    """Decode JWT token and retrieve session data."""
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["data"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def validate_session_token(request: Request) -> Union[dict, str]:
    """
    Validates the session token from cookies and decodes the session data.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        Union[dict, str]: Decoded session data if valid, or an error message if invalid.
    """
    try:
        session_token = request.cookies.get("session_token")
        if not session_token:
            raise ValueError("Session expired")

        session_data = decode_jwt(session_token)
        if not session_data:
            raise ValueError("Session invalid")

        return session_data
    except ValueError:
        return "Session expired or invalid, please log in again."


GMAIL_USER = os.getenv("GMAIL_USER")  
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")  

def send_email(email, otp):
    """Send OTP email using Gmail's SMTP server."""
    subject = "Your Verification Code"
    body = f"Hello,\n\nYour OTP code is {otp}. Please use this to verify your email.\n\nBest regards,\nMagicBot"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establish a connection to the Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)  # Login with Gmail credentials
            server.sendmail(GMAIL_USER, email, msg.as_string())  # Send the email
            print(f"OTP {otp} sent successfully to {email}")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")


# Regex for email validation
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def is_valid_email(email: str) -> bool:
    """
    Validates the email using a regular expression.
    """
    return re.match(EMAIL_REGEX, email) is not None