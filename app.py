from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from email_verification import router as email_verification_router
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://nonprofit-ui.azurewebsites.net"],  # List of allowed origins
    allow_credentials=True,  # Allow cookies or Authorization headers
    allow_methods=["*"],  # HTTP methods allowed (e.g., GET, POST, etc.)
    allow_headers=["*"],  # HTTP headers allowed
)


# Middleware for handling session cookies
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY"))

# Routers
app.include_router(email_verification_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
