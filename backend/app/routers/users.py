from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..models.auth import User
from ..util.auth import get_user

# --- router ---
router = APIRouter(prefix="/users", tags=["User"])


# --- api endpoints ---
@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
def read_users_me(current_user: Annotated[User, Depends(get_user)]):
    """get details for the current user"""
    return current_user
