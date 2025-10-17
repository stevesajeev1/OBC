# utility file for helper functions used in routers/auth.py

import os
from typing import Annotated

import psycopg2
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..models.auth import DBUser, Token, TokenType
from ..util.db import get_db_connection

# --- hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_from_db(username: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT username, hashed_password FROM users WHERE username = %s",
                (username,),
            )
            user_record = cur.fetchone()
            if user_record:
                return DBUser(username=user_record[0], hashed_password=user_record[1])
    finally:
        conn.close()
    return None


def create_user(user: DBUser):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                (user.username, user.hashed_password),
            )
            conn.commit()
            return True
    except psycopg2.Error as e:
        conn.rollback()
        return False
    finally:
        conn.close()


def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jwt_token = Token.from_jwt(token, TokenType.ACCESS)
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(jwt_token.username)
    if user is None:
        raise credentials_exception
    return user
