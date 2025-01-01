from typing import Dict, Any, List


def filter_track_data(track: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": track["name"],
        "artists": [{"name": artist["name"]} for artist in track["artists"]],
        "album": {
            "name": track["album"]["name"],
            "image": (
                track["album"]["images"][0]["url"] if track["album"]["images"] else None
            ),
        },
    }


def filter_singer_data(artist: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": artist["name"],
        "image": artist["images"][0]["url"] if artist["images"] else None,
    }


def filter_profile_data(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "display_name": profile.get("display_name"),
        "email": profile.get("email"),
        "id": profile.get("id"),
        "images": [img.get("url") for img in profile.get("images", [])],
    }
