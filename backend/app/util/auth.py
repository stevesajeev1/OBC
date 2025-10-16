# utility file for helper functions used in routers/auth.py

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import psycopg2
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..models.auth import DBUser, Token
from ..util.db import get_db_connection

# --- config ---
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


def create_access_token(data: Token):
    if JWT_SECRET_KEY is None:
        raise Exception("JWT_SECRET_KEY is not defined")

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_payload = data.to_jwt_payload(expire)
    return jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if JWT_SECRET_KEY is None:
        raise Exception("JWT_SECRET_KEY is not defined")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        jwt_token = Token.from_jwt_payload(payload)
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(jwt_token.username)
    if user is None:
        raise credentials_exception
    return user
