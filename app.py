from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from email_verification import router as email_verification_router
import os
import uvicorn

app = FastAPI()

# Middleware for handling session cookies
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY"))

# Routers
app.include_router(email_verification_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
