# FastAPI Spotify Authentication System

This repository contains a FastAPI application that integrates with the Spotify API to provide authentication and user profile retrieval.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/githubnext/spotify-api.git
   cd spotify-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Spotify API Credentials

To use the Spotify API, you need to create a Spotify Developer account and register your application to obtain the necessary credentials.

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in with your Spotify account.
2. Click on "Create an App" and fill in the required details.
3. Once the app is created, you will be provided with a `Client ID` and `Client Secret`.
4. Set the `Redirect URI` to the URL where you want Spotify to redirect after authentication (e.g., `http://localhost:8000/auth/spotify/callback`).

## Setting up the .env file

1. Create a `.env` file in the root directory of your project.
2. Add your Spotify credentials to the `.env` file:
   ```env
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
   ```

## Running the FastAPI App

1. Start the FastAPI app using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to `http://localhost:8000/docs` to access the interactive API documentation provided by FastAPI.

## Using the Endpoint to List 10 Most Listened Songs

1. Authenticate the user by navigating to the `/auth/spotify` endpoint and following the authentication flow.
2. Use the access token obtained from the `/auth/spotify/callback` endpoint to make authorized requests.
3. To list the 10 most listened songs of the logged-in user in the last week, month, and year, use the `/top-tracks` endpoint with the appropriate `time_range` query parameter (`short_term` for last week, `medium_term` for last month, and `long_term` for last year).

## Using the Endpoint to List Top Singers

1. Authenticate the user by navigating to the `/auth/spotify` endpoint and following the authentication flow.
2. Use the access token obtained from the `/auth/spotify/callback` endpoint to make authorized requests.
3. To list the top singers of the logged-in user in the last week, month, and year, use the `/top-singers` endpoint with the appropriate `time_range` query parameter (`short_term` for last week, `medium_term` for last month, and `long_term` for last year).

## How to Run the Frontend

1. Install a local web server (if not already installed):
   ```bash
   npm install -g http-server
   ```

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Start the local server:
   ```bash
   http-server -p 3000
   ```

4. Open your browser and visit `http://localhost:3000`

Note: Make sure both the FastAPI backend (on port 8000) and the frontend server (on port 3000) are running simultaneously.
