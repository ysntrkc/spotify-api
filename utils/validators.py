from fastapi import HTTPException


def validate_time_range(time_range: str):
    if time_range not in ["short_term", "medium_term", "long_term"]:
        raise HTTPException(status_code=400, detail="Invalid time range")


def validate_limit(limit: int):
    if limit not in [10, 25, 50]:
        raise HTTPException(status_code=400, detail="Limit must be 10, 25, or 50")
