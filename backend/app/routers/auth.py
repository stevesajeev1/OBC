import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import *
from ..util.auth import *
from ..util.db import *

# --- router ---
router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- api endpoints ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if get_user_from_db(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(form_data.password)

    new_user = DBUser(username=form_data.username, hashed_password=hashed_password)

    user_created = create_user(new_user)

    if not user_created:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create account (Database Error)",
        )

    # create and return access token
    token_data = Token(username=form_data.username)
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_from_db(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token_data = Token(username=user.username)
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
