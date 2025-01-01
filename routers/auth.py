from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import Optional, Dict, Any

router = APIRouter()


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


@router.get("/auth/spotify", response_model=StandardResponse)
async def spotify_auth():
    try:
        auth_url = (
            "https://accounts.spotify.com/authorize"
            "?response_type=code"
            f"&client_id={os.getenv('SPOTIFY_CLIENT_ID')}"
            f"&redirect_uri={os.getenv('SPOTIFY_REDIRECT_URI')}"
            "&scope=user-read-private user-read-email user-top-read"
        )
        return StandardResponse(
            status="success",
            message="Auth URL generated successfully",
            data={"auth_url": auth_url},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/auth/spotify/callback", response_model=StandardResponse)
async def spotify_callback(request: Request):
    try:
        code = request.query_params.get("code")
        if not code:
            raise HTTPException(
                status_code=400, detail="Authorization code is required"
            )

        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
            "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
            "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        }
        token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = requests.post(
            token_url, data=token_data, headers=token_headers
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=token_response.status_code, detail=token_response.text
            )

        token_json = token_response.json()
        return StandardResponse(
            status="success",
            message="Token obtained successfully",
            data={"access_token": token_json.get("access_token")},
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth/logout", response_model=StandardResponse)
async def logout():
    return StandardResponse(
        status="success", message="Logged out successfully", data=None
    )
