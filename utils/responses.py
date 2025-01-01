from pydantic import BaseModel
from typing import Optional, Dict, Any
from fastapi import HTTPException


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


def create_success_response(
    message: str, data: Optional[Dict[str, Any]] = None
) -> StandardResponse:
    return StandardResponse(status="success", message=message, data=data)


def create_error_response(
    message: str, detail: Optional[str] = None
) -> StandardResponse:
    return StandardResponse(
        status="error", message=message, data={"detail": detail} if detail else None
    )


def validate_auth_header(auth_header: Optional[str]) -> str:
    if not auth_header:
        raise HTTPException(status_code=401, detail="No authorization header")
    return auth_header.split("Bearer ")[1]


def handle_spotify_error(response, error_prefix: str = "Spotify API error"):
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=f"{error_prefix}: {response.text}"
        )
