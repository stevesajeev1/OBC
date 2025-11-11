from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..models.auth import DBUser
from ..models.profile import Profile, ProfileUpdate
from ..util.auth import get_user
from ..util.profile import *

# --- router ---
router = APIRouter(prefix="/profile", tags=["Profile"])


# --- api endpoints ---
@router.get("/me", response_model=dict, status_code=status.HTTP_200_OK)
def get_own_profile(current_user: Annotated[DBUser, Depends(get_user)]):
    """READ ; get profile for currently logged in user"""

    profile_data = get_raw_profile_data(current_user.username)
    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile cannot be found"
        )
    return profile_data


@router.put("/me", response_model=dict, status_code=status.HTTP_200_OK)
def update_own_profile(
    profile_data: ProfileUpdate, current_user: Annotated[DBUser, Depends(get_user)]
):
    """CREATE/UPDATE ; create or update the logged in user profile"""
    updated_profile = update_profile(current_user.username, profile_data)
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update profile",
        )
    return updated_profile


@router.get("/{username}", response_model=Profile, status_code=status.HTTP_200_OK)
def get_public_profile(username: str):
    """(READ) get ANOTHER user's public profile by their username"""

    profile = get_valid_profile(username)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile could not be found"
        )
    return profile
