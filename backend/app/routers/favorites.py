from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.auth import User
from ..models.listings import Listing
from ..util.auth import get_user
from ..util.favorites import (
    delete_favorite_from_db,
    get_favorites_from_db,
    save_favorite_to_db,
)

# --- router ---
router = APIRouter(prefix="/favorites", tags=["Favorites"])


# --- api endpoints ---
@router.post("/{listing_id}", status_code=status.HTTP_201_CREATED)
def favorite_listing(listing_id: UUID, user: Annotated[User, Depends(get_user)]):
    user_id = user.id

    if not save_favorite_to_db(user_id, listing_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to favorite listing with id. {listing_id} already favorited.",
        )


@router.get("/", response_model=list[Listing], status_code=status.HTTP_200_OK)
def get_favorites(user: Annotated[User, Depends(get_user)]):
    user_id = user.id
    favorites = get_favorites_from_db(user_id)
    return favorites


@router.delete("/{listing_id}", status_code=status.HTTP_200_OK)
def unfavorite_listing(listing_id: UUID, user: Annotated[User, Depends(get_user)]):
    user_id = user.id

    if not delete_favorite_from_db(user_id, listing_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to unfavorite listing with id. {listing_id} not yet favorited.",
        )
