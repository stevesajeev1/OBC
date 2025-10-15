# pydantic models for routers/auth.py

from typing import Union

from pydantic import BaseModel

# --- pydantic models ---


class User(BaseModel):
    """basic user model"""

    username: str


class DBUser(User):
    """model with hashed password for DB use"""

    hashed_password: str


class ResponseToken(BaseModel):
    """model representing the response of /login"""

    access_token: str
    token_type: str


class Token(BaseModel):
    """model representing the JWT data"""

    username: str

    def to_dict(self) -> dict:
        """convert token data to dict"""
        return self.model_dump()
