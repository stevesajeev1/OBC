# pydantic models for routers/auth.py

import os
from datetime import datetime, timedelta, timezone
from enum import Enum

from jose import JWTError, jwt
from pydantic import BaseModel

# --- config ---
JWT_ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 30 * 60
REFRESH_TOKEN_EXPIRE_SECONDS = 7 * 24 * 60 * 60

# --- pydantic models ---


class User(BaseModel):
    """basic user model"""

    username: str
    admin: bool


class DBUser(User):
    """model with hashed password for DB use"""

    hashed_password: str


class TokenType(Enum):
    ACCESS = 1
    REFRESH = 2


def get_secret(token_type: TokenType):
    match token_type:
        case TokenType.ACCESS:
            JWT_SECRET = JWT_ACCESS_SECRET
        case TokenType.REFRESH:
            JWT_SECRET = JWT_REFRESH_SECRET

    if JWT_SECRET is None:
        raise Exception(f"JWT_SECRET for {token_type} is not defined")
    return JWT_SECRET


def get_expiry(token_type: TokenType):
    match token_type:
        case TokenType.ACCESS:
            return ACCESS_TOKEN_EXPIRE_SECONDS
        case TokenType.REFRESH:
            return REFRESH_TOKEN_EXPIRE_SECONDS


class Token(BaseModel):
    """model representing the JWT data"""

    username: str
    token_type: TokenType

    def __init__(self, username: str, token_type: TokenType):
        super().__init__(username=username, token_type=token_type)

    @staticmethod
    def from_jwt(token: str, token_type: TokenType):
        JWT_SECRET = get_secret(token_type)

        jwt_payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = jwt_payload.get("sub", None)
        tt = jwt_payload.get("token_type", None)
        if (
            not isinstance(username, str)
            or not isinstance(tt, str)
            or tt != token_type.name
        ):
            raise JWTError("JWT Payload is malformed")

        return Token(username, token_type)

    def to_jwt(self):
        JWT_SECRET = get_secret(self.token_type)
        expiry = get_expiry(self.token_type)

        expire = datetime.now(timezone.utc) + timedelta(seconds=expiry)
        jwt_payload = {
            "sub": self.username,
            "exp": expire,
            "token_type": self.token_type.name,
        }
        return jwt.encode(jwt_payload, JWT_SECRET, algorithm=ALGORITHM)
