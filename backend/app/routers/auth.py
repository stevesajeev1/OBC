import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from ..util.db import *
from ..util.auth import *
from ..models.auth import *

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
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                (form_data.username, hashed_password),
            )
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )
    finally:
        conn.close()

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
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
def read_users_me(current_user: Annotated[User, Depends(get_user)]):
    return current_user
