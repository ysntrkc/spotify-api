from fastapi import APIRouter, Request
from utils.responses import (
    StandardResponse,
    create_success_response,
    handle_spotify_error,
)
from utils.auth import validate_auth_header, create_spotify_headers
from utils.validators import validate_time_range, validate_limit
from utils.data_filters import filter_track_data, filter_singer_data
import requests

router = APIRouter()


@router.get("/top-tracks", response_model=StandardResponse)
async def get_top_tracks(request: Request, time_range: str, limit: int = 10):
    try:
        validate_time_range(time_range)
        validate_limit(limit)

        access_token = validate_auth_header(request.headers.get("Authorization"))
        headers = create_spotify_headers(access_token)

        response = requests.get(
            f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}",
            headers=headers,
        )
        handle_spotify_error(response)

        filtered_tracks = [
            filter_track_data(track) for track in response.json()["items"]
        ]
        return create_success_response(
            "Top tracks fetched successfully", {"items": filtered_tracks}
        )

    except Exception as e:
        raise e


@router.get("/top-singers", response_model=StandardResponse)
async def get_top_singers(request: Request, time_range: str, limit: int = 10):
    try:
        validate_time_range(time_range)
        validate_limit(limit)

        access_token = validate_auth_header(request.headers.get("Authorization"))
        headers = create_spotify_headers(access_token)

        response = requests.get(
            f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}",
            headers=headers,
        )
        handle_spotify_error(response)

        filtered_singers = [
            filter_singer_data(artist) for artist in response.json()["items"]
        ]
        return create_success_response(
            "Top singers fetched successfully", {"items": filtered_singers}
        )

    except Exception as e:
        raise e
