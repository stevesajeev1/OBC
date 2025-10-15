import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.auth import *
from ..util.auth import *
from ..util.db import *

# --- router ---
router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- api endpoints ---
@router.get("/users/me/", response_model=User)
def read_users_me(current_user: Annotated[User, Depends(get_user)]):
    """get details for the current user"""
    return current_user