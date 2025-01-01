from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from routers import auth, top, profile
import os
from dotenv import load_dotenv

load_dotenv()


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


app = FastAPI()


# Add error handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=StandardResponse(
            status="error", message="Internal server error", data={"detail": str(exc)}
        ).dict(),
    )


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(top.router)
app.include_router(profile.router)
