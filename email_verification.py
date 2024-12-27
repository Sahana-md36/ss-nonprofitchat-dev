from fastapi import APIRouter, Request, Response, HTTPException
from pydantic import BaseModel, EmailStr
from session_utils import encode_jwt, decode_jwt, send_email
from salesforce_utils import get_contact_by_email, create_contact
import random

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "This API is live"}

class EmailRequest(BaseModel):
    email: EmailStr

class OTPValidationRequest(BaseModel):
    otp: int

@router.post("/auth/generate-otp")
async def generate_otp(request: Request, response: Response, email_request: EmailRequest):
    email = email_request.email
    otp = random.randint(100000, 999999)

    # Store session ID and OTP in JWT
    session_data = {"email": email, "otp": otp}
    jwt_token = encode_jwt(session_data)

    send_email(email, otp)
    response.set_cookie(key="session_token", value=jwt_token, httponly=True, samesite="None", secure=False)

    return {"message": f"OTP sent to {email}. Please check your inbox."}

# @router.post("/auth/verify-otp")
# async def verify_otp(request: Request, otp_request: OTPValidationRequest):
#     session_token = request.cookies.get("session_token")
#     if not session_token:
#         raise HTTPException(status_code=400, detail="Session token not found in cookies.")

#     session_data = decode_jwt(session_token)
#     if not session_data:
#         raise HTTPException(status_code=400, detail="Invalid session token.")

#     if session_data["otp"] != otp_request.otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP.")

#     email = session_data["email"]
#     contact = get_contact_by_email(email)
#     if contact:
#         return {"message": f"Email verified. Contact found: {contact['Name']}"}
#     else:
#         create_contact(email)
#         return {"message": "Email verified. New Contact created."}


# @router.post("/auth/verify-otp")
# async def verify_otp(request: Request, otp_request: OTPValidationRequest):
#     session_token = request.cookies.get("session_token")
#     if not session_token:
#         raise HTTPException(status_code=400, detail="Session token not found in cookies.")

#     session_data = decode_jwt(session_token)
#     if not session_data:
#         raise HTTPException(status_code=400, detail="Invalid session token.")

#     if session_data["otp"] != otp_request.otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP.")

#     email = session_data["email"]
#     contact = get_contact_by_email(email)
#     if contact:
#         return {"message": f"Email verified. Contact found: {contact['Name']}"}
#     else:

#         return {
#             "message": "Email verified. Last name is required to create a new Contact.",
#             "next_step": "Please provide your last name.",
#             "email": email,
#         }

# class LastNameRequest(BaseModel):
#     email: EmailStr
#     last_name: str

# @router.post("/auth/add-lastname")
# async def add_lastname(request: Request, lastname_request: LastNameRequest):
#     email = lastname_request.email
#     last_name = lastname_request.last_name

#     contact = get_contact_by_email(email)
#     if contact:
#         return {"message": f"Contact already exists: {contact['Name']}"}

#     create_contact(email, last_name)
#     return {"message": f"New Contact created for email: {email} with last name: {last_name}"}


@router.post("/auth/verify-otp")
async def verify_otp(request: Request, otp_request: OTPValidationRequest):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=400, detail="Session token not found in cookies.")

    session_data = decode_jwt(session_token)
    if not session_data:
        raise HTTPException(status_code=400, detail="Invalid session token.")

    if session_data["otp"] != otp_request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")

    email = session_data["email"]
    contact = get_contact_by_email(email)
    if contact:
        return {"message": f"Email verified. Contact found: {contact['Name']}"}
    else:
        return {
            "message": "Email verified. First name and last name are required to create a new Contact.",
            "next_step": "Please provide your details.",
            "email": email,
        }

class UserDetailsRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

@router.post("/auth/add-details")
async def add_details(request: Request, user_details_request: UserDetailsRequest):
    email = user_details_request.email
    first_name = user_details_request.first_name
    last_name = user_details_request.last_name

    contact = get_contact_by_email(email)
    if contact:
        return {"message": f"Contact already exists: {contact['Name']}"}

    create_contact(email, first_name, last_name)
    return {"message": f"New Contact created for email: {email} with name: {first_name} {last_name}"}
