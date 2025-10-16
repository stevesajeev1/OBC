# pydantic models for routers/auth.py

from datetime import datetime
from typing import Any

from pydantic import BaseModel

# --- pydantic models ---


class User(BaseModel):
    """basic user model"""

    username: str


class DBUser(User):
    """model with hashed password for DB use"""

    hashed_password: str


class Token(BaseModel):
    """model representing the JWT data"""

    username: str

    def __init__(self, username):
        super().__init__(username=username)

    @staticmethod
    def from_jwt_payload(jwt_payload: dict[str, Any]):
        username = jwt_payload.get("sub", None)
        if not isinstance(username, str):
            raise Exception("JWT Payload is malformed")

        return Token(username)

    def to_jwt_payload(self, exp: datetime):
        return {"sub": self.username, "exp": exp}
