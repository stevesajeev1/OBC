from uuid import UUID

from pydantic import BaseModel


class Favorite(BaseModel):
    user_id: int
    listing_id: UUID
