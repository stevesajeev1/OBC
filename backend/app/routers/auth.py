from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from ..models.auth import DBUser, Token, TokenType, get_expiry
from ..util.auth import (
    create_user,
    get_password_hash,
    get_user_from_db,
    verify_password,
)

# --- router ---
router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- api endpoints ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
):
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

    # create and return tokens
    access_token = Token(username=form_data.username, token_type=TokenType.ACCESS)
    refresh_token = Token(username=form_data.username, token_type=TokenType.REFRESH)
    access_jwt = access_token.to_jwt()
    refresh_jwt = refresh_token.to_jwt()

    response.set_cookie(
        key="refresh_token",
        value=refresh_jwt,
        max_age=get_expiry(TokenType.REFRESH),
        path="/auth",
        secure=True,
        httponly=True,
        samesite="none",
    )
    return access_jwt


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
):
    user = get_user_from_db(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # create and return tokens
    access_token = Token(username=form_data.username, token_type=TokenType.ACCESS)
    refresh_token = Token(username=form_data.username, token_type=TokenType.REFRESH)
    access_jwt = access_token.to_jwt()
    refresh_jwt = refresh_token.to_jwt()

    response.set_cookie(
        key="refresh_token",
        value=refresh_jwt,
        max_age=get_expiry(TokenType.REFRESH),
        path="/auth",
        secure=True,
        httponly=True,
        samesite="none",
    )
    return access_jwt


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(response: Response):
    response.delete_cookie(key="refresh_token", path="/auth")


@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_token(
    response: Response, refresh_token: Annotated[str | None, Cookie()] = None
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
        )

    try:
        token = Token.from_jwt(refresh_token, TokenType.REFRESH)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # create and return tokens
    access_token = Token(username=token.username, token_type=TokenType.ACCESS)
    new_refresh_token = Token(username=token.username, token_type=TokenType.REFRESH)

    access_jwt = access_token.to_jwt()
    refresh_jwt = new_refresh_token.to_jwt()

    response.set_cookie(
        key="refresh_token",
        value=refresh_jwt,
        max_age=get_expiry(TokenType.REFRESH),
        path="/auth",
        secure=True,
        httponly=True,
        samesite="none",
    )

    return access_jwt
