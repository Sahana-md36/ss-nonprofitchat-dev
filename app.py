from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from email_verification import router as email_verification_router
import os

app = FastAPI()

# Middleware for handling session cookies
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY"))

# Routers
app.include_router(email_verification_router)
