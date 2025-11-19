from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..models.auth import DBUser
from ..models.profile import Profile, ProfileUpdate
from ..util.auth import get_user
from ..util.profile import get_valid_profile, get_all_profiles, update_profile

# --- router ---
router = APIRouter(prefix="/profiles", tags=["Profile"])


# --- api endpoints ---
@router.get("/me", response_model=Profile, status_code=status.HTTP_200_OK)
def get_own_profile(current_user: Annotated[DBUser, Depends(get_user)]):
    """READ ; get profile for currently logged in user"""

    profile_data = get_valid_profile(current_user.username)
    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile cannot be found"
        )
    return profile_data


@router.patch("/me", response_model=Profile, status_code=status.HTTP_200_OK)
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


@router.get("/", response_model=list[Profile], status_code=status.HTTP_200_OK)
def get_profiles(page: int=1, limit: int=20):
    """(READ) get ALL user's public profile"""

    return get_all_profiles(page, limit)