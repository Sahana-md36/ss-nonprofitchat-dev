from fastapi import APIRouter, Request, Response, HTTPException, status
from pydantic import BaseModel, EmailStr
from session_utils import encode_jwt, decode_jwt, send_email, is_valid_email, validate_session_token
from salesforce_utils import get_contact_by_email, create_contact, query_database
import random
from semantic_router_utils import setup_routes, handle_user_query

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "This API is live"}

class EmailRequest(BaseModel):
    email: str

class OTPValidationRequest(BaseModel):
    otp: int

@router.post("/auth/generate-otp")
async def generate_otp(request: Request, response: Response, email_request: EmailRequest):
    email = email_request.email

    if not is_valid_email(email):
        return {"message": "Please enter a valid email address."}

    otp = random.randint(100000, 999999)

    # Store session ID and OTP in JWT
    session_data = {"email": email, "otp": otp}
    jwt_token = encode_jwt(session_data)

    send_email(email, otp)
    response.set_cookie(key="session_token", value=jwt_token, httponly=True, samesite="None", secure=True)

    return {"message": f"An OTP has been sent to {email}. Please check your inbox and enter the OTP below."}


@router.post("/auth/verify-otp")
async def verify_otp(request: Request, otp_request: OTPValidationRequest):
    session_result = validate_session_token(request)

    if isinstance(session_result, str):
        # If the result is an error message, return it as a response
        return {"message": session_result}
    
    # Proceed with session data
    session_data = session_result

    if session_data["otp"] != otp_request.otp:
        return {"message": "You've entered an invalid OTP. Please try again."}

    email = session_data["email"]
    contact = get_contact_by_email(email)
    if contact:
        return {"message": f"Email verified.\nWelcome {contact['Name']}. You can now ask questions about the Scholarship Application Process, the Documents Required and the Status of your application if you have already applied for scholarship."}
    else:
        return {
            "message": "Email verified.\nSince this is the first time you are using the chat, we will need your first and last name to create a new user.  Please start with providing your first name.",
            "next_step": "Please provide your details.",
            "email": email,
        }

class UserDetailsRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

@router.post("/auth/add-details")
async def add_details(request: Request, user_details_request: UserDetailsRequest):
    session_result = validate_session_token(request)

    if isinstance(session_result, str):
        # If the result is an error message, return it as a response
        return {"message": session_result}

    email = user_details_request.email
    first_name = user_details_request.first_name
    last_name = user_details_request.last_name

    contact = get_contact_by_email(email)
    if contact:
        return {"message": f"User already exists for {contact['Name']}."}

    create_contact(email, first_name, last_name)
    return {"message": f"Created new user for email {email} with name {first_name} {last_name}. You can now ask questions about the Scholarship Application Process and the Documents Required."}

# Semantic routing
rl = setup_routes()

class QueryRequest(BaseModel):
    query: str

@router.post("/process-query")
async def process_query(request: Request, query_request: QueryRequest):
    session_result = validate_session_token(request)

    if isinstance(session_result, str):
        # If the result is an error message, return it as a response
        return {"message": session_result}
    
    session_data = session_result
    
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
    # if route_name=="STATUS_ROUTE" and route_info is None:
    #     route_info = "There is no Application found to report status"
    return {"message": route_info}  # Handling non-list return values


