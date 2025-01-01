from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


class TimeRange(str, Enum):
    one_week = "short_term"
    one_month = "medium_term"
    one_year = "long_term"


@app.get("/auth/spotify")
async def spotify_auth():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        "?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        "&scope=user-read-private user-read-email user-top-read"
    )
    return {"auth_url": auth_url}


@app.get("/auth/spotify/callback")
async def spotify_callback(request: Request):
    code = request.query_params.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_response.json()
    access_token = token_json.get("access_token")
    return {"access_token": access_token}


@app.get("/me")
async def get_current_user_profile(request: Request):
    access_token = request.headers.get("Authorization").split("Bearer ")[1]
    profile_url = "https://api.spotify.com/v1/me"
    profile_headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = requests.get(profile_url, headers=profile_headers)
    profile_json = profile_response.json()
    return profile_json


@app.get("/top-tracks")
async def get_top_tracks(request: Request, time_range: TimeRange):
    access_token = request.headers.get("Authorization").split("Bearer ")[1]
    top_tracks_url = (
        f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit=10"
    )
    top_tracks_headers = {"Authorization": f"Bearer {access_token}"}
    top_tracks_response = requests.get(top_tracks_url, headers=top_tracks_headers)
    top_tracks_json = top_tracks_response.json()
    return top_tracks_json


@app.get("/top-singers")
async def get_top_singers(request: Request, time_range: TimeRange):
    access_token = request.headers.get("Authorization").split("Bearer ")[1]
    top_singers_url = (
        f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit=10"
    )
    top_singers_headers = {"Authorization": f"Bearer {access_token}"}
    top_singers_response = requests.get(top_singers_url, headers=top_singers_headers)
    top_singers_json = top_singers_response.json()
    return top_singers_json
