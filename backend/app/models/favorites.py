from pydantic import BaseModel
from uuid import UUID

class Favorite(BaseModel):
    user_id: int
    listing_id: UUID

    



