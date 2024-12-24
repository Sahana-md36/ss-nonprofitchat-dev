import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
import os


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
ALGORITHM = os.getenv("JWT_ALGORITHM") 
EXPIRE_DELTA = timedelta(hours=1)  # Token expiry time

def encode_jwt(session_data: dict) -> str:
    """Generate JWT token with session data."""
    expiration = datetime.utcnow() + EXPIRE_DELTA
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
