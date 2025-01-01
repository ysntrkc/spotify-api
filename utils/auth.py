from fastapi import HTTPException
from typing import Optional


def validate_auth_header(auth_header: Optional[str]) -> str:
    if not auth_header:
        raise HTTPException(status_code=401, detail="No authorization header")
    try:
        return auth_header.split("Bearer ")[1]
    except:
        raise HTTPException(
            status_code=401, detail="Invalid authorization header format"
        )


def create_spotify_headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}
