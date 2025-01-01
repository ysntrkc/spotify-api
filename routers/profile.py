from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import requests
from typing import Optional, Dict, Any

router = APIRouter()


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


@router.get("/me", response_model=StandardResponse)
async def get_current_user_profile(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="No authorization header")

        access_token = auth_header.split("Bearer ")[1]
        profile_url = "https://api.spotify.com/v1/me"
        profile_headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = requests.get(profile_url, headers=profile_headers)

        if profile_response.status_code != 200:
            raise HTTPException(
                status_code=profile_response.status_code, detail=profile_response.text
            )

        profile_data = profile_response.json()
        filtered_data = {
            "display_name": profile_data.get("display_name"),
            "email": profile_data.get("email"),
            "id": profile_data.get("id"),
            "images": [img.get("url") for img in profile_data.get("images", [])],
        }

        return StandardResponse(
            status="success", message="Profile fetched successfully", data=filtered_data
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
