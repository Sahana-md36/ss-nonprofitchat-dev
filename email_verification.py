from fastapi import APIRouter, Request, Response, HTTPException, status
from pydantic import BaseModel, EmailStr
from session_utils import encode_jwt, decode_jwt, send_email
from salesforce_utils import get_contact_by_email, create_contact, query_database
import random
from semantic_router_utils import setup_routes, handle_user_query

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
    response.set_cookie(key="session_token", value=jwt_token, httponly=True, samesite="None", secure=True)

    return {"message": f"OTP sent to {email}. Please check your inbox."}


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
            "message": "Email verified. To proceed further, please provide your first and last name",
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

# Semantic routing
rl = setup_routes()

class QueryRequest(BaseModel):
    query: str

@router.post("/process-query")
async def process_query(request: Request, query_request: QueryRequest):
    session_token = request.cookies.get("session_token")  # Extract the session token from cookies
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid. Please log in and verify your email to proceed further.")
 
    session_data = decode_jwt(session_token)  # Decode the JWT for session data
    if not session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid. Please log in and verify your email to proceed further.")
    
    query = query_request.query

    # Classify the query using semantic routing
    classification = handle_user_query(query)
    route_name = classification.get("route_name", "OTHER")

    route_info = query_database(session_data["email"], route_name)
    # Handle the case where we get a message instead of data
    if isinstance(route_info, dict) and "message" in route_info:
        return route_info  # Return the message if no data found
    
    # Extract summaries for the records
    if isinstance(route_info, list):
        return route_info  # Return summaries directly if it's a list
    
    # Return the application status or other singular info
    if route_name=="STATUS_ROUTE" and route_info is None:
        route_info = "Status Unavailable"
    return {"message": route_info}  # Handling non-list return values


